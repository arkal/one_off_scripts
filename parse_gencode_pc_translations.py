#!/usr/bin/env python2.7
from __future__ import print_function

import argparse
import os


def read_fasta(input_file):
    """
    This module will accept an input fasta and yield individual sequences
    one at a time.
    """
    first_seq = True
    id = None
    seq = None
    for line in input_file:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith('>'):
            if first_seq:
                first_seq = False
            else:
                if id[1].endswith('_PAR_Y'):
                    pass
                else:
                    yield '>' + ('|'.join(id)), seq
            id = line[1:].split('|')
            seq = ''
        else:
            seq += line
    if not id[1].endswith('_PAR_Y'):
        yield '>' + ('|'.join(id)), seq


def main():
    """
    This is the main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('gencode_file', help='Gencode PS translations file.',
                        type=str)
    params = parser.parse_args()

    params.gencode_file = os.path.abspath(os.path.expanduser(params.gencode_file))
    assert os.path.exists(params.gencode_file)
    outfile_name = os.path.splitext(params.gencode_file)
    outfile_name = ''.join([outfile_name[0], '_NOPARY', outfile_name[1]])
    with open(params.gencode_file, 'r') as infile, open(outfile_name, 'w') as outfile:
        for id, seq in read_fasta(infile):
            print(id, seq, sep='\n', file=outfile)

if __name__ == '__main__':
    main()
