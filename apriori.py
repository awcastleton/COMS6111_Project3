#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import csv
import os

TARGET_CONFIDENCE = 0.3
TARGET_SUPPORT = 0.30
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

    # This will keep track of frequent itemsets of each size (size-1 = index)
    frequent = []
    supports = []

    print('Determining initial frequent items...')
    initial_frequent, initial_supports = getInitialFrequentItems(transactions,items)
    frequent.append(initial_frequent)
    supports.append(initial_supports)

    set_size = 2
    cont = True
    while cont: # TODO flesh out main loop
        print('=========== Size ' + str(set_size-1) + ' ===========')
        printFrequentItemsets(frequent[set_size-2],supports[set_size-2])

        # Generate possible itemsets of this size
        possible_itemsets = generatePossibleItemsets(items, frequent[set_size-2])

        # Generate new frequent itemsets of this size and their supports
        new_frequent, new_supports = getFrequentItemsets(items, transactions, possible_itemsets, set_size)
        frequent.append(new_frequent)
        supports.append(new_supports)

        # continue?
        cont = len(frequent[set_size-1]) > 0
        set_size += 1

def printFrequentItemsets(frequent,supports):
    if (TARGET_SUPPORT * 100).is_integer():
        print('==Frequent itemsets (min_sup={0}%)'.format(int(TARGET_SUPPORT * 100)) )
    else:
        print('==Frequent itemsets (min_sup={0}%)'.format(TARGET_SUPPORT * 100) )
    for f,s in zip(frequent,supports):
        print(str(f) + ", %.2f" % (s*100) + '%')

def getInitialFrequentItems(transactions, items):
    frequent = []
    supports = []
    for i in items:
        ct = 0
        for t in transactions:
            if set([i]).issubset(set(t)):
                ct+=1
        support = (ct / len(transactions))
        if support >= TARGET_SUPPORT:
            frequent.append([i])
            supports.append(support)

    # print('Initial Frequent Items: ') # TESTING
    # print(frequent) # TESTING

    return frequent, supports

# TODO: returns list of frequent itemsets of the given size
def getFrequentItemsets(items,transactions,possible_itemsets,set_size):
    frequent = []
    supports = []

    # Loop through possible itemsets
    for s in possible_itemsets:
        ct = 0

        # Record itemset if it passes support threshold
        support = getSupport(transactions, set(s))
        if support >= TARGET_SUPPORT:
            frequent.append(s)
            supports.append(support)

    return frequent,supports

def generatePossibleItemsets(items, frequent):
    itemsets = []
    for s in frequent:
        itemsets.extend([list(set([i]) | set(s)) for i in items if i not in s])
    return itemsets

# Returns float value of the support
def getSupport(transactions,itemset):
    ct = 0

    for t in transactions:
        if itemset.issubset(set(t)):
            ct+=1

    return (ct / len(transactions))


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

def initCLI():
    # load dataset filename
    global DATASET
    if len(sys.argv) > 1: DATASET = sys.argv[1]

    # load mininmum support
    global TARGET_SUPPORT
    if len(sys.argv) > 4: TARGET_SUPPORT = float(sys.argv[2])

    # load minimum confidence
    global TARGET_CONFIDENCE
    if len(sys.argv) > 4: TARGET_CONFIDENCE = float(sys.argv[3])

if __name__ == '__main__':
    if len(sys.argv) > 1: DATASET = sys.argv[1]
    if len(sys.argv) > 2: TARGET_SUPPORT = float(sys.argv[2])
    if len(sys.argv) > 3: TARGET_CONFIDENCE = float(sys.argv[3])
    sys.exit(main())
