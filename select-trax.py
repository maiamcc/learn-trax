#!/usr/bin/env python

import argparse
import os
from typing import List, Optional

from mido import MidiFile

import trax
import utils


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_mid',
        type=str,
        help='path to base midi file'
    )
    parser.add_argument(
        'outfile',
        type=str,
        help='base name of outfile: <outfile>.mid. (In --auto mode, this will just be the prefix.)'
    )
    parser.add_argument(
        'track_names',
        type=str,
        help='comma-separated list of track names to foreground (case-insensitive)'
    )
    parser.add_argument(
        '--output_dir', '-o',
        type=str,
        help='directory in which to output tracks (may be absolute, or relative to directory of input_mid). By default, tracks are saved to the same directory as input_mid.'
    )
    parser.add_argument(
        '--auto', '-a',
        action='store_true',
        help='automatically try to make s1, s2 etc. tracks according to my usual naming conventions'
    )

    return parser


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()

    if args.auto:
        trax.auto_select_trax(input_mid=args.input_mid,
                  base_outfile=args.outfile,
                  output_dir=args.output_dir
                 )
    else:
        trax.select_trax(
            input_mid=args.input_mid,
            outfile=args.outfile,
            track_names=args.track_names.split(","),
            output_dir=args.output_dir,
        )
