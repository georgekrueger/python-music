
major_scale = [2, 2, 1, 2, 2, 2, 1]

def generate_scale(intervals, start_octave, num_octaves):
    notes = [start_octave * 12 + 12]
    while len(notes) < num_octaves * len(intervals):
        interval = intervals[(len(notes) - 1) % len(intervals)]
        notes.append(notes[-1] + interval)
    return notes