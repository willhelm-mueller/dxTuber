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
#
#
# v0.25 
#
# -bug in cmd parameter check block (thx for the bug report:  Mattia Sturlese)
#
#
# v0.12
# +FilterByMinDens
# 
#
# v0.1
#  +cmd implementation of analyze tube 
#  
#
#

import sys
import os
import re
import subprocess
from lib.analysetube import *
from lib.readpdb import *
from lib.filterdx import *




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


import argparse 

parser = argparse.ArgumentParser(description='This tool is part of the dxTuber package. It is able to analyze previously grouped cavities along principle axis x, y and z. Based on the choosen -c cavity its cross sectioneal area is plotted against the -a axis. Output will be stored in -o OUT. (1st coloumn = axis, 2nd column = area)',epilog='dxTuber v' + version)
parser.add_argument('-p','--pdb', default=False, help='dxTuber grouped outfile')
parser.add_argument('-a','--axis', default=False,choices=('x','y','z'),help='Select an axis')
parser.add_argument('-c','--cavity',default=False, help='Cavity ID (Name column in PDB file)')
parser.add_argument('-o','--out',default=False, help='Output (1st column axis 2nd column area)')
#parser.add_argument('--mindens', help='Minimum density')


args = parser.parse_args()
'''
args.pdb     grouped outfile
args.axis    axis
args.cavity  cavity ID
args.out     outfile
#args.mindens

'''

if not args.pdb or not args.axis or not args.cavity or not args.out:
	sysRun = subprocess.Popen([sys.argv[0], '-h'])
	sysRun.communicate()
	sys.exit() 
	

readPDB = ReadPDB (args.pdb)
readPDB.readPDB()
tuberObj = readPDB.getTubeDxObject()


if not tuberObj.getGroupes():
	sysRun = subprocess.Popen([sys.argv[0], '-h'])
	sysRun.communicate()
	print "Please choose a previously grouped PDB file"
	print "Ensure that your cavity id start with '0'"
	sys.exit()



#if 	args.mindens:
#	filterThis = FilterDx(dxObjectTube = tuberObj.getDxObject())
#	filterThis.filterByDensity( tubeDxObj= tuberObj, densityThreshold=args.mindens)
#	tuberObj.setDxObject(filterThis.getDxObject())

analyse = AnalyseTube (tuberObj.getVoxelGroupGrid(),int(args.cavity))
analyse.analyseTubeArea(args.axis )
analyse.writeStatistics(args.out)






