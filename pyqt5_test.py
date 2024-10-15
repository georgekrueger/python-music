#!/usr/bin/python3
import sys
import rtmidi
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QRegion, QPolygon, QPen, QBrush, QFont
from PyQt5.QtCore import Qt, QPoint
from shapely.geometry import Polygon
import mingus.core.chords as chords
from mingus.containers import Note
from mingus.containers import NoteContainer

g_notes_on = set()

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    print("open port 0")
    midiout.open_port(0)
else:
    print("create virtual port")
    midiout.open_virtual_port("My virtual output")

def allNotesOff():
    for note in g_notes_on:
        midiout.send_message([0x80, note, 0])
    g_notes_on.clear()

def noteOn(note, velocity):
    g_notes_on.add(note)
    midiout.send_message([0x90, note, velocity])

def noteOff(note):
    g_notes_on.remove(note)
    midiout.send_message([0x80, note, 0])

def pointOnCircle(center, radius, angle):
    '''
        Finding the x,y coordinates on circle, based on given angle
    '''
    from math import cos, sin, pi
    #center of circle, angle in degree and radius of circle
    # center = [0,0]
    angle_radians = angle * (pi / 180.0)
    # radius = 100
    x = center[0] + (radius * cos(angle_radians))
    y = center[1] + (radius * sin(angle_radians))
    return QPoint(int(x), int(y))

def lineIntersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

class ClickableImage(QWidget):
    def __init__(self, imagePath):
        super().__init__()

        # self.pixmap = QPixmap(imagePath)
        self.zones = {}  # Dictionary to store clickable zones

        self.initUI()

    def initUI(self):
        # self.resize(self.pixmap.width(), self.pixmap.height())
        self.resize(660, 660)
        self.setWindowTitle('Clickable Image')
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.drawPixmap(self.rect(), self.pixmap)

        for name, polygon in self.zones.items():
            print("draw %s" % (name))
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawPolygon(polygon)
            painter.setFont(QFont('Arial', 20))
            poly = Polygon([(p.x(), p.y()) for p in polygon])
            painter.drawText(int(poly.centroid.x), int(poly.centroid.y), name)
            
            # mid = lineIntersection([[polygon[0].x(), polygon[0].y()], [polygon[2].x(), polygon[2].y()]], \
                                    # [[polygon[1].x(), polygon[1].y()], [polygon[3].x(), polygon[3].y()]])
            # painter.drawText(mid[0], mid[1], name)
            # p1 = polygon[0]
            # p2 = polygon[2]
            # painter.drawText((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2, name)

    def addZone(self, name, polygon):
        self.zones[name] = polygon

    def mousePressEvent(self, event):
        pos = event.pos()
        for name, polygon in self.zones.items():
            if polygon.containsPoint(pos, Qt.OddEvenFill):
                print(f"Clicked on zone: {name}")
                notes = []
                if name[-1] == "m":
                    # minor chord
                    note_name = name[:-1]
                    notes = chords.minor_triad(note_name)
                else:
                    notes = chords.major_triad(name)

                allNotesOff()

                # chord = NoteContainer()
                for note in notes:
                    noteOn(int(Note(note, 4)), 100)
                    # chord.add_note(Note(note, 4))

                break

flat = "\u266d"
outer_notes = ["A", "E", "B", "Gb", "Db", "Ab", "Eb", "Bb", "F", "C", "G", "D"]
inner_notes = ["F#m", "C#m", "G#m", "Ebm", "Bbm", "Fm", "Cm", "Gm", "Dm", "Am", "Em", "Bm"]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClickableImage('circle_of_fifths.png')

    center = [330, 330]
    outer_radius = 310
    inner_radius = 200

    for i in range(0, 12):
        print(i)
        angle = i * 30
        outer_zone = QPolygon([pointOnCircle(center, inner_radius, angle), pointOnCircle(center, outer_radius, angle), \
                        pointOnCircle(center, outer_radius, angle+30), pointOnCircle(center, inner_radius, angle+30)])
        window.addZone(outer_notes[i], outer_zone)
        inner_zone = QPolygon([QPoint(*center), pointOnCircle(center, inner_radius, angle), \
                        pointOnCircle(center, inner_radius, angle+30)])
        window.addZone(inner_notes[i], inner_zone)

    sys.exit(app.exec_())

