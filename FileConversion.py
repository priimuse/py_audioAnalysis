from moviepy.editor import * #v 1.0.3
import sys
import os

def main(inF):
  extension = inF.split('.')[-1]
  if extension != "mp3":
    outF = inF.replace("." + extension, ".mp3")
    vid = VideoFileClip(inF)
    vid.audio.write_audiofile(outF)
    
    if os.path.exists(outF): print(outF)
  else: print(inF)

main(sys.argv[1])
