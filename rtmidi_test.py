#!/usr/bin/python3
import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    print("open port 0")
    midiout.open_port(0)
else:
    print("create virtual port")
    midiout.open_virtual_port("My virtual output")

def noteOn(note, velocity):
    midiout.send_message([0x90, note, velocity])

def noteOff(note):
    midiout.send_message([0x80, note, 0])

for i in range(0, 5):
    noteOn(50, 100)
    noteOn(60, 100)
    time.sleep(2)
    noteOff(50)
    noteOff(60)
    time.sleep(0.5)

del midiout