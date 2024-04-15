print("Hello World!")

import librosa
import numpy as np

randA = np.random.randint(-1, high=1, size=2049).astype("float32")
tempe, beats = librosa.beat.beat_track(y=randA, sr=22050)
print("tempo: ", tempo)
print("beats: ", beats)
