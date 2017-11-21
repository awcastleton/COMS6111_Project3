#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import csv
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))
curated_csv = os.path.join(scriptdir,'INTEGRATED-DATASET.csv')

def main():
    print('reading text...')
    with open(curated_csv,'r') as f:
        raw = f.read()

    print('parsing text into usable data...')
    transactions = []
    for t in raw.split('\n'):
        transactions.append(list(map(str.strip,t.split(','))))

    print(transactions)

if __name__ == '__main__':
    sys.exit(main())
