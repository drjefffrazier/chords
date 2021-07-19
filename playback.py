from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

def play_chord(note_strs, scale_root_str):
    # assume the scale root is at a particular octave
    base_octave = 3
    scale_root = Note(f"{scale_root_str}{base_octave}")
    notes_to_play = []
    last_note = scale_root
    for note_str in note_strs:
        # we have to find the right octave for each note --
        # they will be at most 2 octaves above the base 
        # note, so we can always create the lowest note that 
        # makes the sequence go up
        note = Note(f"{note_str}{base_octave}")
        if note < last_note:
            note = Note(f"{note_str}{base_octave+1}")
        if note < last_note:
            note = Note(f"{note_str}{base_octave+2}")
        notes_to_play.append(note)
        last_note = note
    print(notes_to_play)
    
    time = 0.0
    timeline = Timeline()
    for note in notes_to_play:
        timeline.add(time, Hit(note, 0.5))
    data = timeline.render()
    data = data * 0.25
    playback.play(data)

def begin_playback(progression, scale_root_dir, times_per_chord=2, speed_bpm=60):
    for chord in progression:
        for _ in range(times_per_chord):
            play_chord(chord, scale_root_dir)