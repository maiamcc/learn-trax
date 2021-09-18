### PAN
# background: control_change channel=0 control=10 value=56 time=0
# foreground: control_change channel=0 control=10 value=76 time=0

### VOLUME
# background: control_change channel=0 control=7 value=55 time=0
# foreground: control_change channel=0 control=7 value=120 time=0

# e.g. background
# >>> soptrack[4] = soptrack[4].copy(value=56)
# >>> soptrack[5] = soptrack[5].copy(value=55)

# e.g. foreground
# >>> basstrack[4] = basstrack[4].copy(value=76)
# >>> basstrack[5] = basstrack[5].copy(value=120)

import argparse
from copy import deepcopy
import os
from typing import List

from midi2audio import FluidSynth
from mido import MidiFile
from mido.midifiles.tracks import MidiTrack
from mido.messages.messages import Message
from mido.midifiles.meta import MetaMessage

VOL_CONTROL = 7
PAN_CONTROL = 10

VOL_BACKGROUND = 55
VOL_FOREGROUND = 120

PAN_BACKGROUND = 56
PAN_FOREGROUND = 76

FS = FluidSynth()

def rm_volume_and_pan_set(track: MidiTrack) -> MidiTrack:
    return MidiTrack([msg for msg in track if not is_vol_control_or_pan_control(msg)])


def is_vol_control_or_pan_control(msg: Message) -> bool:
    return msg.type == 'control_change' and msg.control in [VOL_CONTROL, PAN_CONTROL]


def cleaned_meta_and_voice_tracks(mid: MidiFile) -> (MidiTrack, List[MidiTrack]):
    # idk how consistent this is but sib-generated midis, first track is just metadata
    meta_track = mid.tracks[0]

    # TODO: make all tracks same instrument?
    voice_tracks = [rm_volume_and_pan_set(t) for t in mid.tracks[1:]]

    return meta_track, voice_tracks


def vol_background() -> Message:
    return Message('control_change', control=VOL_CONTROL, value=VOL_BACKGROUND)


def vol_foreground() -> Message:
    return Message('control_change', control=VOL_CONTROL, value=VOL_FOREGROUND)


def pan_background() -> Message:
    return Message('control_change', control=PAN_CONTROL, value=PAN_BACKGROUND)


def pan_foreground() -> Message:
    return Message('control_change', control=PAN_CONTROL, value=PAN_FOREGROUND)


def foreground(track: MidiTrack) -> MidiTrack:
    ret = deepcopy(track)  # can i use track.copy() for this?
    ret.insert(1, vol_foreground())
    ret.insert(1, pan_foreground())
    return ret


def background(track: MidiTrack) -> MidiTrack:
    ret = deepcopy(track)  # can i use track.copy() for this?
    ret.insert(1, vol_background())
    ret.insert(1, pan_background())
    return ret


def foreground_tracks_at_indices(tracks: List[MidiTrack], indices: List[int]) -> List[MidiTrack]:
    ret = []
    for i, trk in enumerate(tracks):
        if i in indices:
            ret.append(foreground(trk))
        else:
            ret.append(background(trk))
    return ret


def practice_track_at_index(tpb: int, voice_tracks: List[MidiTrack], meta_track: MidiTrack, base_filename: str, i: int, as_wav=False, clean_up=True):
    practice_track_with_foregrounds(tpb, voice_tracks, meta_track, base_filename, [i], as_wav, clean_up)


def practice_track_with_foregrounds(tpb: int, voice_tracks: List[MidiTrack], meta_track: MidiTrack, base_filename: str, indices: List[int], as_wav=False, clean_up=True):
    mid_name = '{}.mid'.format(base_filename)
    wav_name = '{}.wav'.format(base_filename)

    adjusted_tracks = foreground_tracks_at_indices(voice_tracks, indices)

    outfile = MidiFile(ticks_per_beat=tpb)
    outfile.tracks = [meta_track] + adjusted_tracks

    # TODO: save to same directory as infile
    outfile.save(mid_name)
    if as_wav:
        # TODO: suppress FluidSynth stdout/stderr
        FS.midi_to_audio(mid_name, wav_name)
        if clean_up:
            os.remove(mid_name)


def ordered_track_names(tracks: List[MidiTrack]) -> List[str]:
    names = []
    for i, t in enumerate(tracks):
        names.append(track_name(t))
    return names


def track_name(t: MidiTrack) -> str:
    for msg in t:
        if isinstance(msg, MetaMessage) and msg.name:
            return msg.name.lower()
    raise Exception("No name found for track!")
