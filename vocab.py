#!usr/bin/env python

# CLI Vocab Trainer for Russian Vocabulary
# Just showing the word and asking what it means etc.

# For German to Russian, just show the word and then the rest
# Russian to German: Randomly pick complete or incomplete aspect

# When clearing up, show the entire row

import csv

def read_csv(fname, delimiter=';', encoding='utf-8'):
    """Reads in vocabulary from custom csv file and returns as list"""

    vocab = []

    with open(fname, newline='', encoding=encoding) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=delimiter)
        for row in csvreader:
            vocab.append(row)
    return vocab


def main():
    print(read_csv('vocab.csv'))

if __name__ == '__main__':
    main()
    
