import time
from mingus.midi import fluidsynth
from mingus.containers import Note

fluidsynth.init("keys.sf2")

n = Note("C", 3)
fluidsynth.play_Note(n)
time.sleep(2)
fluidsynth.stop_Note(n)
time.sleep(1)