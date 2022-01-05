# Learn Trax

Make learning tracks from midi files! `learn-trax` will take your input midi file and create a learning track for each voice by adjusting the pan and volume to foreground the voice in question.

## Setup
Python requirements: `pip install -r requirements.txt`

## Usage
```
./learn-trax.py locus-iste.mid locus sop,alto,tenor,bass
```
From input track `locus-iste.mid`, produce tracks `locus-sop.mid`, `locus-alto.mid`, etc. (the names provided are for the 1st/2nd/3rd/4th instruments in the midi file, respectively).


## Limitations/TODOs
* ideally, you could set the volume/pan adjustment via the CLI (right now they're constant)
* ideally, this could change instruments for you:
	* turn all of the tracks into the same, inoffensive instrument
	* turn the foregrounded track into a different instrument for maximum contrast
* option to output audio files (`.wav`, `.mp3`, etc.) instead of/in addition to `.mid` files
	* I tried this using FluidSynth but it was a pain and the generated `.wav` files didn't seem to respect my volume and pan settings from the midi? See branch: [`wav-output`](https://github.com/maiamcc/learn-trax/tree/wav-output)
* `learn-trax` strips the first midi track because for Sibelius-generated midi files (what I am working with), this is always metadata. Is this true of all midi files? I don't actually know! 🙃
* generated learn trax should be outputted to the same directory as the infile
* should be able to auto-detect file prefix from infile, e.g. "hallelujah-chorus.mid" should generate "hallelujah-chorus-sop.wav" etc. without user intervention
