#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__copyright__ = """

    Copyright 2018 Dictanova

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

import csv
import sys
import json
import logging
import argparse

from collections import defaultdict
from scipy.stats import rankdata

def main():
    parser = argparse.ArgumentParser(description='Evaluates bilingual term alignment')
    parser.add_argument('gold_standard', help='The gold standard file for evaluation (json)')
    parser.add_argument('result_file', help='The result file (tsv)')

    args = parser.parse_args()

    source2target = read_gold_standard(args.gold_standard)
    result_index = read_result(args.result_file, source2target)
    result2rank = rank_results(result_index, source2target)

    total_terms = len(source2target)
    terms_found = len(result2rank)

    MAP = max_precision(result2rank, total_terms)
    print('MAP\t{:.4f} '.format(MAP))

    # Accuracy is precision@1
    accuracy = sum(1.0 for ranks in result2rank.values() if 1 in ranks) / total_terms
    print('accu.\t{0:.4f}'.format(accuracy))

    # Display precision at cut off ranks
    prec_at_n = precision_ranges(result2rank, total_terms)
    for cutoff in [5, 10, 15, 20, 30, 100, 200, 500, 1000]:
        print('P_{:<4}\t{:.4f}'.format(cutoff, prec_at_n[cutoff]))

    all_prec = float(terms_found) / total_terms
    print('all\t{:.4f}'.format(all_prec))


def read_gold_standard(json_path):
    """Reads the reference list from a json file

    Args:
        json_path: The path to the json file containing the gold reference list.

    Returns:
        A dict of source to target terms as a set.

    """
    with open(json_path) as gs:
        data = json.load(gs)
        return {key: val for key, val in map(lambda t: [t['source'], set(t['targets'])], data['terms'])}

def read_result(result_file, source2target):
    """Reads the result file while filtering results by terms in the gold standard list

    Args:
        result_file:   The file path (in tsv format).
        source2target: The dict containing the reference list.

    Returns:
        A dict of source to candidate tuples (candidate, score).

    """
    result_index = defaultdict(lambda: [])
   
    with open(result_file) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        for row in tsvreader: 
            source = row[0]
            target = row[1]
            score = float(row[2])

            if source in source2target:
                result_index[source].append((target, score))
            else:
                logging.warning('Source term "%s" not found in the gold standard' % source)

    return result_index

def rank_results(result_index, source2target):
    """Ranks good translations amongts candidates

    Args:
        result_index:  A dict of term to candidate tuples
        source2target: The dict containing the reference list.

    Returns:
        A dict of source to ranks of good translations in ascending sorted order

    """
    result2rank = defaultdict(lambda: [])
    for term, targets in result_index.items():
        ranked = sorted(targets, key=lambda tup: tup[1], reverse=True)
        ranks = rankdata([t[1] for t in ranked], method='min').tolist()
        ranks.reverse()
        for index, target in enumerate(ranked):
            if target[0] in source2target[term]:
                result2rank[term].append(ranks[index])
    return result2rank

def precision_ranges(result2rank, total_terms):
    """Computes precision at standard cutoff ranks: [5, 10, 15, 20, 30, 100, 200, 500, 1000]

    Args:
        result2rank: A dict of source to ranks of good translation candidates.
        total_terms: The expected term count.

    Returns:
        A dict containing a precision value for each cutoff rank

    """
    map_of_prec = dict()
    for cutoff in [5, 10, 15, 20, 30, 100, 200, 500, 1000]:
        map_of_prec[cutoff] = sum(1.0 for ranks in result2rank.values() if len([r for r in ranks if r <= cutoff]) > 0) / total_terms
    return map_of_prec

def max_precision(term2rank, total_terms):
    """Computes the MAP (max average precision) over the whole candidate list

    Args:
        result2rank: A dict of source to ranks of good translation candidates.
        total_terms: The expected term count.

    Returns:
        A dict containing a precision value for each cutoff rank

    """
    term2prec = dict()
    for term, ranks in term2rank.items():
        term2prec[term] = 1.0 / min(term2rank[term])            
    return sum(term2prec.values()) / total_terms
    
    
if __name__ == '__main__':
    main()
