#!/usr/bin/env python
#
#	 This file is part of the dxTuber package
#    Copyright (C) 2010-2013 Martin Raunest
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
#


#
# v0.23
#  +distcutoff parameter can now be set via cmd
#
#
# v0.2 
#  + shell script to postgroup cavities into subcavities. 
#
#
#

import os
import subprocess
from lib.readpdb import *
from lib.writepdb import *

from lib.buildopendx import *
from lib.tubedx import *

from lib.postgroup import *



#########
# Get dxTuber settings
#########



dxTuberConfFile = os.environ['HOME']+"/.dxTuber/dxTuber.conf"
conf = open (dxTuberConfFile,'r')
confLines = conf.readlines()

for line in confLines:
	if re.match ('^#',line):
		continue
	if re.match('VERSION',line):
		tmpArray = re.split('\s',line,1)
		tmp = re.sub('\"','',tmpArray[1])
		tmp = re.sub('\n','',tmp)
		version = re.sub('^\s','',tmp)

####
# Deal with arguments
####

######################################################################
# If argparse is not installed global, get a static lib				 #
# and import it manually (static)									 #
#                                                                    #
# http://packages.ubuntu.com/lucid/python-argparse                   #
# http://code.google.com/p/argparse/                                 #
#																     #
# maybe this helps for implementation ... 							 # 
# 																	 # 
# sys.path.append('path_to_argparse_lib')							 
# from argparse import *												 
#																	 #
######################################################################


try:
	import argparse 
	parser = argparse.ArgumentParser(description='''"--cubicsize" defines the number of voxels in each direction, e.g: 2 => 2 in +x and -x, +y and -y, +z and -z direction defining a 5x5x5 cube with 125 voxels
		
"-t" sets the minimum amount of neighboars in the "--cubicsize" defined cube as a threshold for the core cavities''',
	epilog='There is no spoon',formatter_class=argparse.RawTextHelpFormatter )
except ImportError : 
	sys.path.append('/home/bit/raunest/programms/python/scripts/lib')    ## if argparse is not installed global you can use it in a static way
	from argparse import *												 
	parser = ArgumentParser(description='"--cubicsize" defines the number of voxels in each direction, e.g: 2 => 2 in +x and -x, +y and -y, +z and -z direction defining a 5x5x5 cube with 125 voxels\n\n"-t" sets the minimum amount of neighboars in the "--cubicsize" defined cube as a threshold for the core cavities',epilog='There is no spoon',formatter_class=RawTextHelpFormatter )

parser.add_argument('--ipdb', default=False,help='PDB inputfile (only previously via dxTuber created pdb files are supported)') 
parser.add_argument('--opdb', default=False, help='PDB outfile') 
parser.add_argument('--cid', default='all', help='Cavity ID to postgroup, use "all" if all cavities should be processed (default="all")') 
parser.add_argument('--cubicsize', default='2', help='edge length default 2 Voxels => Volume => 125 Voxels ... [INT] ') 
parser.add_argument('-t','--threshold', default='100', help='Minimum amount of neighbors in --cubicsize to calc "core" cavities (default = 100)') 
parser.add_argument('-d','--distcutoff', default='8', help='Cubic size for reprouping the non core voxels. This routine checks each core voxel per default in +8 and -8 in xyz for non core ISVs.') 

args = parser.parse_args()

if not args.ipdb or not args.opdb:
		sysRun = subprocess.Popen([sys.argv[0], '-h'])
		sysRun.communicate()
		print "Please specify input and output by '--ipdb' and  '--opdb'\n"
		sys.exit()



readPDB = ReadPDB(args.ipdb)
readPDB.readPDB()
cavitiesTubeObject = readPDB.getTubeDxObject()
cavitiesDxObject = readPDB.getDxObject()

### Densities contain now information about each voxels " neighborhood "
postGroup = PostGroup ( cavitiesTubeObject )

#oke testing now :)


# postGroupDensities = postGroup.calcNeighbors(cavityID = args.cid, edgeLength = int(args.cubicsize)) <-- works fine ! 
# postGroupDxObject = BuildOpenDx (density = postGroupDensities, 
#								stepSize = cavitiesDxObject.getStepsize(), 
#								origin = cavitiesDxObject.getOrigin(),
#								dimention = cavitiesDxObject.getDimention())
#






'''
postGroupTubeDx = TubeDx (
				openDxObject = postGroupDxObject, 
				filename = cavitiesTubeObject.getFilename(), 
				proteinObject= cavitiesTubeObject.getProteinObject(), 
				waterObject= cavitiesTubeObject.getWaterObject(), 
				scanMethod = cavitiesTubeObject.getScanMethod(), 
				scanned=cavitiesTubeObject.getScanned(),
				grouped='Yes', 
				groupes=None, 
				VoxelGroupGrid = None, 
				minDiameter = cavitiesTubeObject.getMinDiameter(), 
				protThreshold = cavitiesTubeObject.getProtThreshold(), 
				solventThreshold =cavitiesTubeObject.getSolventThreshold(), 
				version = version, 
				protFile =cavitiesTubeObject.getProtFile(), 
				solvFile = cavitiesTubeObject.getSolvFile(), 
				filterApplied = cavitiesTubeObject.getFilterApplied(), 
				)
'''
## tested ! until here  .... 				
				
postGroupTubeDx	= postGroup.postGroup_Neighbor(threshold =int(args.threshold), cavityID = args.cid, edgeLength = int(args.cubicsize) ,distCutoff =int(args.distcutoff))		
				
writePDB = WritePDB (postGroupTubeDx)
#writePDB.write(filename= "2"+args.opdb)
writePDB.writeGroups(groupArray=  postGroupTubeDx.getGroupes(), filename= args.opdb)

print "Done"


