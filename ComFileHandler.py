# This class parse .com file, calculate atom pair distances
import re
import math

class ComFileHandler:
  coordinates = null
  
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