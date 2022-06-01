import json
from objects import Song
import mido

from utils import roundToMultiple



def myround(x, base=5):
    return int(base * round(float(x)/base))

def createSong(midi,name):
    tempo = 0
    timeSignature = (0,0)
    for msg in midi: 
        if msg.is_meta:
            if msg.type == "time_signature":
                timeSignature = (msg.dict()['numerator'],msg.dict()['denominator'])
            if msg.type == "set_tempo":
                tempo = msg.dict()['tempo']
    return Song(timeSignature,tempo,name)

def writeJSON(song):
    song.writeChordsReadable()
    print(song.chordsReadable)
    dictionary = {
        song.name : song.chordsReadable
    }
    json_object = json.dumps(dictionary, indent = 1)
    with open(f"songs/{song.name}.json","w") as outfile:
        outfile.write(json_object)

def openJSON(song):
    notes_dict = {}
    with open(f"songs/{song.name}.json","w") as outfile:
        notes_dict = json.load(outfile)
    return notes_dict

    


