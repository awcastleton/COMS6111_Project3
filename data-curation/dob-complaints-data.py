#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import csv
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))
rawdata_csv = os.path.join(scriptdir,'DOB_Complaints_Received.csv')
curated_csv = os.path.join(scriptdir,'../INTEGRATED-DATASET.csv')

complaint_category_csv = os.path.join(scriptdir,'DOB_Complaint_Category.csv')
disposition_code_csv = os.path.join(scriptdir,'DOB_Complaint_Disposition_Codes.csv')

def main():
    # Allow max character length of string fields to be long enough
    pd.set_option("display.max_colwidth", 10000)

    print('reading raw data...')
    df = pd.read_csv(rawdata_csv)

    # Merge complaint category descriptions
    complaint_categories_df = pd.read_csv(complaint_category_csv)
    del complaint_categories_df['Priority']
    df = pd.merge(df, complaint_categories_df, on='Complaint Category', how='left')

    # Merge disposition code descriptions
    disposition_codes_df = pd.read_csv(disposition_code_csv)
    df = pd.merge(df, disposition_codes_df, on='Disposition Code', how='left')

    # Leaving community board, complaint type, disposition code, unit
    print('filtering raw data...')
    df = df[pd.notnull(df['Complaint Description'])]
    df = df[pd.notnull(df['Disposition Description'])]
    df = df[0:250000] # OPTIONAL, trim data to manageable size
    filtered_df = df[['House Street', 'Complaint Description', 'Disposition Description', 'Unit']]

    print('%s records left after filtering...' % len(filtered_df))

    print('writing curated data to file...')
    filtered_df.to_csv(curated_csv, header=False, index=False)

if __name__ == '__main__':
    sys.exit(main())
