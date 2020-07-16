import sys
import argparse
import os
import pandas as pd
import numpy as np

# create the master data file
columns=['iso3c', 'country', 'description', 'value', 'units', 'year', 'source']
df = pd.DataFrame(columns=columns)

# included values and their units
# MSW (Million tonnes per year) from World Bank
# MSW per person (Kg per person per year) from World Bank
# Waste collection coverage by population (Percent of population) from World Bank
# Waste collection coverage by percent of waste (Percent of waste) from World Bank
# Waste treatment (Percent) from World Bank
# Waste composition (Percent) from World Bank
# Special waste (Million tonnes per year) from World Bank





# load country-to-iso3c dictionary
f1 = pd.read_csv('iso3c_codes.tsv', sep='\t', header=None)
country_to_iso3c = {}
iso3c_to_country = {}
for index, row in f1.iterrows():
	country_to_iso3c[row[1]] = row[0]
	if row[0] not in iso3c_to_country:
		iso3c_to_country[row[0]] = row[1]

# load World Bank dataset
f1 = pd.read_csv('../data_original/country_level_data_0.csv', sep=',')
f2 = pd.read_csv('country_level_codebook.tsv', sep='\t', dtype=object)
f3 = pd.read_csv('population.tsv', sep='\t')

# add total_msw_generated_tons_year and total MSW per capita
var = 'total_msw_total_msw_generated_tons_year'
for index, row in f1.iterrows():
	if not pd.isnull(row[var]):
		try:
			country = row['iso3c']
			value = row[var]/1000000
			year = f2['year'].loc[(f2['iso3c'] == country) & (f2['measurement'] == var)].values[0]
			df.loc[len(df)] = [country, iso3c_to_country[country], 'MSW', value, 'Million tonnes per year', year, 'World Bank']
			try:
				population = f3['Population'].loc[(f3['Code'] == country) & (f3['Year'] == year)].values[0]
				value2 = (row[var]*1000)/population
				df.loc[len(df)] = [country, iso3c_to_country[country], 'MSW per person', value2, 'Kg per person per year', year, 'World Bank']
			except:
				print('No population data for %s in %s'%(country, year))
		except: 
			print('Problem with %s'%(row['iso3c']))

# add waste collection
variables = ['waste_collection_coverage_total_percent_of_population', 'waste_collection_coverage_total_percent_of_waste']
units = ['Percent of population', 'Percent of waste']
for index, row in f1.iterrows():
	country = row['iso3c']
	for idx, var in enumerate(variables):
		if not pd.isnull(row[var]):
			try:
				year = f2['year'].loc[(f2['iso3c'] == country) & (f2['measurement'] == var)].values[0]
				df.loc[len(df)] = [country, iso3c_to_country[country], var, row[var], units[idx], year, 'World Bank']
			except: 
				print('Problem with %s in %s'%(var, row['iso3c']))

# add waste treatment
variables = [x for x in list(f1) if 'waste_treatment_' in x]
# check that they add up to 100%
f1['waste_treatment_sum'] = f1[variables].sum(axis=1)
set(f1['waste_treatment_sum'])
# add to df
for index, row in f1.iterrows():
	country = row['iso3c']
	for var in variables:
		if not pd.isnull(row[var]):
			try:
				year = f2['year'].loc[(f2['iso3c'] == country) & (f2['measurement'] == var)].values[0]
				df.loc[len(df)] = [country, iso3c_to_country[country], var, row[var], 'Percent', year, 'World Bank']
			except: 
				print('Problem with %s for %s'%(var, row['iso3c']))

# add waste composition
variables = [x for x in list(f1) if 'composition_' in x]
# check that they add up to 100%
f1['waste_composition_sum'] = f1[variables].sum(axis=1)
set(f1['waste_composition_sum'])
# exclude countries that add up to < 85%
exclude = ['MCO', 'NGA']
# add to df
for index, row in f1.iterrows():
	country = row['iso3c']
	if country not in exclude:
		for var in variables:
			if not pd.isnull(row[var]):
				try:
					year = f2['year'].loc[(f2['iso3c'] == country) & (f2['measurement'] == var)].values[0]
					df.loc[len(df)] = [country, iso3c_to_country[country], var, row[var], 'Percent', year, 'World Bank']
				except: 
					print('Problem with %s for %s'%(var, row['iso3c']))

# add special waste
variables = [x for x in list(f1) if 'special_waste_' in x]
for index, row in f1.iterrows():
	country = row['iso3c']
	for var in variables:
		if not pd.isnull(row[var]):
			try:
				year = f2['year'].loc[(f2['iso3c'] == country) & (f2['measurement'] == var)].values[0]
				df.loc[len(df)] = [country, iso3c_to_country[country], var, row[var]/1000000, 'Million tonnes per year', year, 'World Bank']
			except: 
				print('Problem with %s for %s'%(var, row['iso3c']))

## save data
df.to_csv('data_processed.tsv', sep='\t', index=False)
