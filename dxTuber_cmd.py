#!/usr/bin/env python
#
#	 This file is part of the dxTuber package
#    dxTuber v0.27  7. Jan 2013
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
####################################################################################
### This tool s written to detect cavities based on protein and solvent movement ###
###																				 ###
###																				 ###
### 1. flood your system with water (by using GROMACS)							 ###
###	2. Open your molecule in VMD												 ###
### 3. save 2 OpenDX (only solvent and only protein) files via VMD -> VolMap 	 ###
### 4. start this script  													     ###
###																			  	 ###
###	Contact: raunest@bit.uni-bonn.de or m.raunest@gmx.de   Martin Raunest		 ###
###																				 ###
####################################################################################
#
# v.26 
#  -bugfix / typo fixed fox z-axis scanning
#
# v.2
#  +fill after grouping implemented
#  +pdb files as input
#  +if input was not given completely or incorrect "dxtuber_cmd -h" (sys.argv[0] wuha fancy fetature ) will be printed to cmd
#  + '--mdk' (minimum distance keep ... very good english i know ... ) option to separate cavities in a "solvent network" experimental ... 
#  +overlap, switches if a ISV will be stored during scanning if a protein > protMinDens is located at the very same coordinates. 
#
# v0.1
#  -completely rewritten 
#  +dxTuber_cmd comes with full parameter support
#  +comments :]
#
#
# v0.09 
#  +wuhu dxTuber is now also on command line ... beware only standard parameters  and 2D scanning are used 
#  
#
#

import sys
import os
import re
import subprocess
from lib.readopendx import *
from lib.planesearch import *
from lib.writepdb import *
from lib.writedx import *
from lib.grouptubes import *
from lib.filterdx import *
from lib.analysetube import *
from lib.filltube import *
from lib.tubedx import *
from lib.readpdb import *

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

parser = argparse.ArgumentParser(description='Command line version of dxTuber',epilog='dxTuber v' + version)

###
# for static libs use:
# parser = ArgumentParser(description='Command line version of dxTuber',epilog='dxTuber v' + version)
###
parser.add_argument('-p','--protein',default=False, dest='protein',help='Protein dx file')
parser.add_argument('-s','--solvent',default=False, help='Solvent dx file')  
parser.add_argument('--ipdb', default=False,help='PDB inputfile (only previously via dxTuber created pdb files are supported)') 

parser.add_argument('--sm',   default='2D',  choices=('1D','2D','3D'), help='Scan method (default=2D)')
     
parser.add_argument('--sm_x',   default=False, action='store_const', const=True, help='1D scanning x (default=False)')     
parser.add_argument('--sm_y',   default=False,  action='store_const',const=True, help='1D scanning y (default=False)')     
parser.add_argument('--sm_z',   default=False, action='store_const', const=True, help='1D scanning z (default=False)')     
parser.add_argument('-g', '--group', default=False,  action='store_const', const=True, help='-g enables grouping') 
parser.add_argument('--fill',   default=False, action='store_const', const=True, help='Fill cavities after Grouping (only for 2D or 3D scanning) EXPERIMENTAL') 

parser.add_argument('--odx', default=False, help='OpenDX outfile')   
parser.add_argument('--opdb', default=False, help='PDB outfile') 
          
parser.add_argument('--smd',   default='0.00', help='Solvent minimum density (0.00 Atoms / A^3)')      
parser.add_argument('--pmd',   default='0.005', help='Protein minimum density (0.005 Atoms / A^3)') 
parser.add_argument('--md',   default='0', help='Minimum cavity diameter [A] (default=0)') 
parser.add_argument('--overlap',   default=False, action='store_const', const=True, help='Store ISV overlapping with protein voxels, FALSE per default') 


parser.add_argument('--mdk',   default=False,action='store_const',const=True, help='Minimum cavity diameter [A] (defaul=False) groups ISV > "--md [A] "and ISV < "--md [A]" separately --g MUST be set, currently only support with --sm 2D EXPERIMENTAL!') 
  
parser.add_argument('--fn', default=False,choices=range(1,27), help='Apply a neighbor filter int (1-26) (default=false)')   

args = parser.parse_args()

'''
print args.solvent #solvent dx file
print args.protein # protein dxfile
print args.pmd  # protein min density
print args.smd  #solvent min density
print args.sm  # scann method {1D 2D 3D)
print args.sm_x # enable scanning along x axis (same for y and z)
print args.group # enable grouping
print args.odx   # output dxfile
print args.opdb # output pdb file
print args.md # min diameter of the cavity
print args.fn # filter by neighbor
args.overlap # switches if ISV overlapping with protein voxels > proteinMinDens will be deleted during scanning
'''

print "dxTuber v" + version 

###
# Parameter check block :]
###



######
# checking if args.sm was given correct 
######
if not re.match('1D', args.sm):
	if (args.sm_x or args.sm_y or args.sm_x):
# running 'dxtuber_cmd -h'    : 
		sysRun = subprocess.Popen([sys.argv[0], '-h'])
		sysRun.communicate()
		print "Please use --sm  1D if --sm_x or --sm_y or sm_z are enabled"
		sys.exit()

if re.match('1D', args.sm):	
	if not (args.sm_x or args.sm_y or args.sm_z):
		sysRun = subprocess.Popen([sys.argv[0], '-h'])
		sysRun.communicate()
		print "\nChoose at least one axis for 1D scanning:\n--sm 1D --sm_x and/or --sm_y and/or --sm_z"

		sys.exit()

####
# Cheking input files ... 
####

if (args.protein or args.solvent) and args.ipdb:
	sysRun = subprocess.Popen([sys.argv[0], '-h'])
	sysRun.communicate()
	print "\n Only Protein and Solvent OpenDX files (a) or cavities as pdb file (b) are supported as input file(s)\nCombinitions of (a) and (b) are not supported"
	sys.exit()

if not ((args.protein and args.solvent)  or args.ipdb):
	sysRun = subprocess.Popen([sys.argv[0], '-h'])
	sysRun.communicate()

	print "\nInput Error:\nEither protein and solvent OpenDX files or a single pdb file are supported as input\n"

	sys.exit()
	
####
# fill + ipdb are not supported sind no solvent & protein densities are available in pdb format ... and yes they are nessacary for "fill" option
####
	
if args.ipdb and args.fill:
	sysRun = subprocess.Popen([sys.argv[0], '-h'])
	sysRun.communicate()
	
	print "\nFill option is not supported for pdb files as input\n"
	sys.exit()
		
######
# Testing if any output will be created
######

if not (args.odx) and not (args.opdb):
	sysRun = subprocess.Popen([sys.argv[0], '-h'])
	sysRun.communicate()

	print "At least one output should be generated: \n--odx OUTPUT.DX or --opdb OUTPUT.PDB"

	sys.exit()


####
# Testing args.fill
####
if args.fill and args.sm == '1D' or (args.fill and not args.group):
	sysRun = subprocess.Popen([sys.argv[0], '-h'])
	sysRun.communicate()
	print "Fill after grouping routine works only with 2D or 3D scanning, grouping is mandatory"

	sys.exit()

if args.fill and args.mdk:
	sysRun = subprocess.Popen([sys.argv[0], '-h'])
	sysRun.communicate()
	print "Fill after grouping in combinition with --mdk is not supported, ... not yet"

	sys.exit()	
##################
# Oke parameters are fine, lets start :>
##################


if args.protein and args.solvent:
	####
	#Read protein and water densities. 
	####

	readDx = ReadOpenDx (args.protein)
	readDx.importDx()
	proteinDxObject = readDx.getDxObject()
	readDx.setDxfile(args.solvent)
	readDx.importDx()
	solventDxObject = readDx.getDxObject()


	#####################
	#Scanning 
	#####################
# array of array of densities 	
	scannedArray = False  
	
	scanType = args.sm
	scanDx = PlaneSearch (dxObjectWater = solventDxObject, dxObjectProtein = proteinDxObject, minDiameter=args.md,minProteinDens =args.pmd,minSolventDens = args.smd, mdk = args.mdk, storeOverLappingISV = args.overlap) 
	
	
	if args.sm == '1D':
		scanMethod = 1
		if args.sm_x:
			scanDx.oneDimension ('x')
			scanType += " x"	
		if args.sm_y:
			scanDx.oneDimension ('y')
			scanType += " y"	
		if args.sm_z:
			scanDx.oneDimension ('z')
			scanType += " z"	
		scanned = scanDx.getDxObject()
	if args.sm == '2D':
		scanMethod = 2
		if args.mdk:
			scanDx.twoDimensionMinDiaArray()
			scannedArray = scanDx.getDxObjectArray()
#			print str(len(scannedArray))
		else:
			scanDx.twoDimension()
			
		scanned = scanDx.getDxObject()
	if args.sm == '3D':
		scanMethod = 3
		scanDx.threeDimension()
		scanned = scanDx.getDxObject()
		if args.mdk: 
			scannedArray = scanDx.getDxObjectArray()

if args.ipdb:
	readPDB = ReadPDB(args.ipdb)
	readPDB.readPDB()
	
	scanned = readPDB.getDxObject()
	scanMethod = readPDB.getTubeDxObject().getScanMethod()
	scanType = readPDB.getTubeDxObject().getScanned()
	args.pmd =readPDB.getTubeDxObject().getProtThreshold()
	args.smd =readPDB.getTubeDxObject().getSolventThreshold()
	filterName = readPDB.getTubeDxObject().getFilterApplied()
	groupes = readPDB.getTubeDxObject().getGroupes()
	grouped = readPDB.getTubeDxObject().getGrouped()
	voxelGroupGrid = readPDB.getTubeDxObject().getVoxelGroupGrid()
	args.protein = readPDB.getTubeDxObject().getProtFile()
	args.solvent = readPDB.getTubeDxObject().getSolvFile()
################
# Filter 
################
if args.protein and args.solvent:
	filterName = 'None'
	
if args.fn:
	filter = FilterDx (scanned, args.md)
	filter.filterTunnelNeighbour(neighbourMin=args.fn) 
	scanned  = filter.getDxObject()
	filterName += 'Neighbor ' + args.fn

#######
# Grouping
#######
if args.protein and args.solvent:
	grouped = 'No'
	
if args.group:
	if args.mdk:
##
# grouping isv > args.md
###
		groupes = False
		groupDx=  GroupTubes(scannedArray[0])
		groupDx.findGroups()
		groupesArray = []
		voxelGroupGridArray = []
		groupesArray.append(groupDx.getTubeGroup())    # 0
		voxelGroupGridArray.append(groupDx.getGroups()) #0     
#		voxelGroupGridArray.extend(groupDx.getGroups()) #0
		
# they only contain the filtered ISV's 
		voxelGroupGrid = groupDx.getTubeGroup()
		grouped = groupDx.getGroups()
		groupDx= ""
### 
# grouping isv < args.md
###		
		groupDx=  GroupTubes (scannedArray[1])
		groupDx.findGroups()
		groupesArray.append(groupDx.getTubeGroup())   # 1
		voxelGroupGridArray.append(groupDx.getGroups()) #1      #<<<<<----- these items should be sorted .... into one array ? [x][y][z] = density ? 
		#voxelGroupGridArray.extend(groupDx.getGroups()) #1
		grouped = 'Yes'
	else:
		groupesArray = False
		voxelGroupGridArray = False
		scannedArray = False
		groupDx=  GroupTubes (scanned)
		groupDx.findGroups()
		groupes =  groupDx.getTubeGroup()
		voxelGroupGrid =  groupDx.getGroups()
		grouped = 'Yes'
	
### +v0.12 fill after grouping	 should be testet if it works in combinition with mdk    *scared*

	if args.fill: 
		print "fill"
		fill = FillTube(dxObjectWater = solventDxObject,
				dxObjectProtein = proteinDxObject, 
				dxObjectTube = scanned, 
				scanMethod = scanMethod, 
				minProteinDensity = args.pmd,
				minSolvDensity =  args.smd,
				groups = groupes, 
				voxelGroupGrid  = voxelGroupGrid
				)
		fill.fillGroups()
		voxelGroupGrid=fill.getVoxelGroupGrid()
		groupes=fill.getGroups()
		scanned  = fill.getNewTubeObject()
### filltube needs to be rewritten really ugly code inside .... just to be sure nothing strange happens group again ...
		groupDx=  GroupTubes (scanned)
		groupDx.findGroups()
		groupes =  groupDx.getTubeGroup()
		voxelGroupGrid =  groupDx.getGroups()	
### / fill after grouping	

	result =  TubeDx ( scanned, 
			filename="None",
			scanMethod = scanMethod, 
			scanned = scanType,
			solventThreshold = args.smd , 
			protThreshold = args.pmd,
			minDiameter = args.md,
			protFile = args.protein,
			solvFile = args.solvent,
			version = version,
			filterApplied = filterName,
			groupes = groupes,
			VoxelGroupGrid = voxelGroupGrid,
			grouped = grouped,
			groupesArray = groupesArray,
			VoxelGroupGridArray = voxelGroupGridArray,
			dxObjectArray = scannedArray
			)	
		
		
			
### else ... no grouping flag ... 			
else:
	if args.protein and args.solvent:
		result =  TubeDx ( scanned, 
			filename="None",
			scanMethod = scanMethod, 
			scanned = scanType,
			solventThreshold = args.smd , 
			protThreshold = args.pmd,
			minDiameter = args.md,
			protFile = args.protein,
			solvFile = args.solvent,
			version = version,
			filterApplied = filterName,
	#		groupes = groupes,
	#		VoxelGroupGrid = voxelGroupGrid,
			grouped = grouped
			)
	if args.ipdb:
		result = readPDB.getTubeDxObject()
		
		

###########
# Output
###########


if args.odx:
	saveToDx = WriteDx (scanned)
	saveToDx.write(args.odx)

if args.opdb:
	saveToPDB = WritePDB (result)
	if args.group:
		if args.mdk:
#			print result.getGroupesArray()
			saveToPDB.writeMultiGroups(result.getGroupesArray(),args.opdb)
		else:
			saveToPDB.writeGroups(result.getGroupes(),args.opdb)
			
	else:
		saveToPDB.write(args.opdb)

'''
storePDB = WritePDB (result)
#saveToDx = WriteDx (scanned)
outfile = sys.argv[1][:-3]
outfile += ".pdb"
#outfile += "_out.dx"
storePDB.writeGroups(result.getGroupes(),outfile)
#saveToDx.write(outfile)
'''




