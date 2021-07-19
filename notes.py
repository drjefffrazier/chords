NOTES = "A A# B C C# D D# E F F# G G#".split(' ') * 2
SHARPS_TO_FLATS = {"A#": "Bb", "C#": "Db", "D#": "Eb", "F#": "Gb", "G#": "Ab"}
FLATS_TO_SHARPS = {"Ab": "G#", "Bb": "A#", "Db": "C#", "Eb": "D#", "Gb": "F#"}
CIRCLE_OF_FIFTHS = "Gb Db Ab Eb Bb F C G D A E B".split(' ')
MAJ_PATTERN = [2,2,1,2,2,2,1]

def as_sharp(note: str):
    if note.endswith("b"):
        return FLATS_TO_SHARPS[note]
    return note

def as_flat(note: str):
    if note.endswith("#"):
        return SHARPS_TO_FLATS[note]
    return note

def get_note_index(note: str):
    return NOTES.index(as_sharp(note))

# TODO: only works for major mode
def key_has_flats(root):
    return (root == "F" or root.endswith("b"))

def get_scale(root, pattern):
    has_flats = key_has_flats(root)
    note_index = get_note_index(root)
    scale = []
    for bump in pattern:
        scale.append(NOTES[note_index])
        note_index += bump
    if has_flats:
        scale = [as_flat(x) for x in scale]
    return scale