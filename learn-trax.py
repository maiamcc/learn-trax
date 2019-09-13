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

from mido import MidiFile
mid = MidiFile('si-chio-full.mid')

# TODO: make all tracks same instrument?

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