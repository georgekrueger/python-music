from enum import IntEnum

class Note(IntEnum):
    C = 0
    Db = 1
    D = 2
    Eb = 3
    E = 4
    F = 5
    Gb = 6
    G = 7
    Ab = 8
    A = 9
    Bb = 10
    B = 11

def major_scale(root_note):
    return make_scale(root_note, [2, 2, 1, 2, 2, 2, 1])

def minor_scale(root_note):
    return make_scale(root_note, [2, 1, 2, 2, 1, 2, 2])

def make_scale(root_note, intervals):
    notes = [12 + int(root_note)]
    while notes[-1] < 127:
        interval = intervals[(len(notes) - 1) % len(intervals)]
        notes.append(notes[-1] + interval)
    return notes

def midi_note_to_note(midi_note):
    return Note(midi_note % 12)