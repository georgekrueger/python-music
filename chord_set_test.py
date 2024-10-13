# import time
import asyncio
import random
from random import choice
from random import randint
import song
import mingus.core.notes as notes
import mingus.core.keys as keys
import mingus.core.chords as chords
import mingus.core.progressions as progressions

chord = chords.major_triad('D')
for n in chord:
    print(notes.note_to_int(n))

# chords = [['C', 'E', 'G'], ['D', 'F', 'A'], ['E', 'G', 'B'], ['F', 'A', 'C'], ['G', 'B', 'D'], ['A', 'C', 'E']]

def midi_note_to_note(midi_note):
    pass

def voice(chord, focal_point):
    pass

# async def main():
#     beat = .75
#     bar = beat * 4
#     num_bars = 4
#     song1 = song.Song(bar * num_bars)
#     time = 0
#     n = 7 * 3
#     for i in range(0, num_bars):
#         print(music.midi_note_to_note(c_maj[n]))
#         velocity = randint(75, 100)
#         scale = scales[randint(0, 1)]
#         song1.add_event(time, song.Event(bar, scale[n], velocity, 0))
#         song1.add_event(time, song.Event(bar, scale[n+4], velocity, 0))
#         song1.add_event(time, song.Event(bar, scale[n+7], velocity, 0))
#         song1.add_event(time, song.Event(bar, scale[n+9], velocity, 0))

#         time += bar
#         n += random.choice([-2, -1, 0, 1, 2, 3])
#         # while n % 6 == 0:
#         #     n += random.choice([-2, -1, 0, 1, 2, 3])

#     await song1.play()


# asyncio.run(main())