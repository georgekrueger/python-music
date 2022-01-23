import mingus.core.notes as notes
import mingus.core.keys as keys
import mingus.core.chords as chords
from mingus.containers import Note
from mingus.containers import NoteContainer
from mingus.containers import Bar
from mingus.containers import Track
from mingus.containers.instrument import Instrument, Piano, Guitar
from mingus.midi import fluidsynth
import time
import random

fluidsynth.init("keys.sf2")

#print( chords.triads("C")[:-1] +  [chords.triads("c")[0]] + chords.triads("c")[2:] )

t = Track()
chord_list = chords.triads("C")[:-1] +  [chords.triads("c")[0]] + chords.triads("c")[2:]
print(chord_list)

def octave(note, n):
    return Note(note.name, note.octave+n)

for i in range(0, 8):
    n = random.randint(0, len(chord_list)-1)
    triad = NoteContainer(chord_list[n])
    c = NoteContainer([
                      octave(triad[0], -2),
                      octave(triad[0], -1), 
                      octave(triad[2], -1),
                      triad[1], 
                      triad[2],
                      octave(triad[1], 1) if random.randint(0, 1) == 0 else octave(triad[2], 1)
                      ])
    # print("%s: %s" % (n+1, NoteContainer(c.remove_duplicate_notes()).determine(True)))
    print("%s: %s" % (n+1, c.get_note_names()))
    t.add_notes(c, 1)

fluidsynth.play_Track(t, 1, 100)

time.sleep(2)