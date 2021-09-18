# Learn Trax

Make learning tracks from midi files! `learn-trax` will take your input midi file and create a learning track for each voice by adjusting the pan and volume to foreground the voice in question.

## Setup
1. Python requirements: `pip install -r requirements.txt`
2. If converting to `.wav`, you need [FluidSynth](https://www.fluidsynth.org/):
	a. `brew install fluidsynth`
	b. put a good soundfont at `~/.fluidsynth/default_sound_font.sf2` (I use [GeneralUser GS](http://www.schristiancollins.com/generaluser.php))

## Usage
```
./learn-trax.py locus-iste.mid locus sop,alto,tenor,bass
```
From input track `locus-iste.mid`, produce tracks `locus-sop.wav`, `locus-alto.wav`, etc. (the names provided are for the 1st/2nd/3rd/4th instruments in the midi file, respectively).

To output as `.mid` files instead of `.wav` (much faster and doesn't require FluidSynth setup), pass `--mid`.

## Limitations/TODOs
* ideally, you could set the volume/pan adjustment via the CLI (right now they're constant)
* ideally, this could change instruments for you:
	* turn all of the tracks into the same, inoffensive instrument (probably piano -- depending on the soundfont, midi choir sounds awful)
	* turn the foregrounded track into a different instrument for maximum contrast
* option to also `.wav`-ify the input track
* `learn-trax` strips the first midi track because for Sibelius-generated midi files (what I am working with), this is always metadata. Is this true of all midi files? I don't actually know! 🙃
* generated learn trax should be outputted to the same directory as the infile
* should be able to auto-detect file prefix from infile, e.g. "hallelujah-chorus.mid" should generate "hallelujah-chorus-sop.wav" etc. without user intervention
* wish we could output `.mp3` instead of `.wav` but I'm too lazy to figure that out right now
