#!/usr/bin/env python

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
from typing import List

from mido import MidiFile
from mido.midifiles.tracks import MidiTrack
from mido.messages.messages import Message

VOL_CONTROL = 7
PAN_CONTROL = 10

VOL_BACKGROUND = 55
VOL_FOREGROUND = 120

PAN_BACKGROUND = 56
PAN_FOREGROUND = 76


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_mid',
        type=str,
        help='path to base midi file'
    )

    return parser


def rm_volume_and_pan_set(track: MidiTrack) -> MidiTrack:
    return MidiTrack([msg for msg in track if not is_vol_control_or_pan_control(msg)])


def is_vol_control_or_pan_control(msg: Message) -> bool:
    return msg.type == 'control_change' and msg.control in [VOL_CONTROL, PAN_CONTROL]


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


def foreground_track_at_index(tracks: List[MidiTrack], index: int) -> List[MidiTrack]:
    ret = []
    for i, trk in enumerate(tracks):
        if i == index:
            ret.append(foreground(trk))
        else:
            ret.append(background(trk))
    return ret


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()

    mid = MidiFile(args.input_mid)

    # TODO: make all tracks same instrument?

    # idk how consistent this is but sib-generated midis, first track is just metadata
    meta_track = mid.tracks[0]
    tracks = [rm_volume_and_pan_set(t) for t in mid.tracks[1:]]

    alto_tracks = foreground_track_at_index(tracks, 2)

    outfile = MidiFile(ticks_per_beat=mid.ticks_per_beat)
    outfile.tracks = [meta_track.copy()] + alto_tracks
    outfile.save('alto.mid')