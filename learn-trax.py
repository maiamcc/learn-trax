#!/usr/bin/env python

import argparse
import os.path

from mido import MidiFile

import utils


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_mid',
        type=str,
        help='path to base midi file'
    )
    parser.add_argument(
        'voice_parts',
        type=str,
        help='comma-separated list of voice parts to be used for naming files: fair-phyllis-<sop>.wav'
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

    voice_parts = args.voice_parts.split(',')

    mid = MidiFile(args.input_mid)

    # TODO: make all tracks same instrument?

    directory, filename = os.path.split(args.input_mid)
    prefix = args.prefix if args.prefix else os.path.splitext(filename)[0]

    # idk how consistent this is but sib-generated midis, first track is just metadata
    meta_track, voice_tracks = utils.cleaned_meta_and_voice_tracks(mid)

    for i in range(len(voice_tracks)):
        # TODO: derive filename (and path?) from infile
        base_filename = os.path.join(directory, '{}-{}'.format(prefix, voice_parts[i]))
        print('making practice track {} at index: {}'.format(base_filename, i))
        utils.practice_track_at_index(mid.ticks_per_beat, voice_tracks, meta_track.copy(), base_filename, i)
