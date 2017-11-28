#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import csv
import os

CONFIDENCE = 0.3
SUPPORT = 0.01
DATASET = 'INTEGRATED-DATASET.csv'

scriptdir = os.path.dirname(os.path.realpath(__file__))

def main():
    # read config values from command line
    initCLI()

    # load data into application
    curated_csv = os.path.join(scriptdir, DATASET)

    print('reading text...') # TESTING
    with open(curated_csv,'r') as f:
        raw = f.read()

    print('parsing text into usable data...') # TESTING
    transactions = []
    items = set()
    for t in raw.split('\n')[:-1]: # don't include last line (which is just an empty string)
        new_itemset = set(map(str.strip,t.split(',')))
        transactions.append(new_itemset)
        items = items | new_itemset

    print('Determining initial frequent items...')
    print(getInitialFrequentItems(transactions,items))

def initCLI():
    # load dataset filename
    global DATASET
    if len(sys.argv) > 1: DATASET = sys.argv[1]

    # load mininmum support
    global SUPPORT
    if len(sys.argv) > 4: SUPPORT = float(sys.argv[2])

    # load minimum confidence
    global CONFIDENCE
    if len(sys.argv) > 4: CONFIDENCE = float(sys.argv[3])

def getInitialFrequentItems(transactions, items):
    frequent = set()
    for i in items:
        ct = 0
        for t in transactions:
            if set([i]).issubset(set(t)):
                ct+=1
        if (ct / len(transactions)) > SUPPORT:
            frequent.add(i)
    return frequent

# Boolean: is the itemset's frequency greater than the support threshold?
def isFrequent(transactions,itemset):
    ct = 0

    for t in transactions:
        if itemset.issubset(t):
            ct+=1

    passes_support = (ct / len(transactions)) > SUPPORT


    # METHODS NEEDED:
    # TODO: compute confidence of itemset
    # TODO: outer loop of itemset size
    # TODO: compute INITIAL frequent items (size=1) DONE
    # TODO: 3. compute frequent itemsets (support > threshold, confidence > threshold)
    # TODO: get all subsets of size n (includes pruning impossible itemsets)
    # TODO: 4. build association rules
    # TODO: 5. Printout of frequent itemsets (output.txt)

    # TODO: find a larger dataset!

    '''
    LOOP set size = 2 -> k:
        * determine possible frequent itemsets from previous frequent itemsets
        * calculate and record frequent item subsets
        * calculate high-confidence assoc. rules from the frequent itemsets of this size
        * add assoc. rules to our dict (frozenset -> {'Value':'item','Conf':0.13,'Supp':0.08})
    '''

if __name__ == '__main__':
    if len(sys.argv) > 1: DATASET = sys.argv[1]
    if len(sys.argv) > 2: SUPPORT = float(sys.argv[2])
    if len(sys.argv) > 3: CONFIDENCE = float(sys.argv[3])
    sys.exit(main())
