# import time
import asyncio
import random
from random import choice
from random import randint
import song
import music

scales = [music.major_scale(music.Note.C), music.major_scale(music.Note.D)]

async def main():
    beat = .75
    bar = beat * 4
    num_bars = 4
    song1 = song.Song(bar * num_bars)
    time = 0
    n = 7 * 3
    for i in range(0, num_bars):
        scale = scales[randint(0, 1)]
        print(music.midi_note_to_note(scale[n]))
        velocity = randint(75, 100)
        song1.add_event(time, song.Event(bar, scale[n], velocity, 0))
        song1.add_event(time, song.Event(bar, scale[n+4], velocity, 0))
        song1.add_event(time, song.Event(bar, scale[n+7], velocity, 0))
        song1.add_event(time, song.Event(bar, scale[n+9], velocity, 0))

        # time2 = time
        # for j in range(0, 3):
        #     time2 += random.choice([0, beat/2, beat, beat*2, beat*3])
        #     length = random.choice([beat/2, beat, beat*2, beat*4])
        #     # pitch += random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        #     note = random.choice([0, 1, 2, 3, 4])
        #     song1.add_event(time2, song.Event(length, c_maj[n + 21 + note], random.randint(90,120), 0))
        #     time2 += length
        #     if time2 > time + bar:
        #         break

        time += bar
        n += random.choice([-2, -1, 0, 1, 2, 3])
        # while n % 6 == 0:
        #     n += random.choice([-2, -1, 0, 1, 2, 3])

    await song1.play()


asyncio.run(main())