import sys
import re

if len(sys.argv) < 2 :
	print 'Please specify the name of the file'

def getScan(input) :
	signals = input.split("\r\n\r\n")
	scan = [None] * (len(signals) - 1)
	for i in range(1, len(signals)) :
		perScanData = re.split("[\r\n|,]", signals[i])
		intensity = float(perScanData[1].strip(" intensity = "))
		mass = float(perScanData[2].strip(" mass/position = "))
		scan[i - 1] = (mass, intensity)
	return scan

def getScanTitle(input) :
	title = "ITMS + p NSI Full "
	arr = re.split("[\r\n|,]", input)
	startMass = 0
	endMass = 0
	precursors = []
	energies = []
	for item in arr :
		if item.startswith(" start_mass= ") :
			startMass = float(item.strip(" start_mass= "))
		elif item.startswith(" end_mass = ") :
			endMass = float(item.strip(" end_mass = "))
		elif item.startswith("Precursor Mass  "):
			precursors = item.strip("Precursor Mass  ").split("  ")
		elif item.startswith("Collision Energy  ") :
			energies = item.strip("Collision Energy  ").split("  ")
	
	for i in range(0, len(precursors)) :
		title += "ms" + str(2 + i) + " " + str(precursors[i]) + "@cid" + str(energies[i]) + " "
	title += "[" + str(startMass) + "-" + str(endMass) + "]"
	return title

def getRT(input) :
	arr = re.split("[\r\n|,]", input)
	for item in arr :
		if item.startswith("start_time = ") :
			return float(item.strip("start_time = "))
	return 0

with open(sys.argv[1], "r") as fp :
	data = fp.read().strip().split("\r\n\r\n\r\n")
	scanTitle = getScanTitle(data[1].split("\r\n\r\n")[0])
	scans = [getScan(input) for input in data[1: len(data)]]

	# Average scans
	totalIntensities = [0] * len(scans[0])
	for scan in scans :
		for i in range(0, len(scan)) :
			totalIntensities[i] += scan[i][1]

	with open(sys.argv[1] + ".average", "w") as fout :
		fout.write("SPECTRUM - MS\t \n")
		fout.write(sys.argv[1] + "\t \n")
		fout.write(scanTitle + "\t \n")
		fout.write("Scan#:1-" + str(len(scans)) + "\t \n")
		rtStart = getRT(data[1].split("\r\n\r\n")[0])
		rtEnd = getRT(data[-1].split("\r\n\r\n")[0])
		fout.write("RT: " + str(rtStart) + "-" + str(rtEnd) + "\t \n")
		fout.write("AV: " + str(len(scans)) + "\t \n")
		fout.write("Data points: " + str(len(totalIntensities)) + "\t \n")
		fout.write("Mass\tIntensity\n")
		for i in range(0, len(scans[0])) :
			averageIntensity = totalIntensities[i] / len(scans)
			fout.write(str(scans[0][i][0]) + "\t" + str(averageIntensity) + "\n")
