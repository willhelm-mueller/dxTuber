#!/usr/bin/env python
#	 This file is part of the dxTuber package
#    Copyright (C) 2010-2013  Martin Raunest
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###
# This script converts OpenDX files into PDB files, optionally a threshold for minimim atoms per voxel can be set.
#
# v0.084  
#  +settings are stored now in pdb files
#  +filter by density

import sys, os
from lib.readopendx import *
from lib.writepdb import *
from lib.tubedx import *
from lib.buildopendx import *





dxTuberConfFile = os.environ['HOME']+"/.dxTuber/dxTuber.conf"
conf = open (dxTuberConfFile,'r')
confLines = conf.readlines()
for line in confLines:
	if re.match ('^#',line):
		continue
	if re.match('VERSION',line):
#				print line
		tmpArray = re.split('\s',line,1)
		tmp = re.sub('\"','',tmpArray[1])
		tmp = re.sub('\n','',tmp)
		version = re.sub('^\s','',tmp)
print "dxTuber v" + version 


try:
	sys.argv[1]
	sys.argv[2]
except IndexError:
	print "\nThis script converts OpenDX files into PDB files, optionally a threshold for minimim atoms per voxel can be set.\n\nusage:\ndx2pdb <input-dxfile> <output-pdbfile> (minimum-residence-probabilities)\n<> Mandatory parameters \n() Optional parameters\n\n"
	sys.exit()

#print "dxTuber v" + version 
print "Reading..."
readDx = ReadOpenDx (sys.argv[1])
readDx.importDx()
#tubeDx = TubeDx (openDxObject = readDx.getDxObject(), filename = sys.argv[1],version = version,scanned = 'converted')
filter = 1
try:
	sys.argv[3]
except:
	filter = 0

if filter == 1:
	tubeDx = TubeDx (openDxObject = readDx.getDxObject(), filename = sys.argv[1],version = version,scanned = 'converted', solventThreshold = sys.argv[3])
	print "Minimum residence probability: "+sys.argv[3]
	print "Start filtering..."
	densities = tubeDx.getDxObject().getDensity()
	densities_filtered = [[[-1 for zR in range(len (densities[0][0]))] for yR in range(len (densities[0]))] for xR in range(len (densities))]
	for  xCount in range (len (densities)):
		for  yCount in range (len (densities[0])):
			for zCount in range (len (densities[0][0])):
				if float(densities[xCount][yCount][zCount]) > float(sys.argv[3]):
					densities_filtered[xCount][yCount][zCount] = densities[xCount][yCount][zCount]
			outputLine = int ((xCount*100)/len(densities))
			print str(outputLine)+" %\r",
	tmp = (BuildOpenDx (density = densities_filtered,  stepSize = tubeDx.getDxObject().getStepsize(), origin = tubeDx.getDxObject().getOrigin(),dimention = tubeDx.getDxObject().getDimention()))
	tubeDx.setDxObject(tmp)
	print "Done"
else:
	tubeDx = TubeDx (openDxObject = readDx.getDxObject(), filename = sys.argv[1],version = version,scanned = 'converted')
print "Saving..."
savePDB = WritePDB (tubeDx)
savePDB.write(sys.argv[2])
print "Done"
