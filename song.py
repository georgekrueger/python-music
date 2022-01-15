import mido
import asyncio
from datetime import datetime
from collections import OrderedDict

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
    def __init__(self, length, note_num = None, velocity = None, channel = None):
        self.length = length
        self.note_num = note_num
        self.velocity = velocity
        self.channel = channel

class Song:
    def __init__(self, length):
        self.length = length
        self.events = OrderedDict()
        self.times = []  # order list of event start times
        self.tasks = []
        self.cursor = 0

    # add an event
    def add_event(self, time, event):
        if time >= self.length:
            print("not adding event at time %s that is >= to song length %s" % (time, self.length))
            return
        if time not in self.events:
            self.events[time] = []
        self.events[time].append(event)
        self.times = list(self.events) # re-generate list of times
        self.times.sort()

    def timer_callback(self):
        # play the event(s) at cursor
        cur_time = self.times[self.cursor]
        events = self.events[cur_time]
        #print("sequencer timer. schedule %s events" % (len(events)))
        for event in events:
            if event.note_num != None:
                self.tasks.append(asyncio.create_task(note(event.length, event.note_num, event.velocity, event.channel)))
            else:
                self.tasks.append(asyncio.create_task(asyncio.sleep(event.length)))

        # increment cursor to the next event and set a timer to fire for the it
        # if the next event is past the end, then set a timer for the remaining time left in the song
        self.cursor += 1
        if self.cursor >= len(self.events):
            self.cursor = 0
            self.tasks.append(asyncio.create_task(timer(self.length - cur_time, self.timer_callback)))
        else:
            dur = self.times[self.cursor] - cur_time
            self.tasks.append(asyncio.create_task(timer(dur, self.timer_callback)))

    def print_events(self):
        for key, events in self.events.items():
            for event in events:
                print("t: %s %s %s %s" % (key, event.note_num, event.length, event.channel))

    async def play(self):
        print(self.times)
        self.cursor = 0
        self.tasks.append(asyncio.create_task(timer(self.times[0], self.timer_callback)))
        while True:
            await asyncio.wait(self.tasks)