#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import csv
import os

from sodapy import Socrata

NUM_ROWS = 100000

scriptdir = os.path.dirname(os.path.realpath(__file__))
curated_csv = os.path.join(scriptdir,'../INTEGRATED-DATASET.csv')

def main():
    client = Socrata("data.cityofnewyork.us", None)

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    result_list = client.get("fhrw-4uyv", limit=NUM_ROWS)

    # Convert to pandas DataFrame
    print('reading raw data...')
    df = pd.DataFrame.from_records(result_list)

    print('filtering raw data...')
    df = df[pd.notnull(df['incident_address'])]
    housing_complaints_df = df[(df['agency'].isin(['HPD', 'DOB']))]
    noise_complaints_df = df[(df.complaint_type.str.contains('Noise')) & (df.location_type.str.contains('Residential'))]

    filtered_df = pd.merge(housing_complaints_df, noise_complaints_df, on='incident_address', how='inner')
    filtered_df = filtered_df[['complaint_type_x', 'complaint_type_y', 'descriptor_x', 'descriptor_y', 'incident_address']]

    print('%s records left after filtering...' % len(filtered_df))

    print('writing curated data to file...')
    filtered_df.to_csv(curated_csv, header=True, index=False)

if __name__ == '__main__':
    sys.exit(main())
