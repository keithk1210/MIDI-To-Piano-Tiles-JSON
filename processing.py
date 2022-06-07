import json
from objects import Song
import mido

from utils import roundToMultiple



def myround(x, base=5):
    return int(base * round(float(x)/base))

def createSong(midi,name,has_pickup,time_signature_string,pickup_duration=None):
    tempo = 0
    time_signature_list = time_signature_string.split(",")
    timeSignature = (int(time_signature_list[0]),int(time_signature_list[1]))

    for msg in midi: 
        if msg.is_meta:
            if msg.type == "set_tempo":
                tempo = msg.dict()['tempo']
    print(timeSignature)
    return Song(timeSignature,tempo,name,has_pickup,pickup_duration)

def writeJSON(song):
    measuresSerializable = []
    info_serializable = [["Tempo",song.tempo],["Time Signature",song.timeSignature],"Has Pickup",song.has_pickup]
    for i in range(0,len(song.measures)):
        measuresSerializable.append(["Measure %d/%d" % (song.measures[i].positionInSong,len(song.measures))] + song.measures[i].chordsReadable)
    dictionary = {
        "Info": info_serializable,
        song.name : measuresSerializable
    }
    json_object = json.dumps(dictionary, indent = 1)
    with open(f"songs/{song.name}.json","w") as outfile:
        outfile.write(json_object)

def openJSON(jsonFileName):
    notes_dict = {}
    with open(jsonFileName.replace("\\","\\\\"),"r") as outfile:
        notes_dict = json.load(outfile)
    return notes_dict

    


