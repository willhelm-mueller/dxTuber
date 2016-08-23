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
# This script converts PDB files into OpenDX files, optionally a previously group can be set. Use this tool only for pdb files dxtuber previously created.
#
# v0.084  
#  +settings are stored now in pdb files
#  +filter by density

import sys, os
from lib.tubedx import *
from lib.buildopendx import *
from lib.readpdb import *
from lib.writedx import *



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
	sys.argv[1] #pdb file
	sys.argv[2] #dx file
except IndexError:
	print "\nThis script converts PDB files into OpenDX files, optionally a group ca be given as argument .\n\nusage:\npdb2dx <input-pdbfile> <output-dxfile> (group)\n<> Mandatory parameters \n() Optional parameters\n\n"
	sys.exit()
try:
	sys.argv[3]
	group = sys.argv[3]
except:
	group = 0
	
print "Reading..."
readPDB = ReadPDB (sys.argv[1])
if readPDB.readPDB() == 0:
	dxObject = readPDB.getDxObject()
else:
	print "Can not read pdb file"
	sys.exit()
# only selected group gets densities > 0 
if group:
	print "Extracting group id: "+ sys.argv[3]
	voxelGroupGrid = readPDB.getTubeDxObject().getVoxelGroupGrid() #[x][y][z] = group
	densityArray = dxObject.getDensity() #[x][y][z] = density
	for  xCount in range (len (densityArray)):
		for  yCount in range (len (densityArray[0])):
			for zCount in range (len (densityArray[0][0])):
				if sys.argv[3] != voxelGroupGrid[xCount][yCount][zCount]:
					densityArray[xCount][yCount][zCount]=0
	dxObject.setDensity(densityArray)	
saveToDx = WriteDx (dxObject)
saveToDx.write(sys.argv[2])
print "Done"


