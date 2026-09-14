# Learn Trax

Make learning tracks from midi files! `learn-trax` will take your input midi file and create a learning track for each voice by adjusting the pan and volume to foreground the voice in question.

## Setup
Python requirements: `pip install -r requirements.txt`

## Usage
### Single file at a time
```
./learn-trax.py locus-iste.mid
```
If your midi instrument names are Soprano, Alto, Tenor, and Bass, produce tracks `locus-iste-soprano.mid`, `locus-iste-alto.mid`, etc.

```
./learn-trax.py locus-iste.mid --prefix locus --voices sop,alto,tenor,bass
```
From input track `locus-iste.mid`, produce tracks `locus-sop.mid`, `locus-alto.mid`, etc. (the names provided are for the 1st/2nd/3rd/4th instruments in the midi file, respectively).

```
./learn-trax.py stanford-bluebird.mid --ignore solo,piano
```

Produces tracks `stanford-bluebird-soprano.mid` etc., _not_ producing practice tracks for the midi tracks named Solo or Piano.

### From directory / batched
```
./batch-trax.py ~/Documents/fall_season/midi
```
Produces practice tracks (passing through any provided arguments) for any `.mid` file in the given directory.

### Via YAML config
```
./yaml-trax.py path/to/some/input.yaml
```
Makes practice tracks according to the configuration given in the yaml file, which might look like:
```yaml
fair:  # will be used as file name prefix
    input_mid: '/my/midis/fair-in-face.mid'  # this directory will be used as outfile directory
    tracks:
        s-ssa_s1:  # e.g. this will output to `/my/midis/fair_s-ssa_s1.mid
            - soprano
            - ssa_s1
        s-ssa_s2:
            - soprano
            - ssa_s2
        a-ssa_s2:
            - alto
            - ssa_s2
        a-ssa_a:
            - alto
            - ssa_a
        ...
locus:
    input_mid: '/my/midis/locusiste.mid'
    tracks:
        sop:
            - soprano
        alto:
            - alto
        tenor:
            - tenor
        bass:
            - bass
```
You may pass multiple midi specs, each indicating the input midi file and what tracks to construct (as indicated by a map of track name -> constituent tracks to foreground).


## Limitations/TODOs
* ideally, you could set the volume/pan adjustment via the CLI (right now they're constant)
* ideally, this could change instruments for you:
	* turn all of the tracks into the same, inoffensive instrument
	* turn the foregrounded track into a different instrument for maximum contrast
* option to output audio files (`.wav`, `.mp3`, etc.) instead of/in addition to `.mid` files
	* I tried this using FluidSynth but it was a pain and the generated `.wav` files didn't seem to respect my volume and pan settings from the midi? See branch: [`wav-output`](https://github.com/maiamcc/learn-trax/tree/wav-output)
* `learn-trax` strips the first midi track because for Sibelius-generated midi files (what I am working with), this is always metadata. Is this true of all midi files? I don't actually know! 🙃
