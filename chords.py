from enum import Enum
from typing import NamedTuple

from notes import (NOTES, get_note_index)


class Quality(Enum):
    MAJOR_TRIAD = 1
    MINOR_TRIAD = 2
    DIM_TRIAD   = 3
    AUG_TRIAD   = 4
    MAJ_7       = 5
    MIN_7       = 6
    DOM_7       = 7
    DIM_7       = 8

class Accidental(Enum):
    NATURAL = 1
    FLAT    = 2
    SHARP   = 3

class ChordTemplate(NamedTuple):
    """ Representation of a chord string like IVb7 - has
        scale degree, accidental (may be NATURAL), and quality """
    degree:     int                 # scale degree
    accidental: Accidental          # accidental modifying scale degree
    quality:    Quality             # chord quality

# Spacings between notes (on the 12-tone scale) for different types of
# chords. Note that this uses the 12-tone scale and not the 7 tone key
# scale because some notes are not in key.
CHORD_INTERVAL_PATTERNS = {
    Quality.MAJOR_TRIAD: [4, 3],
    Quality.MINOR_TRIAD: [3, 4],
    Quality.DIM_TRIAD:   [3, 3],
    Quality.AUG_TRIAD:   [4, 4],
    Quality.MAJ_7:       [4, 3, 4],
    Quality.MIN_7:       [3, 4, 3],
    Quality.DOM_7:       [4, 3, 3],
    Quality.DIM_7:       [3, 3, 3]
}

def get_chord_notes(root: str, quality: Quality):
    """ Given a root note and a quality, return the notes in a chord """
    index = get_note_index(root)
    notes = [NOTES[index]]
    for bump in CHORD_INTERVAL_PATTERNS[quality]:
        index += bump
        notes.append(NOTES[index])
    return notes

def get_chord_root(template: ChordTemplate, scale: list):
    """ Given a template and the current 7-tone scale, determines the 
        root (using the accidental) """
    root_before_acc = scale[template.degree - 1]
    if template.accidental == Accidental.NATURAL:
        return root_before_acc
    bump = -1 if template.accidental == Accidental.FLAT else 1
    return NOTES[get_note_index(root_before_acc) + bump]

def get_all_chord_degrees(scale):
    all_chords = []
    qualities = [Quality.MAJOR_TRIAD, Quality.MINOR_TRIAD, Quality.MINOR_TRIAD,
                 Quality.MAJOR_TRIAD, Quality.MAJOR_TRIAD, Quality.MINOR_TRIAD, Quality.DIM_TRIAD]
    for i in range(7):
        all_chords.append(get_chord_notes(scale[i], qualities[i]))
    return all_chords


### CHORD STRING PARSING BLAH

QUALITY_SUFFIXES = {Quality.MINOR_TRIAD: "m", 
                    Quality.MAJOR_TRIAD: "",
                    Quality.DIM_TRIAD:   "o",
                    Quality.AUG_TRIAD:   "+",
                    Quality.MAJ_7:       "M7",
                    Quality.MIN_7:       "m7",
                    Quality.DOM_7:       "7",
                    Quality.DIM_7:       "o7"}

ACCIDENTAL_STR = {Accidental.FLAT: "b", Accidental.SHARP: "#", Accidental.NATURAL: ""}

def get_quality(chord_str: str):
    """ returns the quality according to the string suffix, or None
        if no suffix is given """
    if chord_str.endswith("7"):
        if chord_str.endswith("m7"):
            return Quality.MIN_7
        if chord_str.endswith("M7"):
            return Quality.MAJ_7
        if chord_str.endswith("o7"):
            return Quality.DIM_7
        return Quality.DOM_7
    if chord_str.endswith("m"):
        return Quality.MINOR_TRIAD
    if chord_str.endswith("o"):
        return Quality.DIM_TRIAD        
    if chord_str.endswith("+"):
        return Quality.AUG_TRIAD
    if chord_str.endswith("M"):
        return Quality.MAJOR_TRIAD
    return None

def get_accidental(chord_str: str):
    if chord_str.endswith("b"):
        return Accidental.FLAT
    if chord_str.endswith("#"):
        return Accidental.SHARP
    return Accidental.NATURAL

NUMERAL_TO_INT = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7}

def chord_template_from_str(chord_str: str):
    """ Given a string, return a ChordTemplate 
        String looks like "IVbm7":
            * numeral (non-optional)
            * accidental (optional)
            * quality suffix (optional)
        If no quality suffix is given, the standard enharmonic triad for
        the given scale degree will be assumed.
    """
    # quality
    quality = get_quality(chord_str)
    if quality is not None:
        chord_no_suffix = chord_str.replace(QUALITY_SUFFIXES[quality], "")
    else:
        chord_no_suffix = chord_str
    # accidental 
    accidental = get_accidental(chord_no_suffix)
    chord_no_acc = chord_no_suffix.replace(ACCIDENTAL_STR[accidental], "")
    # degree
    degree = NUMERAL_TO_INT[chord_no_acc]
    
    # default quality handling for mode
    if quality is None:
        # TODO: this breaks for any mode other than major
        if degree in {1,4,5}:
            quality = Quality.MAJOR_TRIAD
        elif degree in {2,3,6}:
            quality = Quality.MINOR_TRIAD
        elif degree == 7:
            quality = Quality.DIM_TRIAD
    return ChordTemplate(degree, accidental, quality)

def chord_template_to_str(template: ChordTemplate, scale: list):
    """ Note that the accidental is not its own part of this string, because
        it is already accounted for in getting the root """
    return (get_chord_root(template, scale) + 
            QUALITY_SUFFIXES[template.quality])