#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))
rawdata_csv = os.path.join(scriptdir,'Times_Square_Property_Data__Commercial_and_Retail_properties_.csv')
curated_csv = os.path.join(scriptdir,'INTEGRATED-DATASET.csv')

def main():
    # TODO
    print('reading raw data...')
    df = pd.read_csv(rawdata_csv)

    print('filtering raw data...')
    filtered_df = df[(df.Amenities.notnull()) & (df.Amenities.str.contains(','))]['Amenities']

    print(filtered_df)
    print('%s records left after filtering...' % len(filtered_df))
    print('writing curated data to file...')
    filtered_df.to_csv(curated_csv,header=None)

if __name__ == '__main__':
    sys.exit(main())
