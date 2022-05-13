#!/usr/bin/env python

import argparse
from datetime import datetime
import os
import os.path

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

    input_dir = args.input_dir

    midi_files = sorted([filename for filename in os.listdir(input_dir) if filename.endswith('.mid')])
    if not midi_files:
        raise Exception('No midi files found, sorry :-/')

    output_dir = os.path.join(input_dir, 'learntrax_{}'.format(datetime.now().strftime("%Y%m%d%H%M%S")))
    os.mkdir(output_dir)

    print('Will process {} midi files to directory: {}'.format(len(midi_files), output_dir))
    print()

    for file in midi_files:
        print('+ {}'.format(file))
        trax.tracks_for_file(os.path.join(args.input_dir, file),
            output_dir=output_dir,
            ignore_voices = args.ignore.split(',') if args.ignore else None
        )
        print()
