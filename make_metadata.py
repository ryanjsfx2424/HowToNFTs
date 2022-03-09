## make_metadata.py
"""
The purpose of this script is to generate metadata for all the gifs.
"""
import os
import glob

os.system("mkdir -p metadata")
os.chdir("metadata")

IMG_URI = "https://drive.google.com/drive/u/1/folders/1rA_dxqeL0TApAxRwZPGeK7sr8iJdaUXb"
<<<<<<< HEAD
IMG_URI = "https://storage.googleapis.com/how-to-nfts-data"

=======
>>>>>>> 5081ce4afe167c573bcb4312aad6ed6b55704ea7
IMG_URI += "/HowToKarate"
EXT = ".mp4"
changes = {
           "name" : ['  "name":"how to #' + str(ii) + '",\n' for ii in range(0,26)],
           "description" : ['  "description":"pithy description on how to #' + str(ii) + '",\n' for ii in range(0,26)],
           "image" : ['  "image":"' + IMG_URI + str(ii) + EXT + '",\n' for ii in range(0,26)],
           "edition" : ['  "edition":' + str(ii-1) + ',\n' for ii in range(0,26)]
          }

with open("_metadata.json", "w") as fid_write_global:
  fid_write_global.write("[\n")
  with open("1.json", "r") as fid_template:
    for line in fid_template:
      fid_write_global.write(4*" " + line)
    # end for
  # end with

  for ii in range(2,25):
    with open("1.json", "r") as fid_template:
      with open(str(ii) + ".json", "w") as fid_write_local:
        for line in fid_template:
          for key in changes.keys():
            if key in line:
              line = changes[key][ii]
            # end if
          # end for keys
          fid_write_local.write(line)
<<<<<<< HEAD
          if "}" in line and len(line) == 2 and ii != 24:
            line = "},\n"
=======
>>>>>>> 5081ce4afe167c573bcb4312aad6ed6b55704ea7
          fid_write_global.write(4*" " + line)
        # end for line in fid_template
      # end with open fid_write_local
    # end with open fid_template
  fid_write_global.write("]")
# end with open _metadata.json
