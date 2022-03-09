## backend.py
"""
The purpose of this script is to continuously monitor the blockchain to
1) determine if a holder aquires or loses an NFT:
2) if they do, generate a new image/movie for the tokens they hold,
3) upload the new image/movie to the hosting service
4) update the metadata file
Repeat :)

(The above ordering matters!)
"""

## use python3!!!
import os
import io
import json
from web3 import Web3

## PARAMETERS
DEPLOYER_ADDRESS = "0x01656d41e041b50fc7c1eb270f7d891021937436"
INFURA_URL = "https://rinkeby.infura.io/v3/37de3193ccf345fe810932c3d0f103d8"

EXT_IMG      = ".mp4"
EXT_METADATA = ".json"

ADDRESS   = "0xb552E0dDd94EA72DBc089619115c81529cd8CA70" # address for deployed smart contract

## web3 stuff
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

with open("../contract/abi_v020.json", "r") as fid:
  rl = "".join(fid.readlines())
  abi = json.loads(rl)
# end with open

## goal is to update token URI based on how many are held
## by that owner (but deployer doesn't count!)
contract = w3.eth.contract(address=ADDRESS, abi=abi)

totalSupply = contract.functions.totalSupply().call()
print("total supply: ", totalSupply)

for ii in range(totalSupply):
  token = contract.functions.tokenByIndex(ii).call()
  owner = contract.functions.ownerOf(token).call()
  tokenList = contract.functions.walletOfOwner(owner).call()

  ## string comparison fails for some mysterious reason
  if int(owner,16) == int(DEPLOYER_ADDRESS,16):
    tokenList = [ii+1]
  # end if

  print("token: ", token)
  print("owner: ", owner)
  print("tokenList: ", tokenList)

  newTokenName = str(token)
  for jj in range(len(tokenList)):
    if tokenList[jj] != token:
      newTokenName += "_" + str(tokenList[jj])
    # end if
  # end for jj
  print("newTokenName: ", newTokenName)

  ## first, check if metadata on hosting service has newTokenName.
  ## if so, we're good! If not, update it!
  old_foos = []
  metadata_correct = False

  os.system("gsutil ls gs://how-to-nfts-metadata/foo" + str(token) + ".txt"
            + " > foo_file0.txt")
  os.system("gsutil ls gs://how-to-nfts-metadata/foo" + str(token) + "_*.txt"
            + " > foo_file1.txt")

  for jj in range(2):
    with open("foo_file" + str(jj) + ".txt", "r") as fid:
      for line in fid:
        old_foos.append(line)
        if "foo" + newTokenName + ".txt" in line:
          metadata_correct = True
        # end if
      # end for
    # end with
    os.system("rm foo_file" + str(jj) + ".txt")
  # end for jj
  print("old_foos: ", old_foos)

  if metadata_correct:
    print("metadata correct (supposedly) so skipping")
    continue
  # end if

  if len(old_foos) > 1:
    print("error! only expected one old foo file.")
    raise
  # end if
  old_foo = old_foos[0][:-1] # strip trailing newline character
  old_foo = old_foo.split("metadata/")[1]
  print("old_foo: ", old_foo)

  ## evidently metadata is not correct...
  ## first, we generate a new movie (if needed) and rsync with
  ## the GCP bucket.
  ## then, we'll update the metadata file, remove the old foo
  ## file and touch a new one
  ## then we'll rsync the metadata folder with the bucket.

  target      = "../nftmp4s/HowToKarate" + str(token) + ".mp4"
  destination = "../nftmp4s/HowToKarate" + newTokenName + ".mp4"
  if not os.path.exists(destination):
    os.system("cp " + target + " " + destination)
    for jj in range(len(tokenList)):
      if tokenList[jj] != token:
        print("destination: ", destination)
        print("tokenList[jj]: ", tokenList[jj])
        os.system('ffmpeg -y -i ' + destination + ' -i nftmp4s/HowToKarate' + str(tokenList[jj]) + '.mp4' + \
              ' -filter_complex "[0:v] [1:v]' + \
              ' concat=n=2:v=1 [v]"' + \
              ' -map "[v]" ' + "concat.mp4")
        os.system("mv concat.mp4 " + destination)
      # end if
    # end for jj
    ## note, can rsync in parallel via rsync -m...
    os.system("gsutil rsync ../nftmp4s/ gs://how-to-nfts-data/")
  # end if
  
  ## next, we'll update the metadata file, remove the old foo
  ## file and touch a new one
  ## then we'll rsync the metadata folder with the bucket.
  os.system("cp ../metadata/" + str(token) + ".json temp.json")
  with open("../metadata/" + str(token) + ".json", "w") as fid_write:
    with open("temp.json", "r") as fid_read:
      for line in fid_read:
        if '"image":' in line:
          line = line.split("HowToKarate")[0] + "HowToKarate" + \
                 str(newTokenName) + '.mp4",\n'
        # end i
        fid_write.write(line)
      # end for line
    # end with open write
  # end with open read
  os.system("rm temp.json")
  os.system("touch ../metadata/foo" + str(newTokenName) + ".txt")
  os.system("rm ../metadata/" + old_foo)

  ## last, we need to update the _metadata file and then rsync.
  with open("../metadata/_metadata.json", "w") as fid_write:
    fid_write.write("{\n")
    for jj in range(1,25):
      with open("../metadata/" + str(jj) + ".json", "r") as fid_read:
        for line in fid_read:
          if "}" in line and len(line) == 2 and jj != 24:
            line = "},\n"
          # end if
          fid_write.write(line)
        # end for
      # end with open
    fid_write.write("}")
  # end with open

  os.system("gsutil rsync -d ../metadata/ gs://how-to-nfts-metadata/")
# end for ii
## end test.py
