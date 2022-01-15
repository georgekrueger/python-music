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
    #print("start timer for %s" % (t))
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
            if t >= track.length:
                break
        if t < track.length:
            if t not in self.events:
                self.events[t] = []
            self.events[t].append(Event(track.length - t))
        self.times = list(self.events) # list of keys (times)

    def timer_callback(self):
        cur_time = self.times[self.cursor]
        events = self.events[cur_time]
        #print("sequencer timer. schedule %s events" % (len(events)))
        for event in events:
            if event.note_num != None:
                self.tasks.append(asyncio.create_task(note(event.length, event.note_num, event.velocity, event.channel)))
            else:
                self.tasks.append(asyncio.create_task(asyncio.sleep(event.length)))

        self.cursor += 1
        if self.cursor >= len(self.events):
            self.cursor = 0
            self.tasks.append(asyncio.create_task(timer(events[0].length, self.timer_callback)))
        else:
            dur = self.times[self.cursor] - cur_time
            self.tasks.append(asyncio.create_task(timer(dur, self.timer_callback)))

    def print_events(self):
        for key, events in self.events.items():
            for event in events:
                print("t: %s %s %s %s" % (key, event.note_num, event.length, event.channel))

    async def play(self):
        self.timer_callback() #schedule first event
        while True:
            await asyncio.wait(self.tasks)

class Track:
    def __init__(self, length, channel=0):
        self.length = length
        self.channel = channel
        self.events = []

    def add_note(self, length, note_num=None, velocity=100):
        print("add note %s %s %s" % (length, note_num, velocity))
        self.events.append(Event(length, note_num, velocity))

    def add_rest(self, length):
        print("add rest %s" % length)
        self.events.append(Event(length))

async def main():
    track1 = Track(4, channel=0)
    for i in range(1, 5):
        track1.add_note(0.5, 36+i, 100)

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

    track2 = Track(4, channel=1)
    for i in range(0, 8):
        print(i)
        track2.add_note(0.5, 42, 100)

    sequencer = Sequencer()
    sequencer.add_track(track1)
    sequencer.add_track(track2)

    await sequencer.play()
    # sequencer.print_events()

    # await asyncio.gather(track1.play(), track2.play())


asyncio.run(main())