import sys
import math
import os

if len(sys.argv) < 2 :
	print 'Please specify the name of the folder'
n = 0
for f in os.listdir(sys.argv[1]) :
	if f.endswith(".txt") :
		os.system("python average_spec.py " + sys.argv[1] + "/" + f)
		n += 1

files = [None] * n
curr = 0
for f in os.listdir(sys.argv[1]) :
	if f.endswith("average") :
		with open(sys.argv[1] + "/" + f, "r") as fin : 
			files[curr] = fin.read().split("\n")
			curr += 1

maxLine = 0
for f in files :
	maxLine = max(maxLine, len(f))

with open(sys.argv[1] + ".tsv", "w") as fout :
	for i in range(0, maxLine) :
		for f in files :
			if i >= len(f) :
				fout.write("\t\t\t\t\t")
			else : 
				fout.write(f[i] + "\t\t\t\t")
		fout.write("\n")







