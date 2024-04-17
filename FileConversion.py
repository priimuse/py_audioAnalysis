from moviepy.editor import * #v 1.0.3
import sys

def main(argsList):
  inF = argsList[1]
  extension = inF.split(".")[-1]
  outF = inF.replace("." + extension, ".mp3")
  vid = VideoFileClip(inF)
  vid.audio.write_audiofile(outF)
  if os.path.exists(outF): return outF
  else: return None

ret = main(sys.argv)
print("file converted to ", ret)
