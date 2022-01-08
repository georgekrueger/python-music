import mido
import time
import asyncio
import random
from datetime import datetime

#print (mido.get_output_names())

major_scale = [2, 2, 1, 2, 2, 2, 1]

def generate_scale(intervals, start_octave, length):
    notes = [start_octave * 12 + 12]
    while len(notes) < length:
        interval = intervals[(len(notes) - 1) % len(intervals)]
        notes.append(notes[-1] + interval)
    return notes

outport = mido.open_output('loopMIDI Port 1')

async def note(t, length, note_num=None, velocity=100, channel=0):
    await asyncio.sleep(t)
    print("[%s] play note %s %s %s" % (datetime.now().time(), length, note_num, velocity))
    outport.send(mido.Message('note_on', note=note_num,velocity=velocity, channel=channel))
    await asyncio.sleep(length)
    outport.send(mido.Message('note_off', note=note_num, channel=channel))

def play_note(t, length, note_num=None, velocity=100, channel=0):
    return asyncio.create_task(note(t, length, note_num, velocity, channel))

class Track:
    def __init__(self, channel=0):
        self.channel = channel
        self.notes = []
        self.play_cursor = 0

    def add_note(self, length, note_num=None, velocity=100):
        print("add note %s %s %s" % (length, note_num, velocity))
        self.notes.append((length, note_num, velocity))

    def add_rest(self, length):
        print("add rest %s" % length)
        self.notes.append([length])

    async def play(self, loop=False):
        while 1:
            event = self.notes[self.play_cursor]
            if len(event) == 1:
                await asyncio.sleep(event[0]) # rest
            else:
                await note(0, event[0], event[1], event[2], self.channel)
            self.play_cursor = (self.play_cursor + 1) % len(self.notes)

async def main():
    track1 = Track(channel=0)
    notes = generate_scale(major_scale, 2, 21)
    n = 7
    track1.add_note(1, notes[n])
    for i in range(1, 8):
        if random.randint(1, 100) < 25:
            track1.add_rest(random.choice([0.25, 0.5, 1]))
        else:
            n += random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
            # track1.add_note(random.choice([0.25, 0.5, 1, 2]), notes[n], velocity=100)
            track1.add_note(random.choice([0.5]), notes[n], velocity=100)
    
    track2 = Track(channel=1)
    for i in range(1, 4):
        track2.add_note(0.5, 42, 100)

    await asyncio.gather(track1.play(), track2.play())


asyncio.run(main())