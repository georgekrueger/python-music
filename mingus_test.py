import mingus.core.notes as notes
import mingus.core.keys as keys
import mingus.core.chords as chords
from mingus.containers import Note
from mingus.containers import NoteContainer
from mingus.containers import Bar
from mingus.containers import Track
from mingus.containers import Composition
#from mingus.containers.instrument import Instrument
from mingus.midi import fluidsynth
from mingus.midi import midi_file_out
import mingus.extra.lilypond as LilyPond
import time
import random

#print(notes.__file__)

#print(chords.determine(["E", "C", "G"], shorthand=True))
#print(chords.determine(['C', 'E', 'A']))
chord1 = chords.triads("C")[0]
chord1_nc = NoteContainer(chord1)
#print("%s %s" % (chord1_nc.get_note_names(), chords.determine(chord1_nc.get_note_names())))

fluidsynth.init("keys.sf2")

#print( chords.triads("C")[:-1] +  [chords.triads("c")[0]] + chords.triads("c")[2:] )

''' Notes
* Separate voices (tracks) so sheet music shows separate parts for bass / treble
* Try picking only a few chords and then generate 8-bar pattern from only those chords
* Play chords with inversions to keep the voicings close to each other (see voicing func below)
* Add a function to generate a voicing of a chord
  * start_range, end_range: range within the chord must fit
  * how many notes in the voicing
  * spread: show dense or sparse the distribution of notes should be 
'''


#chord_list = chords.triads("C")[:-1] +  [chords.triads("c")[0]] + chords.triads("c")[2:]
#print(chord_list)

# build a master chord list
chord_list = []
for i in range(0, 6):
    chord_list.append((chords.triads("C")[i], "%s" % (i+1)))
chord_list.append((chords.triads("c")[0], "1*"))
for i in range(2, 7):
    chord_list.append((chords.triads("c")[i], "%s*" % (i+1)))

def octave(note, n):
    return Note(note.name, note.octave+n)

# pick some chords from the list
new_chord_list = []
for i in range(0, 6):
    new_chord_list.append(chord_list[random.randint(0, len(chord_list)-1)])

composition = Composition()

def makeBassChord(triad):
    return NoteContainer([
                  octave(triad[0], -2),
                  octave(triad[2], -2), 
                  octave(triad[1], -1)
                  ])

def arpeggiate(chord, track):
    # print(chord[0])
    track.add_notes(NoteContainer(chord[0]), 4)
    track.add_notes(NoteContainer(chord[1]), 4)
    track.add_notes(NoteContainer(chord[2]), 4)
    track.add_notes(NoteContainer(chord[1]), 4)

def repeat(track, count):
    new_track = Track()
    for i in range(0, count):
        for bar in track:
            new_track.add_bar(bar)
    return new_track

chosen_chords = []

track = Track()
triad = NoteContainer(chord_list[0][0])
# track.add_notes(makeBassChord(triad), 1)
c = makeBassChord(triad)
print("[%s]: %s" % (c, c.get_note_names()))
arpeggiate(c, track)
chosen_chords.append(chord_list[0])

for i in range(0, 3):
    n = random.randint(0, len(new_chord_list)-1)
    chosen_chord = new_chord_list[n]
    chosen_chords.append(chosen_chord)
    triad = NoteContainer(chosen_chord[0])
    c = makeBassChord(triad)
    print("[%s]: %s" % (c, c.get_note_names()))
    #track.add_notes(c, 1)
    arpeggiate(c, track)

composition.add_track(repeat(track, 2))

# print(chosen_chords)

# track = Track()
# for chord in chosen_chords:
#   triad = NoteContainer(chord[0])
#   c = NoteContainer([triad[1], triad[2]])
#   print("%s" % (triad.get_note_names()))
#   track.add_notes(c, 1)

# composition.add_track(track)

fluidsynth.play_Composition(composition, [1], 100)
midi_file_out.write_Track("song.mid", track, 100)

#LilyPond.to_png(LilyPond.from_Composition(composition), "mysong")

time.sleep(2)