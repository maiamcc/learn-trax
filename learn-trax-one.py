#!/usr/bin/env python

import argparse

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
        'outfile',
        type=str,
        help='base name of outfile: <outfile>.mid'
    )
    parser.add_argument(
        'track_names',
        type=str,
        help='comma-separated list of track names to foreground (case-insensitive)'
    )

    return parser


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()

    mid = MidiFile(args.input_mid)

    # idk how consistent this is but sib-generated midis, first track is just metadata
    meta_track, voice_tracks = utils.cleaned_meta_and_voice_tracks(mid)
    names = utils.ordered_track_names(voice_tracks)
    requested = [r.lower() for r in args.track_names.split(",")]

    indices = []
    for req in requested:
        try:
            i = names.index(req)
        except ValueError:
            raise Exception("Couldn't find track with name: '{}'. (Known names: {})".
                            format(req, ", ".join(names)))
        indices.append(i)

    utils.practice_track_with_foregrounds(mid.ticks_per_beat, voice_tracks, meta_track, args.outfile, indices)
