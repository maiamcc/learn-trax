import os
import typing as t

from mido import MidiFile

import utils


def tracks_for_file(input_mid: str,
                    output_dir: t.Optional[str] = None,
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

        if not output_dir:
            # by default, output files to the same directory as the input mid
            output_dir = directory
        elif not os.path.isabs(output_dir):
            # if output_dir isn't an absolute path, it's assumed relative to directory of the input mid
            output_dir = os.path.join(directory, output_dir)
        # otherwise, it's just an absolute path

        outfile_name = '{}-{}'.format(prefix, voice)
        outfile_path = os.path.join(output_dir, outfile_name)
        print('making practice track for voice: {}'.format(voice))
        utils.practice_track_at_index(mid.ticks_per_beat, voice_tracks,
                                      utils.meta_track_with_title(meta_track, outfile_name),
                                      outfile_path, i)
