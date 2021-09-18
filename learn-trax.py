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
        'file_prefix',
        type=str,
        help='prefix for outfiles: <prefix>-alto.mid'
    )
    parser.add_argument(
        'voice_parts',
        type=str,
        help='comma-separated list of voice parts to be used for naming files: fair-phyllis-<sop>.wav'
    )
    parser.add_argument(
        '--mid',
        type=bool,
        default=False,
        help='if true, output tracks as .mid files. By default, will be .wav files.'
    )

    return parser


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()

    as_wav = not args.mid

    voice_parts = args.voice_parts.split(',')

    mid = MidiFile(args.input_mid)

    # TODO: make all tracks same instrument?

    # idk how consistent this is but sib-generated midis, first track is just metadata
    meta_track, voice_tracks = utils.cleaned_meta_and_voice_tracks(mid)

    for i in range(len(voice_tracks)):
        # TODO: derive filename (and path?) from infile
        base_filename = '{}-{}'.format(args.file_prefix, voice_parts[i])
        print('making practice track {} at index: {}'.format(base_filename, i))
        utils.practice_track_at_index(mid.ticks_per_beat, voice_tracks, meta_track.copy(), base_filename, i, as_wav, True)
