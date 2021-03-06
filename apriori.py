#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import itertools
import sys
import csv
import os

TARGET_CONFIDENCE = 0.20
TARGET_SUPPORT = 0.20
DATASET = 'INTEGRATED-DATASET.csv'

scriptdir = os.path.dirname(os.path.realpath(__file__))

def main():

    # read config values from command line
    initCLI()

    # load data into application
    curated_csv = os.path.join(scriptdir, DATASET)

    print ("Loading data ...")
    with open(curated_csv,'r') as f:
        raw = f.read()

    print ("Processing ... ")
    transactions = []
    items = set()
    for t in raw.split('\n')[:-1]: # don't include last line (which is just an empty string)
        new_itemset = set(map(str.strip,t.split(',')))
        transactions.append(new_itemset)
        items |= new_itemset

    # This will keep track of frequent itemsets of each size (size-1 = index)
    frequent, frequent_supports, rules, confidences, rule_supports = [], [], [], [], []

    # The initial set is a bit different from the subsequent ones
    initial_frequent, initial_supports = getInitialFrequentItems(transactions,items)
    frequent.extend(initial_frequent)
    frequent_supports.extend(initial_supports)

    # We only care about frequent items!
    items = set([x[0] for x in initial_frequent])

    # Iterate over the set that is left looking for relations
    set_size = 2
    cont = True
    previous_frequent = initial_frequent
    while cont:

        # Trim possible items
        items = trimItems(previous_frequent)

        # Generate possible itemsets of this size
        possible_itemsets = generatePossibleItemsets(items, previous_frequent)

        # Generate new frequent itemsets of this size and their supports
        new_frequent, new_supports = getFrequentItemsets(items, transactions, possible_itemsets, set_size)
        frequent.extend(new_frequent)
        frequent_supports.extend(new_supports)
        previous_frequent = new_frequent

        # Generate high-confidence association rules
        new_rules, new_confidences, new_rule_supports = getAssociationRules(new_frequent, new_supports, transactions)
        rules.extend(new_rules)
        confidences.extend(new_confidences)
        rule_supports.extend(new_rule_supports)

        # Continue?
        cont = len(new_frequent) > 0
        set_size += 1

    # Print
    printFrequentItemsets(frequent,frequent_supports)
    if len(rules) > 0:
        printAssociationRules(rules, confidences, rule_supports)

    print('done')

# Print confidence and support percentages
def printAssociationRules(rules, confs, supps):
    if (TARGET_CONFIDENCE * 100).is_integer():
        log('==High-confidence association rules (min_conf={0}%)'.format(int(TARGET_CONFIDENCE*100)))
    else:
        log('==High-confidence association rules (min_conf={0}%)'.format(TARGET_CONFIDENCE*100))

    for c,s,r in sorted(zip(confs,supps,rules), reverse=True):
        log(str(r[0]) + ' => ' + str([r[1]]) + (' (Conf: %.2f' % (c*100)) + '%, ' + ('Supp: %.2f' % (s*100)) + '%)')

# Trim the overall item sets
def trimItems(itemsets):
    items = set()
    for s in itemsets:
        items |= set(s)
    return items

# Filter matches based on percent targets
def getAssociationRules(frequent, supports, transactions):
    new_rules,new_confidences,new_supports = [], [], []
    for f,s in zip(frequent,supports):
        for i in f:
            conf = getConfidence(set(f)-set([i]),i,transactions)
            if conf >= TARGET_CONFIDENCE:
                new_rules.append([list(set(f)-set([i])),i])
                new_confidences.append(conf)
                new_supports.append(s)

    return new_rules, new_confidences, new_supports

# Compute target
def getConfidence(s,i,transactions):
    ct_s_i, ct_s = 0, 0
    for t in transactions:
        if s.issubset(set(t)):
            ct_s += 1
            if i in t:
                ct_s_i += 1
    return float(ct_s_i) / ct_s

# Print item sets and stats
def printFrequentItemsets(frequent,supports):
    if (TARGET_SUPPORT * 100).is_integer():
        log('==Frequent itemsets (min_sup={0}%)'.format(int(TARGET_SUPPORT * 100)) )
    else:
        log('==Frequent itemsets (min_sup={0}%)'.format(TARGET_SUPPORT * 100) )
    for s,f in sorted(zip(supports,frequent), reverse=True):
        log(str(f) + ", %.2f" % (s*100) + '%')

# Item set choosing
def generatePossibleItemsets(items, frequent):
    possible_itemsets = []
    for s in frequent:
        # Grab new item sets
        possible_itemsets.extend([list(set([i]) | set(s)) for i in items if i not in s])
    possible_itemsets.sort()

    # Use inference logic to further limit set (as to 2.1.1)
    pruned = []
    for itemset in possible_itemsets:
        valid = True

        for removed_item in itemset:
            subset = set(itemset) - set([removed_item])

            if list(subset) not in frequent:
                valid=False
                break

        if valid:
            pruned.append(itemset)

    # Make sure there are no duplicates
    pruned = deduplicate(pruned)

    return pruned

# De-duplicate a list of lists
def deduplicate(a):
    deduped = []
    seen = set()
    for t in a:
        s = frozenset(t)
        if s not in seen:
            seen.add(s)
            deduped.append(t)
    return deduped


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

    return frequent, supports

# returns list of frequent itemsets of the given size
def getFrequentItemsets(items,transactions,possible_itemsets,set_size):
    frequent = []
    supports = []

    # Loop through possible itemsets
    for s in possible_itemsets:

        # Record itemset if it passes support threshold
        support = getSupport(transactions, set(s))

        if support >= TARGET_SUPPORT:
            frequent.append(s)
            supports.append(support)

    return frequent,supports

# Returns float value of the support
def getSupport(transactions,itemset):
    ct = 0

    for t in transactions:
        if itemset.issubset(set(t)):
            ct+=1

    return (ct / len(transactions))

# logging function: prints out to file in addition to system if specified
def log(s):
    print(s)
    with open('output.txt','a') as t:
        t.write(s + "\n")

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

    # printout
    open('output.txt','w')
    log ("Dataset:                 " + DATASET)
    log ("Target Confidence:       {0}%".format(int(TARGET_CONFIDENCE * 100)))
    log ("Target Support:          {0}%".format(int(TARGET_SUPPORT * 100)))

if __name__ == '__main__':
    if len(sys.argv) > 1: DATASET = sys.argv[1]
    if len(sys.argv) > 2: TARGET_SUPPORT = float(sys.argv[2])
    if len(sys.argv) > 3: TARGET_CONFIDENCE = float(sys.argv[3])
    sys.exit(main())
