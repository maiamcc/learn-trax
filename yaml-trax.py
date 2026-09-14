#!/usr/bin/env python

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any, List, Optional
import yaml


from mido import MidiFile

import trax
import utils


"""
ave-maria: # outfile prefix
    input_mid: /path/to/ave.mid
    tracks:
        s1_s:
            - s1,sop,ssa_s
"""
@dataclass
class FileSpec:
    """Instructions on how to make a set of tracks
    for a single input midi"""
    base_outfile: str
    input_mid: str
    track_sets: dict[str, list[str]] # dict of part name -> list of component tracks

    @classmethod
    def parse(cls, base_outfile: str, info: dict) -> 'FileSpec':
        print(info)
        input_mid = info['input_mid']
        track_sets = info['tracks']


        return cls(base_outfile, input_mid, track_sets)


    @property
    def midi_file_name(self) -> str:
        _, filename = os.path.split(self.input_mid)
        return filename

    @property
    def output_dir(self) -> str:
        directory, _ = os.path.split(self.input_mid)
        return directory

    def make_trax(self):
        for track_name, component_tracks in self.track_sets.items():
            trax.select_trax(
                input_mid=self.input_mid,
                outfile=f"{self.base_outfile}-{track_name}",
                track_names=component_tracks,
                output_dir=self.output_dir,
            )

@dataclass
class ParsedYaml:
    """The contents of a parsed yaml file containing
    instructions on how to make some number of tracks"""
    file_specs: list[FileSpec]

    @classmethod
    def from_path(cls, path: str) -> 'ParsedYaml':
        yaml_dict = yaml.safe_load(Path(path).read_text())

        assert isinstance(yaml_dict, dict)
        specs = [FileSpec.parse(k, v) for k, v in yaml_dict.items()]
        return cls(specs)




def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'yaml_path',
        type=str,
        help='path to yaml file detailing tracks'
    )

    return parser


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()

    parsed = ParsedYaml.from_path(args.yaml_path)
    for spec in parsed.file_specs:
        print(f"Making {len(spec.track_sets)} track(s) for {spec.midi_file_name}...")
        spec.make_trax()






def _single_key_and_val(d: dict) -> (Any, Any):
    keys = [k for k in d.keys()]
    vals = [v for v in d.values()]
    assert len(keys) == 1
    assert len(vals) == 1
    return keys[0], vals[0]



