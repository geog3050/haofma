#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEOG:5050 Geospatial Programming
Spring 2022
Final Project

Haofeng Ma
"""

from pysal.lib import weights
from pysal.model import spreg
import numpy as np
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import seaborn
import statsmodels.formula.api as sm

import os

"""
Read Data and Process Variables
"""

# the input file should be in the current working directory
workingdir = os.getcwd()

df = geopandas.read_file(workingdir + '/data_individual_region.geojson')


# overwrite empty cells in the dataframe with NaN
df = df.replace(r'^\s*$', np.nan, regex=True)

# drop rows with at least a NaN (listwise deletion)
df = df.dropna()

# rescale and change the types of variables
df.trust_president = df.trust_president.astype(float) + 1 # change the range from the original [0, 3] to [1, 4]
df.LD_french = df.LD_french.astype(float)
df.Lfrac_norm = df.Lfrac_norm.astype(float)
df.male = df.male.astype(float)
df.age = df.age.astype(float)
df.urban = df.age.astype(float)
df.edu = df.edu.astype(float)
df.living = df.living.astype(float)
df.member_religious = df.member_religious.astype(float)
df.member_voluntary = df.member_voluntary.astype(float)
df.use_mobile = df.use_mobile.astype(float)
df.use_internet = df.use_internet.astype(float)
df.interest = df.interest.astype(float)

df.pop_den = df.pop_den.astype(float)
pop_den_ln = np.log(df.pop_den) # natural log of the original values
df.pop_den = pop_den_ln

df.health_index = df.health_index.astype(float)
df.education_index = df.education_index.astype(float)
df.income_index = df.income_index.astype(float)

# generate dummy variables for eacg ethnicity
df['ethnicity'] = df['ethnicity'].astype('category')
ethnicity = pd.get_dummies(df['ethnicity'])

for name in ethnicity.columns:
    ethnicity = ethnicity.rename(columns={name: 'ethnicity_' + str(name)})

df = pd.concat([df, ethnicity], axis=1, join="inner") # join the created ethnicity dummies to the dataframe


# generate dummy variables for each region
df['region'] = df['region'].astype('category')
region = pd.get_dummies(df['region'])

for name in region.columns:
    region = region.rename(columns={name: 'region_' + str(name).replace('.0', '')})

df = pd.concat([df, region], axis=1, join="inner") # join the created region dummies to the dataframe

# generate an interaction term between two main IVs (LD_french & Lfrac_norm)
df['LDLfrac'] = df['LD_french']*df['Lfrac_norm'].astype('float')


# list of individual-level IVs' names (except dummies)
variable_names_base = ['LD_french', 'LDLfrac', 'male', 'age', 'edu', 'living', 'member_religious', 'member_voluntary', 'use_mobile', 'use_internet', 'interest']

# list of region-level IVs' names
variable_names_regionlv = ['pop_den', 'health_index', 'education_index', 'income_index', 'Lfrac_norm']

# list of ethnicity dummy variables' names
variable_names_ethnicity = []
for name in ethnicity.columns[ :-1]: # drop the last category of ethnicity to avoid multicollinearity
    variable_names_ethnicity.append(name)

# list of region dummy variables' names
variable_names_region = []
for name in region.columns:
    variable_names_region.append(name)


"""
Fit Basic OLS model
without any spatial component
"""

# independent variables to be included
variable_names= variable_names_base + variable_names_ethnicity + variable_names_regionlv

m1 = spreg.OLS(
    # Dependent variable
    df[['trust_president']].values, 
    # Independent variables
    df[variable_names].values,
    # Dependent variable name
    name_y='trust_president', 
    # Independent variable name
    name_x=variable_names
)
print(m1.summary)


"""
Examine whether the errors are spatially clustered
"""

# Create column with residual values from m1
df['residual'] = m1.u


# Obtain the median value of residuals in each region
residual_region_medians = df.groupby(
    "region"
).residual.median().to_frame(
    'region_residual'
)


# Plot the mean and the distribution of residuals in each region
    
# Increase fontsize
seaborn.set(font_scale = 1.25)
# Set up figure
f = plt.figure(figsize=(15,3))
# Grab figure's axis
ax = plt.gca()
# Generate bloxplot of values by region
# Note the data includes the median values merged on-the-fly
seaborn.boxplot(
    'region', 
    'residual', 
    ax = ax,
    data=df.merge(
        residual_region_medians, 
        how='left',
        left_on='region',
        right_index=True
    ).sort_values(
        'region_residual'), palette='bwr'
)
# Auto-format of the X labels
f.autofmt_xdate()
# Display
plt.show()    
    
    
"""
Spatial fixed effects
"""

# a string of region dummies
variable_names_region_str = ''
for name in variable_names_region:
    variable_names_region_str += ' + ' + name

# other independent variables (except region dummies) to be included
variable_names = variable_names_base + variable_names_ethnicity


f = 'trust_president ~ ' + ' + '.join(variable_names) + variable_names_region_str + ' - 1'
print(f)
    
m2 = sm.ols(f, data=df).fit()


# Store variable names for all the spatial fixed effects
sfe_names = [i for i in m2.params.index if 'region_' in i]
# Create table
pd.DataFrame(
    {
        'Coef.': m2.params[sfe_names],
        'Std. Error': m2.bse[sfe_names],
        'P-Value': m2.pvalues[sfe_names]
    }
)


region_effects = m2.params.filter(like='region')
region_effects


"""
Endogenous spatial effects (spatial lag of DV)
"""

# spatial weight
knn = weights.KNN.from_dataframe(df, k=100) # only consider the linkages of each individual to their closest 100 other individuals

wx_dv = df.filter(
    like='trust'
# Select only columns in `df` containing the keyword `trust` (name of DV)
# Compute the spatial lag of each of those variables
).apply(
    lambda y: weights.spatial_lag.lag_spatial(knn, y)
# Rename the spatial lag, adding w_ to the original name
).rename(
    columns=lambda c: 'w_'+c
)


# Join the spatial lag of DV into the dataframe
df['w_trust_president'] = wx_dv

# update the list of variable names
variable_names_endogenous = variable_names_base + variable_names_regionlv + variable_names_ethnicity + ['w_trust_president']


# Fit linear model accounting for exogenous spatial effects
m3 = spreg.OLS(
    # Dependent variable
    df[['trust_president']].values, 
    # Independent variables
    df[variable_names_endogenous].values,
    # Dependent variable name
    name_y='trust_president', 
    # Independent variables names
    name_x=variable_names_endogenous
)

print(m3.summary)


"""
Exogenous spatial effects (spatial lag of IVs)
"""

wx_iv = df.filter(
    like='L'
# Select only columns in `df` containing the keyword `L_` (names of main IVs)
# Compute the spatial lag of each of those variables
).apply(
    lambda y: weights.spatial_lag.lag_spatial(knn, y)
# Rename the spatial lag, adding w_ to the original name
).rename(
    columns=lambda c: 'w_'+c
)

   
# Join the spatial lag of IVs into the dataframe
df = pd.concat([df, wx_iv], axis=1, join="inner")


# list of IVs' names (with ethnicity dummies and region dummies)
variable_names_exogenous = variable_names_base + variable_names_regionlv + variable_names_ethnicity + ['w_LD_french'] + ['w_Lfrac_norm'] + ['w_LDLfrac']

# Fit linear model accounting for exogenous spatial effects
m4 = spreg.OLS(
    # Dependent variable
    df[['trust_president']].values, 
    # Independent variables
    df[variable_names_exogenous].values,
    # Dependent variable name
    name_y='trust_president', 
    # Independent variables names
    name_x=variable_names_exogenous
)

print(m4.summary)


"""
Model Endogenous Spatial Effects and Exogenous Spatial Effects together
"""

# list of IVs' names (with ethnicity dummies and region dummies)
variable_names_all = variable_names_base + variable_names_regionlv + variable_names_ethnicity + ['w_trust_president'] + ['w_LD_french'] + ['w_Lfrac_norm'] + ['w_LDLfrac']

# Fit linear model accounting for both the endogenous spatial effects and the exogenous spatial effects
m5 = spreg.OLS(
    # Dependent variable
    df[['trust_president']].values, 
    # Independent variables
    df[variable_names_all].values,
    # Dependent variable name
    name_y='trust_president', 
    # Independent variables names
    name_x=variable_names_all
)

print(m5.summary)