import os
import re
import sys

if len(sys.argv) < 2 :
  print "python grepEnergy.py folderName"

os.system("grep 'SCF Done' " + sys.argv[1] + "/*.log >tmpGrepEnergy.tmp")
data = []
with open("tmpGrepEnergy.tmp", "r") as fin :
  for line in fin :
    arr = re.split(" +", line.strip())
    fnumber = int(arr[0].rstrip(".log:").split("_")[-1])
    fdata = arr[0] + "\t" + arr[5] + "\n"
    data.append((fnumber, fdata))
os.system("rm tmpGrepEnergy.tmp")
def getKey(item) :
  return item[0]
data = sorted(data, key=getKey)

with open(sys.argv[1] + "_energy.tsv", "w") as fout :
  for item in data :
    fout.write(item[1])


