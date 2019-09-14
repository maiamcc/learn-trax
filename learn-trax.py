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
from typing import List

from mido import MidiFile
from mido.midifiles.tracks import MidiTrack
from mido.messages.messages import Message

VOL_CONTROL = 7
PAN_CONTROL = 10


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_mid',
        type=str,
        help='path to base midi file'
    )

    return parser


def rm_volume_and_pan_set(track: MidiTrack):
    return MidiTrack([msg for msg in track if not is_vol_control_or_pan_control(msg)])


def is_vol_control_or_pan_control(msg: Message) -> bool:
    return msg.type == 'control_change' and msg.control in [VOL_CONTROL, PAN_CONTROL]


def foreground_track_at_index(tracks: List[MidiTrack], i: int) -> List[MidiTrack]:
    pass


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()

    mid = MidiFile(args.input_mid)

    # TODO: make all tracks same instrument?

    # idk how consistent this is but sib-generated midis, first track is just metadata
    tracks = mid.tracks[1:]


"""
instrument_tracks = [t for t in mid.tracks if not_meta(t)]
for t in instrument_tracks:
    remove_vol_control(t)
    remote_pan_control(t)

foreground_index = 2  # TODO: one midi object per track-to-foreground
for i, t in enumerate(instrument_tracks):
    if i == foreground_index:
        make_foreground(t)
        continue
    make_background(t)

# TODO: convert to mp3
mid.save('out.mid')
"""