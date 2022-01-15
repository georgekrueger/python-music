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
    song = Song(beat * 4)
    time = 0
    for i in range(0, 4):
        # t = random.choice([beat/2, beat, beat*2])
        t = beat * 2
        song.add_event(time, Event(t, 36+i, 100, 0))
        time += t

    time = 0
    for i in range(0, 4):
        song.add_event(time, Event(beat, 42, 70, 1))
        time += beat

    await song.play()


asyncio.run(main())