import math
import re
import sys

if len(sys.argv) < 5 :
  print "Usage: python measureDistances.py energyFile comFileFolder pairFile outputFile"
  sys.exit()

class ComFileHandler:
  coordinates = None
  
  def __init__(self, comFile):
    with open(comFile, "r") as fin:
      data = []
      for line in fin:
        if line.strip() == "":
          continue
        if line.startswith("  "):
          arr = re.split(" +", line.strip())
          if len(arr) == 4:
            x = float(arr[1])
            y = float(arr[2])
            z = float(arr[3])
            data.append((x, y, z))
      self.coordinates = data

  def getDistance(self, atomA, atomB):
    if atomA > len(self.coordinates) or atomB > len(self.coordinates):
      raise Exception("The given atom number exceeds the maximum atom number in file")
    coordA = self.coordinates[atomA]
    coordB = self.coordinates[atomB]
    distance = 	(coordA[0] - coordB[0]) ** 2
    distance += (coordA[1] - coordB[1]) ** 2
    distance += (coordA[2] - coordB[2]) ** 2
    return math.sqrt(distance)

outputFile = sys.argv[4]
comFileFolder = sys.argv[2]
pairs = []
with open(sys.argv[3], "r") as fin :
  for line in fin :
    arr = line.strip().split("\t")
    if len(arr) == 2 :
      pairs.append((int(arr[0]), int(arr[1])))

def getComFileName(inputFile) :
  fileName = re.split("/+", inputFile)[-1]
  snapName = fileName.split(".")[0]
  return snapName + ".com"

def printHeader(pairs) :
  headers = []
  headers.append("snap_file")
  headers.append("energy")
  for pair in pairs :
    headers.append(str(pair[0]) + "_" + str(pair[1]))
  return "\t".join(headers)

with open(sys.argv[1], "r") as fin :
  with open(outputFile, "w") as fout :
    fout.write(printHeader(pairs) + "\n")
    for line in fin :
      arr = line.strip().split("\t")
      if len(arr) < 2 :
        continue
      data = []
      currentEnergy = arr[1]
      comFileName = getComFileName(arr[0])
      data.append(comFileName)
      data.append(currentEnergy)
      comFileHandler = ComFileHandler(comFileFolder + "/" + comFileName)
      for pair in pairs :
        data.append(str(comFileHandler.getDistance(pair[0], pair[1])))
      fout.write("\t".join(data) + "\n")
        