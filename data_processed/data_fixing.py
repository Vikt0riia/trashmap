import sys
import argparse
import os
import pandas as pd
import numpy as np

# correct population.csv
f1 = pd.read_csv('../data_original/population.csv', sep=',')
f1.loc[f1['Entity'] == 'Channel Islands', 'Code'] = 'CHI'
f1.to_csv('population.tsv', sep='\t', index=False)

# correct country_level_codebook.csv
f1 = pd.read_csv('../data_original/country_level_codebook.csv', sep=',')
f1.loc[len(f1)] = ['','BIH','','','waste_treatment_recycling_percent','','2015','','']
f1.loc[len(f1)] = ['','SYR','','','composition_other_percent','','2010','','']
f1.loc[(f1['iso3c'] == 'LCA') & (f1['measurement'] == 'special_waste_medical_waste_tons_year'), 'year'] = '2015'
f1.to_csv('country_level_codebook.tsv', sep='\t', index=False)





