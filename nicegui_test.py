#!/usr/bin/python3
from nicegui import ui
from nicegui.events import ValueChangeEventArguments
import rtmidi
import time
import mingus.core.chords as chords

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

def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')

def playNote(note, velocity, length):
    noteOn(note, velocity)
    time.sleep(length)
    noteOff(note)

ui.button('Button', on_click=lambda: playNote(55, 100, 1))
with ui.row():
    ui.checkbox('Checkbox', on_change=show)
    ui.switch('Switch', on_change=show)
# ui.radio(['A', 'B', 'C'], value='A', on_change=show).props('inline')
with ui.row():
    ui.input('Text input', on_change=show)
    ui.select(['One', 'Two'], value='One', on_change=show)
ui.link('And many more...', '/documentation').classes('mt-8')

ui.run()