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
        '--voices', '-v',
        type=str,
        help='comma-separated list of voice parts to be used for naming files: fair-phyllis-<sop>.mid. (By default, use track name.)'
    )
    parser.add_argument(
        '--ignore', '-X',
        type=str,
        help='comma-separated list of track names to IGNORE, i.e. not to create a foregrounded track for. Case insensitive.'
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

    mid = MidiFile(args.input_mid)

    ignore_voices = set([ignore.lower() for ignore in args.ignore.split(',')])

    directory, filename = os.path.split(args.input_mid)
    prefix = args.prefix if args.prefix else os.path.splitext(filename)[0]

    # idk how consistent this is but sib-generated midis, first track is just metadata
    meta_track, voice_tracks = utils.cleaned_meta_and_voice_tracks(mid)

    track_names = [trk.name.lower().replace(' ', '') for trk in voice_tracks]
    voices = args.voices.split(',') if args.voices else track_names
    if len(voices) != len(voice_tracks):
        raise ValueError('Invalid number of voices passed, does not align with number of tracks!'
            '\n\tVoices passed: {}\n\tTrack names: {}'.
            format(voices, track_names))

    for i in range(len(voice_tracks)):
        voice = voices[i]
        if voice.lower() in ignore_voices:
            print('(ignoring track for {}...)'.format(voice))
            continue

        base_filename = os.path.join(directory, '{}-{}'.format(prefix, voice))
        print('making practice track for voice: {}'.format(voice))
        utils.practice_track_at_index(mid.ticks_per_beat, voice_tracks, meta_track.copy(), base_filename, i)
