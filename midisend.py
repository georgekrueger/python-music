import mido
import time
import asyncio
import random
from datetime import datetime
from collections import OrderedDict

#print (mido.get_output_names())

major_scale = [2, 2, 1, 2, 2, 2, 1]

def generate_scale(intervals, start_octave, length):
    notes = [start_octave * 12 + 12]
    while len(notes) < length:
        interval = intervals[(len(notes) - 1) % len(intervals)]
        notes.append(notes[-1] + interval)
    return notes

outport = mido.open_output('loopMIDI Port 1')

async def note(length, note_num=None, velocity=100, channel=0):
    print("[%s] play note %s %s %s" % (datetime.now().time(), length, note_num, velocity))
    outport.send(mido.Message('note_on', note=note_num,velocity=velocity, channel=channel))
    await asyncio.sleep(length)
    outport.send(mido.Message('note_off', note=note_num, channel=channel))

async def timer(t, callback):
    print("start timer for %s" % (t))
    await asyncio.sleep(t)
    callback()

class Event:
    def __init__(self, length, note_num = None, velocity = None):
        self.length = length
        self.note_num = note_num
        self.velocity = velocity
        self.t = None
        self.channel = None

class Sequencer:
    def __init__(self):
        self.events = OrderedDict()
        self.times = []
        self.tasks = []
        self.cursor = 0

    def add_track(self, track):
        t = 0
        for event in track.events:
            event.channel = track.channel
            event.t = t
            if t not in self.events:
                self.events[t] = []
            self.events[t].append(event)
            t += event.length
        self.times = list(self.events) # list of keys (times)

    def timer_callback(self):
        cur_time = self.times[self.cursor]
        events = self.events[cur_time]
        print("sequencer timer. schedule %s events" % (len(events)))
        for event in events:
            if event.note_num != None:
                self.tasks.append(asyncio.create_task(note(event.length, event.note_num, event.velocity, event.channel)))
            else:
                self.tasks.append(asyncio.create_task(asyncio.sleep(event.length)))

        next_cursor = (self.cursor + 1) % len(self.events)
        dur = self.times[next_cursor] - cur_time
        self.tasks.append(asyncio.create_task(timer(dur, self.timer_callback)))
        self.cursor = next_cursor

    async def play(self):
        self.timer_callback() #schedule first event
        while True:
            await asyncio.wait(self.tasks)

class Track:
    def __init__(self, channel=0):
        self.channel = channel
        self.events = []

    def add_note(self, length, note_num=None, velocity=100):
        print("add note %s %s %s" % (length, note_num, velocity))
        self.events.append(Event(length, note_num, velocity))

    def add_rest(self, length):
        print("add rest %s" % length)
        self.events.append(Event(length))

async def main():
    track1 = Track(channel=0)
    for i in range(1, 4):
        track1.add_note(0.5, 42+i, 100)
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

    track2 = Track(channel=1)
    for i in range(1, 4):
        track2.add_note(0.5, 42, 100)

    sequencer = Sequencer()
    sequencer.add_track(track1)
    sequencer.add_track(track2)

    await sequencer.play()

    # await asyncio.gather(track1.play(), track2.play())


asyncio.run(main())