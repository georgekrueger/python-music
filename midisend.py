import mido
import time
import asyncio
import random
from datetime import datetime

#print (mido.get_output_names())

major_scale = [2, 2, 1, 2, 2, 2, 1]

def generate_scale(scale, start_octave, length):
    notes = [start_octave * 12 + 12]
    while len(notes) < length:
        interval = scale[(len(notes) - 1) % len(scale)]
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
        self.cursor = 0

    def add_note(self, length, note_num=None, velocity=100, sustain=0):
        print("add note %s %s %s" % (length, note_num, velocity))
        self.notes.append(asyncio.create_task(note(self.cursor, length + sustain, note_num, velocity, self.channel)))
        self.cursor += length

    def add_rest(self, length):
        print("add rest %s" % length)
        self.cursor += length

    async def play(self, loop=False):
        # asyncio.get_event_loop().run_until_complete(asyncio.wait(self.notes))
        done, pending = await asyncio.wait(self.notes)
        while loop:
            done, pending = await asyncio.wait(self.notes)

async def main():
    track1 = Track()
    notes = generate_scale(major_scale, 3, 21)
    note = notes[0]
    track1.add_note(1, note)
    # for i in range(1, 10):
    #     if random.randint(1, 100) < 25:
    #         track1.add_rest(random.choice([0.25, 0.5, 1]))
    #     else:
    #         note += random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    #         track1.add_note(random.choice([0.25, 0.5, 1, 2]), note, velocity=100, sustain=0)
    for i in range(1, 4):
        note += random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        track1.add_note(random.choice([2]), note, velocity=100, sustain=0)
    await track1.play(loop=True)


asyncio.run(main())