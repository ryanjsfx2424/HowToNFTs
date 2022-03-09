## converter.py
"""
The purpose of this script is to convert gifs to mp4s.
"""
import os

os.system("mkdir -p nftmp4s")
for ii in range(1,25):
  os.system('ffmpeg -i nftgifs/HowToKarate' + str(ii) + '.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" nftmp4s/HowToKarate' + str(ii) + '.mp4')
# end for ii
## end converter.py
