from enum import Enum
from typing import NamedTuple
from progressions import PROGRESSIONS
from notes import (CIRCLE_OF_FIFTHS, MAJ_PATTERN, get_scale)
from chords import (
    chord_template_from_str, chord_template_to_str,
    get_chord_notes, get_chord_root, get_all_chord_degrees)
from ui import UI
from playback import (play_chord, begin_playback)

def rotate(array, n):
    return array[n:] + array[:n]

### GLOBAL DATA

# index into list of all keys
KEY_INDEX = CIRCLE_OF_FIFTHS.index("C")
# index into list of progressions
PROG_INDEX = 0
# possible future use to change modes
MODAL_INDEX = 0 

### SCREEN UPDATERS, DELIVER DATA TO APP

def get_play_chord_lambda(chord_notes, scale_root):
    return lambda event: play_chord(chord_notes, scale_root)

def get_play_all_lambda(all_notes, scale_root):
    return lambda event: begin_playback(all_notes, scale_root)

def set_scale(app, key):
    scale = get_scale(key, rotate(MAJ_PATTERN, MODAL_INDEX))
    app.set_key_label(key)
    app.set_scale(scale)
    all_chords = get_all_chord_degrees(scale)
    for i in range(7):
        app.degree_labels[i].bind("<Button-1>", 
            get_play_chord_lambda(all_chords[i], scale[0]))
    return scale

def set_progression(app, prog, scale):
    # template strings to templates
    templates = [chord_template_from_str(x) for x in prog]
    # templates to notes and chord strings
    app.set_notes([get_chord_notes(get_chord_root(t, scale), t.quality) for t in templates])
    chords = [chord_template_to_str(t, scale) for t in templates]
    # set on the screen
    app.set_progression(prog, chords)
    # bind to the labels and play button for playback
    for i, lbl in enumerate(app.chord_labels):
        lbl.bind("<Button-1>", get_play_chord_lambda(app.notes[i], scale[0]))
    app.prog_buttons["last"].bind("<Button-1>", get_play_all_lambda(app.notes, scale[0]))

def update_screen(app):
    # set the scale at the top
    scale = set_scale(app, CIRCLE_OF_FIFTHS[KEY_INDEX])
    # set the progression at the bottom
    set_progression(app, PROGRESSIONS[PROG_INDEX].split(' '), scale)


### CREATE THE SCREEN
the_app = UI()
UI.create_app(the_app)
update_screen(the_app)

### BIND EVENT HANDLERS

def key_prev(event):
    global KEY_INDEX
    KEY_INDEX -= 1
    if KEY_INDEX < 0:
        KEY_INDEX = len(CIRCLE_OF_FIFTHS) - 1
    update_screen(the_app)

def key_next(event):
    global KEY_INDEX
    KEY_INDEX += 1
    if KEY_INDEX == len(CIRCLE_OF_FIFTHS):
        KEY_INDEX = 0
    update_screen(the_app)

def prog_prev(event):
    global PROG_INDEX
    PROG_INDEX -= 1
    if PROG_INDEX < 0:
        PROG_INDEX = len(PROGRESSIONS) - 1
    update_screen(the_app)

def prog_next(event):
    global PROG_INDEX
    PROG_INDEX += 1
    if PROG_INDEX == len(PROGRESSIONS):
        PROG_INDEX = 0
    update_screen(the_app)

the_app.key_buttons["prev"].bind("<Button-1>", key_prev)
the_app.key_buttons["next"].bind("<Button-1>", key_next)
the_app.prog_buttons["prev"].bind("<Button-1>", prog_prev)
the_app.prog_buttons["next"].bind("<Button-1>", prog_next)

### THUNDERCATS GOOOOOOO
the_app.window.mainloop()
