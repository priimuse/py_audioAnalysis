import librosa #v 0.10.1
import sys
import math
import numpy as np

def main():
    inF = ""
    potentials = os.listdir(os.path.join(os.getcwd(), "temp"))
    for each in potentials:
        each_split = each.split('.')
        if each_split[0] == "out" and each_split[1] == "mp3":
            inF = os.path.join(os.getcwd(), "temp", each)
    if inF == "":
        print("! no valid file found to process in dir " , os.getcwd(), " leaving early !")
        return None
    else:
        print("given in file:\n", inF)
        #load into librosa and perform analysis
        duration = 20
        step = 5
        offset = 0
        totalD = math.floor(librosa.get_duration(path=inF))
        print("total duration: ", totalD)
        allY, allSr = librosa.load(inF)
        allTempo, allBeats = librosa.beat.beat_track(y=allY, sr=allSr)
        print("average tempo: ", allTempo)
    
        while (offset < totalD):
            y, sr = librosa.load(inF, offset=offset, duration=duration)
            C = np.abs(librosa.cqt(y=y, sr=sr))
            onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median, fmax=8000, n_mels=256)
            tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
            print("@ offset: ", offset, "tempo: ", tempo)
            offset += step

main()
