#!/usr/bin/env python

import argparse
import os.path
import typing as t

from mido import MidiFile

import trax


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_mid',
        type=str,
        help='path to base midi file'
    )
    parser.add_argument(
        '--output_dir', '-o',
        type=str,
        help='directory in which to output tracks (may be absolute, or relative to directory of input_mid). By default, tracks are saved to the same directory as input_mid.'
    )
    parser.add_argument(
        '--ignore', '-X',
        type=str,
        help='comma-separated list of track names to IGNORE, i.e. not to create a foregrounded track for. Case insensitive.'
    )
    parser.add_argument(
        '--voices', '-v',
        type=str,
        help='comma-separated list of voice parts to be used for naming files: fair-phyllis-<sop>.mid. (By default, use track name.)'
    )
    parser.add_argument(
        '--prefix', '-p',
        type=str,
        help='prefix for outfiles: <prefix>-alto.mid'
    )

    return parser

if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()

    trax.tracks_for_file(args.input_mid,
                    output_dir = args.output_dir,
                    ignore_voices = args.ignore.split(',') if args.ignore else None,
                    voices = args.voices.split(',') if args.voices else None,
                    prefix = args.prefix
    )
