from dis import dis
from mido import MidiFile
from processing import *
from resources import *
from objects import *
import pygame
import easygui

#setting up files and such

midiFileName = easygui.fileopenbox(msg="Please select a MIDI file",default='C:\\Users\\keith\\coding-projects\\Python\\MIDI_To_Piano_Tiles_JSON\\MIDIs\\*.mid',filetypes=["*.mid"])

midi = MidiFile(midiFileName.replace("\\","\\\\"),clip=True)
songName = easygui.enterbox("Enter the name of the JSON file you would like to create",title="Enter text")
song = createSong(midi,songName)
song.createChords(midi)
song.createMeasuresReadable()
measuresDisplay = []

sumBeats = 0


for i in range(0,len(song.measuresReadable)):
    measuresDisplay.append("")

for i in range(0,len(song.measuresReadable)):
    measuresDisplay[i] += "Measure %d/%d\n" % (i+1,len(song.measuresReadable))
    for j in range(0,len(song.measuresReadable[i].chordsReadable)):
        if len(song.measuresReadable[i].chordsReadable[j]) > 0:
            measuresDisplay[i] += "Duration: %.4f of a measure\nNotes:\n" % (song.measuresReadable[i].chordsReadable[j][0])
        else:
            measuresDisplay[i] += "N/A\n"
        measuresDisplay[i] += "%s\n" % (str(song.measuresReadable[i].chordsReadable[j][1:len(song.measuresReadable[i].chordsReadable[j])]))
        if j != len(song.measuresReadable[i].chordsReadable) - 1:
            measuresDisplay[i] += "---\n"


        


#initializing display
button_list =  ["Previous","Next","Write JSON","Quit"]
screen = Screen()
buttonBox = ""
while buttonBox != "Quit":
    buttonBox = easygui.buttonbox(msg=measuresDisplay[screen.currentMeasure],choices=button_list,title="JSON preview")
    if buttonBox == "Next":
        print("in")
        if screen.currentMeasure + 1 < len(song.measuresReadable):
            screen.nextMeasure()
    elif buttonBox == "Previous":
        if screen.currentMeasure - 1 >= 0:
            screen.prevMeasure()
    elif buttonBox == "Write JSON":
        writeJSON(song)
        break

"""
pygame.init()

FPS = 60
clock = pygame.time.Clock()

win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
win.fill(WHITE)
pygame.display.set_caption("MIDI to JSON converter")
screen = Screen(win)

for i in range(0,NUM_SCREEN_UNITS):
    screen.addButton()

running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for button in screen.buttons:
        button.draw()

    clock.tick(FPS)
    pygame.display.update()
    win.fill(WHITE)
pygame.quit()
"""




