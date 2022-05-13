import argparse
import os
import typing as t

from mido import MidiFile

import utils


def tracks_for_file(input_mid: str,
                    ignore_voices: t.Optional[t.Set[str]] = None,
                    voices: t.Optional[t.List[str]] = None,
                    prefix: t.Optional[str] = None):
    mid = MidiFile(input_mid)
    meta_track, voice_tracks = utils.cleaned_meta_and_voice_tracks(mid)

    track_names = [trk.name.lower().replace(' ', '') for trk in voice_tracks]
    voices = voices if voices else track_names
    if len(voices) != len(voice_tracks):
        raise ValueError('Invalid number of voices passed, does not align with number of tracks!'
            '\n\tVoices passed: {}\n\tTrack names: {}'.
            format(voices, track_names))
    ignore_voices = ignore_voices if ignore_voices else set()

    directory, filename = os.path.split(input_mid)
    prefix = prefix if prefix else os.path.splitext(filename)[0]

    for i in range(len(voice_tracks)):
        voice = voices[i]
        if voice.lower() in ignore_voices:
            print('(ignoring track for {}...)'.format(voice))
            continue

        base_filename = os.path.join(directory, '{}-{}'.format(prefix, voice))
        print('making practice track for voice: {}'.format(voice))
        utils.practice_track_at_index(mid.ticks_per_beat, voice_tracks, meta_track.copy(), base_filename, i)
