import os
import typing as t

from mido import MidiFile

import utils


STANDARD_VOICES = ['soprano', 'alto', 'tenor', 'bass']


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


def select_trax(input_mid: str, outfile: str,
                track_names: t.List[str],
                output_dir: t.Optional[str]=None):
    """
    Make a practice track with MULTIPLE selected tracks foregrounded.

    e.g. if you have the common soprano notes in the `soprano` instrument
    and splits broken into the `s1` and `s2` tracks, you might want a
    practice track for the s2s that foregrounds `soprano` + `s2.
    """

    print(f'*** voices {track_names} -> file {outfile}')

    mid = MidiFile(input_mid)

    # idk how consistent this is but sib-generated midis, first track is just metadata
    meta_track, voice_tracks = utils.cleaned_meta_and_voice_tracks(mid)
    names = utils.ordered_track_names(voice_tracks)
    requested = [r.lower() for r in track_names]

    indices = []
    for req in requested:
        try:
            i = names.index(req)
        except ValueError:
            raise utils.TrackNotFoundException(req, names)
        indices.append(i)


    directory, filename = os.path.split(input_mid)
    if not output_dir:
        # by default, output files to the same directory as the input mid
        output_dir = directory
    elif not os.path.isabs(output_dir):
        # if output_dir isn't an absolute path, it's assumed relative to directory of the input mid
        output_dir = os.path.join(directory, output_dir)
    # otherwise, it's just an absolute path

    outfile_path = os.path.join(output_dir, outfile)
    utils.practice_track_with_foregrounds(mid.ticks_per_beat, voice_tracks, meta_track, outfile_path, indices)


def auto_select_trax(input_mid: str, base_outfile: str,
              output_dir: t.Optional[str]=None):
    """
    I (Maia) commonly structure my midis like:
        - common soprano notes in the `soprano` instrument
        - splits broken into the `s1` and `s2` tracks

    This fn attempts to make practice tracks for all split parts
    (s1, s2, a1...) if indicated by track structure; if a part isn't
    indicated to have splits, it just makes a track for that part
    (soprano, alto...)

    Relies on the track naming scheme matching exactly.
    """
    mid = MidiFile(input_mid)
    _, voice_tracks = utils.cleaned_meta_and_voice_tracks(mid)
    existing_tracks = utils.ordered_track_names(voice_tracks)

    # if we don't have the minimum recognized track names,
    # this won't work--just normally practice-track-ify it.
    if not all([v in existing_tracks for v in STANDARD_VOICES]):
        print(f'===== Didn\'t find expected tracks in {os.path.basename(input_mid)} so can\'t be fancy, just doing a normal one')
        tracks_for_file(input_mid,
            output_dir=output_dir,
        )
        return

    for voice in STANDARD_VOICES:
        # check if there are splits in this part, e.g.
        #   if a track 's1' exists, there are sop splits
        if voice[0]+'1' in existing_tracks:
            # there are splits, do some part combinations!
            for split in [f'{voice[0]}{n}' for n in range(1,3)]:
                outfile = f'{base_outfile}-{split}'
                select_trax(
                    input_mid=input_mid,
                    outfile=outfile,
                    track_names=[voice, split],
                    output_dir=output_dir,
                )
        else:
            # there are no splits, just make a practice track
            # for the voice we've currently got.
            outfile = f'{base_outfile}-{voice}'
            select_trax(
                input_mid=input_mid,
                outfile=outfile,
                track_names=[voice],
                output_dir=output_dir,
            )

