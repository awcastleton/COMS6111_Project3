#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import csv
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))
rawdata_csv = os.path.join(scriptdir,'Times_Square_Property_Data__Commercial_and_Retail_properties_.csv')
curated_csv = os.path.join(scriptdir,'../INTEGRATED-DATASET.csv')

def main():
    # Allow max character length of string fields to be long enough
    pd.set_option("display.max_colwidth", 10000)

    print('reading raw data...')
    df = pd.read_csv(rawdata_csv)

    print('filtering raw data...')
    filtered_df = df[(df.Amenities.notnull()) & (df.Amenities.str.contains(','))]['Amenities']

    print(filtered_df)
    print('%s records left after filtering...' % len(filtered_df))
    print('writing curated data to file...')

    with open(curated_csv,'w') as f:
        for index, row in filtered_df.iteritems():
            f.write(row + '\n')

if __name__ == '__main__':
    sys.exit(main())
