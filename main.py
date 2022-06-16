from ast import keyword
from dis import dis
from mido import MidiFile
from processing import *
from resources import *
from objects import *
import pygame
import easygui

#TO do
#make it work with 3/8

#MAYBE_DO
#ask the user: What is the shortest note value in this song? (aka quantization)
#figure out how to make moonlight sonata movement one work

button_list = ("Create JSON", "Open JSON")

userChoice = easygui.buttonbox(msg="What would you like to do?",choices=button_list)

measuresDisplay = []

create_mode = False
open_mode = False

if userChoice == "Create JSON":
    create_mode = True
elif userChoice == "Open JSON":
    open_mode = True


if create_mode:

    midiFileName = easygui.fileopenbox(msg="Please select a MIDI file",default='MIDIs\\*.mid',filetypes=["*.mid"])

    midi = MidiFile(midiFileName.replace("\\","\\\\"),clip=True)
    songName = easygui.enterbox("Enter the name of the JSON file you would like to create",title="Enter text")
    pickup = easygui.ynbox("Does this song have a pickup/anacrusis? \n(Does it start on beat other than beat 1?)")
    if pickup:
        pickup_amount = easygui.enterbox("How many beats is the pickup? \n(Enter this as a decimal - i.e. and eigth note in 4/4 is worth .125 beats, a sixteenth note in 3/8 is worth .5 beats. In other words, the rhythmic value that gets the beat is 1, and everything else is a fraciton of that.)")
    time_signature_str = easygui.enterbox("What is this song's time signature? (Enter two digits separated by a comma)")
    quantization = easygui.choicebox(msg="What is the quantization for this song?",choices=["1/4 Note","1/8 Note","1/16 note","1/32 note","1/64 note"])
    if pickup:
        song = createSong(midi,songName,pickup,time_signature_str,quantization,float(pickup_amount))
    else:
        song = createSong(midi,songName,pickup,time_signature_str,quantization)
    song.createChords(midi)
    song.createMeasures()

    sumBeats = 0

    for i in range(0,len(song.measures)):
        measuresDisplay.append("")

    for i in range(0,len(song.measures)):
        measuresDisplay[i] += "Measure %d/%d\n" % (i+1,len(song.measures))
        for j in range(0,len(song.measures[i].chordsReadable)):
            if len(song.measures[i].chordsReadable[j]) > 0:
                measuresDisplay[i] += "Duration: %.4f of a measure\nNotes:\n" % (song.measures[i].chordsReadable[j][0])
            else:
                measuresDisplay[i] += "N/A\n"
            measuresDisplay[i] += "%s\n" % (str(song.measures[i].chordsReadable[j][1:len(song.measures[i].chordsReadable[j])]))
            if j != len(song.measures[i].chordsReadable) - 1:
                measuresDisplay[i] += "---\n"
elif open_mode:

    jsonFileName = easygui.fileopenbox(msg="Please select a JSON file",default='songs\\*.json')
    print(jsonFileName)
    song_dict = openJSON(jsonFileName)
    song_info = []
    for key in song_dict: #gets the info from the dictionary
        song_info = song_dict[key]
    print(song_info)

    for i in range(0,len(song_info)):
        measuresDisplay.append("")

    for i in range(0,len(song_info)):
        measuresDisplay[i] += "%s\n" % (song_info[i][0])
        for j in range(1,len(song_info[i])):
            if len(song_info[i][j]) > 0:
                measuresDisplay[i] += "Duration: %.4f of a measure\nNotes:\n" % (float(song_info[i][j][0]))
            else:
                measuresDisplay[i] += "N/A\n"
            measuresDisplay[i] += "%s\n" % (str(song_info[i][j][1:len(song_info[i][j])]))
            if j != len(song_info[i]) - 1:
                measuresDisplay[i] += "---\n"
        


#initializing display
button_list =  ["Previous","Next","Write JSON","Quit"]
screen = Screen()
buttonBox = ""
while buttonBox != "Quit":
    buttonBox = easygui.buttonbox(msg=measuresDisplay[screen.currentMeasure],choices=button_list,title="JSON preview")
    if buttonBox == "Next":
        if screen.currentMeasure + 1 < len(measuresDisplay):
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




