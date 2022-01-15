# import time
import asyncio
import random
import song

major_scale = [2, 2, 1, 2, 2, 2, 1]

def generate_scale(intervals, start_octave, num_octaves):
    notes = [start_octave * 12 + 12]
    while len(notes) < num_octaves * len(intervals):
        interval = intervals[(len(notes) - 1) % len(intervals)]
        notes.append(notes[-1] + interval)
    return notes



async def main():
    # notes = generate_scale(major_scale, 2, 21)
    # n = 7
    # track1.add_note(1, notes[n])
    # for i in range(1, 8):
    #     if random.randint(1, 100) < 20:
    #         track1.add_rest(random.choice([0.25, 0.5, 1]))
    #     else:
    #         n += random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    #         # track1.add_note(random.choice([0.25, 0.5, 1, 2]), notes[n], velocity=100)
    #         track1.add_note(random.choice([0.5]), notes[n], velocity=100)

    # track2 = Track(4, channel=1)
    # for i in range(0, 8):
    #     print(i)
    #     track2.add_note(0.5, 42, 100)

    # sequencer = Sequencer()
    # sequencer.add_track(track1)
    # sequencer.add_track(track2)

    # sequencer.print_events()

    beat = 0.5
    song1 = song.Song(beat * 8)
    notes = generate_scale(major_scale, 1, 6)
    time = 0
    n = 14
    for i in range(0, 8):
        n += random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        t = random.choice([beat/2, beat, beat*2])
        song1.add_event(time, song.Event(t, notes[n], random.randint(30,100), 0))
        time += t

    time = 0
    for i in range(0, 8):
        song1.add_event(time, song.Event(beat, 42, 70, 1))
        time += beat

    await song1.play()


asyncio.run(main())