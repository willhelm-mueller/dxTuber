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
# v0.2
# +yay lets start posst proccessing
#

import sys
import os
from lib.readopendx import *
from lib.writedx import *
from lib.writepdb import *
from lib.filterdx import *
from lib.readpdb import *
from lib.tubedx import *

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


import argparse 

parser = argparse.ArgumentParser(description='FilterVoxel was written to post proccess results of dxTuber:\nMin and max defines coordinates of an rectangle',epilog='dxTuber v' + version)

###
# for static libs use:
# parser = ArgumentParser(description='Command line version of dxTuber',epilog='dxTuber v' + version)
###
parser.add_argument('--idx',default=False,help='Input OpenDX file')
parser.add_argument('--ipdb',default=False,help='Input PDB file')
parser.add_argument('--odx',default=False,help='Output OpenDX file')
parser.add_argument('--opdb',default=False,help='Output PDB file')
parser.add_argument('-g', '--group', default=False,  action='store_const', const=True, help='-g enables grouping') 

parser.add_argument('--min',default=False,help='Array containing minimum "x y z" coordinates')
parser.add_argument('--max',default=False,help='Array containing maximum "x y z" coordinates')



args = parser.parse_args()

print args.min

if (not args.idx and not args.ipdb) or (args.idx and args.ipdb) :
	print "Define ONE input file either ipdb OR idx"
	sys.exit()
	
if args.group and args.idx:
	print "Goupes can not be stored in OpenDX file format"
	sys.exit()	
	
minArray = args.min.split()
maxArray = args.max.split()

if args.idx:
	readDx = ReadOpenDx (args.idx)
	readDx.importDx()
	dxObject = readDx.getDxObject()
if args.pdb:
	readPDB = ReadPDB (args.pdb)
	readPDB.readPDB()
	dxObject = readPDB.getDxObject()

filterThis = FilterDx (dxObject)
filterThis.deleteRectangleInside(minArray,maxArray)
dxObject = filterThis.getDxObject()


if args.group:
	groupDx=  GroupTubes (dxObject)
	groupDx.findGroups()
	groupes =  groupDx.getTubeGroup()
	voxelGroupeGrid =  groupDx.getGroups()
#	grouped = 'Yes'

if args.odx:
	saveToDx = WriteDx (dxObject)
	saveToDx.write(args.odx)
	
if args.opdb:
	saveToPDB = WritePDB (result)
	if args.group:
		if args.ipdb:
			tubeDxObject = readDx.getTubeDxObject()
			tubeDxObject.setDxObject(dxObject)
			if tubeDxObject.getFilterApplied() == 'None':
				tubeDxObject.setFilterApplied("delRectangleInside")
			else:
				tubeDxObject.setFilterApplied(tubeDxObject.getFilterApplied() + " delRectangleInside")
			tubeDxObject.setVoxelGroupGrid(voxelGroupeGrid)
			tubeDxObject.setGroupes(groupes)
			tubeDxObject.setGrouped("Yes")
			tubeDxObject.setFilename(args.ipdb)
			
		if args.idx:
			tubeDxObject = TubeDx ( dxObject, 
									filename=args.idx,
#									scanMethod = "n/a", 
#									scanned = "n/a",
#									solventThreshold = "n/a" , 
#									protThreshold = "n/a",										#better keep theire default values ... 
#									minDiameter = args.md,
#									protFile = args.protein,
#									solvFile = args.solvent,
									version = version,
									filterApplied = "delRectangleInside",
									groupes = groupes,
									VoxelGroupGrid = voxelGroupeGrid,
									grouped = 'Yes'
									)	
		
		
	else:	
		saveToPDB.write(args.opdb)


