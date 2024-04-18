from moviepy.editor import * #v 1.0.3
import sys
import os

def main():
  inPath = os.path.join(os.getcwd(), "temp")
  inF = ""
  outF = ""
  potentials = os.listdir(inPath)
  for each in potentials:
    each_split = each.split('.')
    if each_split[0] == "out":
      inF = os.path.join(inPath, "out." + each_split[1])
      extension = each_split[1]
      break

  if inF != "":
    outF = inF.replace("." + extension, ".mp3")
    vid = VideoFileClip(inF)
    vid.audio.write_audiofile(outF)
  
  if outF != "" and os.path.exists(outF): return outF
  else: return None

print("file converted to ", main())
