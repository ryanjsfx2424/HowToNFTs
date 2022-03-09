import os
os.system('ffmpeg -i nftmp4s/HowToKarate1.mp4 -i nftmp4s/HowToKarate2.mp4' + \
            ' -filter_complex "[0:v] [1:v]' + \
            ' concat=n=2:v=1 [v]"' + \
            ' -map "[v]" nftmp4s/HowToKarate1_2.mp4')

