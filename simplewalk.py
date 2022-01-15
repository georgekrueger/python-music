# import time
import asyncio
import random
import song
import music

async def main():
    beat = 0.5
    song1 = song.Song(beat * 8)
    notes = music.generate_scale(music.major_scale, 1, 6)
    time = 0
    n = 14
    for i in range(0, 8):
        n += random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        t = random.choice([beat/2, beat, beat*2, beat*4])
        song1.add_event(time, song.Event(t, notes[n], random.randint(30,100), 0))
        time += t

    time = 0
    song1.add_event(0, song.Event(beat, 36, 100, 1))
    for i in range(0, 8):
        song1.add_event(time, song.Event(beat, 42, 70, 1))
        time += beat

    await song1.play()


asyncio.run(main())