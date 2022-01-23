# import time
import asyncio
import random
import song
import music

async def main():
    beat = 0.5
    eigth = beat / 2
    dot_8 = eigth * 1.5
    dot_4 = beat * 1.5
    song1 = song.Song(beat * 8)
    notes = music.generate_scale(music.major_scale, 1, 6)
    time = 0
    n = 14

    time = 0
    song1.add_event(time, song.Event(dot_8, notes[14], 100, 0))
    time += dot_8
    song1.add_event(time, song.Event(dot_8, notes[15], 100, 0))
    time += dot_8
    song1.add_event(time, song.Event(dot_8, notes[16], 100, 0))
    time += dot_8
    song1.add_event(time, song.Event(dot_8, notes[17], 100, 0))
    time += dot_8
    song1.add_event(time, song.Event(beat, notes[18], 100, 0))
    time += beat
    song1.add_event(time, song.Event(dot_4, notes[19], 100, 0))
    time += dot_4
    song1.add_event(time, song.Event(dot_4, notes[18], 100, 0))
    time += dot_4
    song1.add_event(time, song.Event(beat, notes[17], 100, 0))
    time += beat

    time = 0
    song1.add_event(0, song.Event(beat, 36, 100, 1))
    for i in range(0, 8):
        song1.add_event(time, song.Event(beat, 42, 70, 1))
        time += beat

    await song1.play()


asyncio.run(main())