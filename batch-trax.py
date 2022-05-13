#!/usr/bin/env python

import argparse
import os
import os.path

from mido import MidiFile

import trax


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_dir',
        type=str,
        help='directory to process'
    )
    parser.add_argument(
        '--ignore', '-X',
        type=str,
        help='comma-separated list of track names to IGNORE, i.e. not to create a foregrounded track for. Case insensitive.'
    )
    return parser


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()

    midi_files = sorted([filename for filename in os.listdir(args.input_dir) if filename.endswith('.mid')])
    print('Will process {} midi files...'.format(len(midi_files)))
    print()

    for file in midi_files:
        print('+ {}'.format(file))
        trax.tracks_for_file(os.path.join(args.input_dir, file),
            ignore_voices = args.ignore.split(',') if args.ignore else None
        )
        print()
