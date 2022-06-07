from turtle import position
import pygame
import mido
from resources import *
from processing import *
from utils import roundToMultiple

class Song:
    def __init__(self,timeSignature,tempo,name,has_pickup,pickup_duration):
        self.timeSignature = timeSignature
        self.tempo = tempo
        self.measures = []
        self.chordsReadable = []
        self.chords = []
        self.name = name
        self.has_pickup = has_pickup
        self.pickup_duration = pickup_duration

    def writeChordsReadable(self):
        for i in range(0,len(self.chords)):
            notesList = []
            if i + 1 < len(self.chords):
                notesList.append(self.chords[i+1].duration)
            for j in range(0,len(self.chords[i].notes)):
                notesList.append(self.chords[i].notes[j].noteName)
            self.chordsReadable.append(notesList)
    def addMeasure(self):
        self.measures += 1
    def createMeasures(self):
        self.writeChordsReadable()
        i = 0
        while i < len(self.chordsReadable):
            list = []
            sumBeats = 0.0
            measure_value = (self.timeSignature[0]/self.timeSignature[1]) #how many beats in one measure = top number of time sig/lower number of time sig
            if self.has_pickup and len(self.measures) == 0:
                sumBeats = measure_value - self.pickup_duration
            while i < len(self.chordsReadable) and sumBeats < measure_value:
                #print("sumbeats %f i %d" % (sumBeats,i))
                
                if i < len(self.chordsReadable):
                    list.append(self.chordsReadable[i])
                    
                    if len(self.chordsReadable[i]) > 0:
                        sumBeats += self.chordsReadable[i][0]
                    
                i += 1
            self.measures.append(Measure(list,len(self.measures)+1))
    def createChords(self,mid):
        for msg in mid:
            if not msg.is_meta and msg.type == "note_on" or msg.type == "note_off":
                if "note" in msg.dict():
                    midiNum = msg.dict()['note']
                    note = Note(midiNum)
                    duration = roundToMultiple((mido.second2tick(msg.time,mid.ticks_per_beat,self.tempo)/mid.ticks_per_beat)/self.timeSignature[1],1/(self.timeSignature[1]*4)) #rounds to multiple of an eighth note
                    print("%s %f %s" % (msg.dict(),duration,note.noteName))
                    if duration > 0:
                        if msg.type == "note_on": #if it is a new note and  the time between the last msg is greater than zero, this indicates a new chord
                            self.chords.append(Chord([note],duration))
                        elif msg.type == "note_off": #if its a note off, this also indicates a new chord, but we have no harmonic info about it yet
                            if len(self.chords) == 0:
                                self.chords.append(Chord([note],duration))
                            else:
                                self.chords.append(Chord([],duration))
                    elif msg.type == "note_on" and duration <= 0: #if its a new note and the time between the last message is 0, this indicates that we are still on the same chord. We add the note to the current chord.
                        lastIndex = len(self.chords) - 1
                        if lastIndex >= 0:
                            self.chords[lastIndex].notes += [note]
                        elif lastIndex < 0:
                            self.chords.append(Chord([note],1))
            else: #for some reasons there are sometimes meta messages in between note_on and note_off msgs that indicate how much time has passed. These have no harmonic information but indicate that a new chord has begun.
                duration = roundToMultiple((mido.second2tick(msg.time,mid.ticks_per_beat,self.tempo)/mid.ticks_per_beat)/self.timeSignature[1],1/(self.timeSignature[1]*4)) #rounds to multiple of an eighth note
                if duration > 0:
                    self.chords.append(Chord([],duration))

class Note:
    def __init__(self,midiNum):
        self.midiNum = midiNum
        self.frequency = self.getFrequency()
        self.noteName = self.midiNumToNote()
    def __eq__(self, obj) -> bool:
        return isinstance(obj,Note) and self.noteName == obj.noteName
    def getFrequency(self): 
        return (2 ** ((self.midiNum - 69)/12)) * 440
    def midiNumToNote(self): #converts a MIDI number to a string in the format f"NoteNameOctave"
        str = ""
        remainder = (self.midiNum - 21) % 12
        octave = (self.midiNum - 12) // 12
        if remainder == 0:
            str += "A"
        elif remainder == 1:
            str += "Bb"
        elif remainder == 2:
            str += "B"
        elif remainder == 3:
            str += "C"
        elif remainder == 4:
            str += "C#"
        elif remainder == 5:
            str += "D"
        elif remainder == 7:
            str += "E"
        elif remainder == 8:
            str += "F"
        elif remainder == 9:
            str += "F#"
        elif remainder == 10:
            str += "G"
        elif remainder == 11:
            str += "A"
        return "%s%d" % (str,octave)

class Chord:
    def __init__(self,notes,duration):
        self.notes = notes
        self.duration = duration
class Measure:
    def __init__(self,chordsReadable,positionInSong):
        self.chordsReadable = chordsReadable
        self.positionInSong = positionInSong

#GUI objects

class Screen():
    def __init__(self):
        self.buttons = []
        self.currentMeasure = 0
    """
    def addButton(self):
        print(len(self.buttons) * SCREEN_UNIT_HEIGHT)
        if len(self.buttons) == 0:
            self.buttons.append(Button(self.surface,(SCREEN_WIDTH,SCREEN_UNIT_HEIGHT),0,0))
        else:
            self.buttons.append(Button(self.surface,(SCREEN_WIDTH,SCREEN_UNIT_HEIGHT),0,len(self.buttons)))
    """
    def nextMeasure(self):
        self.currentMeasure += 1
    def prevMeasure(self):
        self.currentMeasure -= 1

class Button(pygame.sprite.Sprite):
    def __init__(self,win, scale, x, y):
        super(Button, self).__init__()

        self.surface = pygame.Surface(scale, pygame.SRCALPHA)
        self.win = win
        self.scale = scale
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.positionOnScreen = y
        self.rect.y = self.positionOnScreen * SCREEN_UNIT_HEIGHT

    def draw(self):
        pygame.draw.rect(self.surface, PURPLE,(0,0,SCREEN_WIDTH,SCREEN_UNIT_HEIGHT * self.positionOnScreen),border_radius=25)
        self.win.blit(self.surface,self.rect)