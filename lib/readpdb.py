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
#v0.27
#+Added error message for unsupported pdb files. Example header is now printed to cli
#
#v0.12
# -coordinates are extrated now absolute postions
#



import re
import sys
from tubedx import *
from buildopendx import *

class ReadPDB ():
	__scanned = 'No'
	__filename="None"
	__scanType = 'None'
	__minSolvDens =''
	__minProtDens =''
	__minDiameter = ''
	__protFile = ''
	__solvFile = ''
	__version = 0
	__filter = ''
	__grouped = 'No'
	def __init__ (self, pdbFile):
		self.__pdbFile = pdbFile
	def readPDB (self):
		pdbFH = open(self.__pdbFile,"r")
		origin = ['x','y','z']
		maxCoord = ['x','y','z']
		dimention = [0,0,0]
		groupArray = []
		lastGroup = 0  
		for line in  pdbFH.readlines():
#getting dxTuber settings 			
			if (re.match('^dxTuber\s+Version',line)):
				self.__version = line.rsplit()[2]
				print 'Created with Version ' + self.__version			
			if (re.match('^dxTuber\s+OpenDXFile',line)):
				self.__dxFile = line.rsplit()[2]
#				print line.rsplit()[2]
				
			if (re.match('^dxTuber\s+ProteinFile',line)):
				self.__protFile = line.rsplit()[2]
				print 'Protein file ' + self.__protFile
			if (re.match('^dxTuber\s+SolventFile',line)):
				self.__solvFile = line.rsplit()[2]
				print 'Solvent file ' + self.__solvFile
			if (re.match('^dxTuber\s+StepSize',line)):
				self.__stepSize = line.rsplit()[2]
				print 'Stepsize ' + self.__stepSize
			if (re.match('^dxTuber\s+ScanType',line)):
				self.__scanType = line.rsplit()[2]
				print 'Scan type ' + self.__scanType
			if (re.match('^dxTuber\s+MinDiameter',line)):
				self.__minDiameter = line.rsplit()[2]
				print 'Min diameter ' + self.__minDiameter
			if (re.match('^dxTuber\s+MinProtDens',line)):
				self.__minProtDens = line.rsplit()[2]
				print 'Min protein density ' +self.__minProtDens
			if (re.match('^dxTuber\s+MinSolvDens',line)):
				self.__minSolvDens= line.rsplit()[2]
				print 'Min solvent density ' + self.__minSolvDens
			if (re.match('^dxTuber\s+Filter',line)):
#filters are seperated by ', ' 
				tempLine = line.rstrip('\n')
				self.__filter= tempLine.split(None,2)[2]
				print 'Filter applied ' + self.__filter
#getting the origin 	
#					x_coord = line[31:38]
#					y_coord= line[39:46]				
#					z_coord= line[47:54]

		
			if (re.match('^ATOM',line)):
#				print 'x: ' + line[31:38]
#				print 'y: ' + line[39:46]
#				print 'z: ' + line[47:54]
				if origin[0] == 'x':
					origin[0] = float (line[31:38]) 
					origin[1] = float (line[39:46]) 
					origin[2] = float (line[47:54]) 
					
				if (origin[1] > float (line[39:46])):
					origin[1] = float (line[39:46]) 
				if (origin[2] > float (line[47:54])):
					origin[2] = float (line[47:54]) 
#getting size of the grid
				if (maxCoord[0] == 'x'):
					maxCoord[0] = float (line[31:38]) 
					maxCoord[1] = float (line[39:46]) 
					maxCoord[2] = float (line[47:54]) 
					
				if (maxCoord[0] < float (line[31:38])):
					maxCoord[0] = float (line[31:38]) 					
				if (maxCoord[1] < float (line[39:46])):
					maxCoord[1] = float (line[39:46]) 
				if (maxCoord[2] < float (line[47:54])):
					maxCoord[2] = float (line[47:54]) 						
		pdbFH.close()			
		if self.__version == 0:
			print 'PDB file not supported \nOnly previously processed files can be read.'
#			print 'Please add an "dxTuber" header to your file (e.g.): \ndxTuber	Version		0.25\ndxTuber	OpenDXFile	None\ndxTuber	ProteinFile	110_protein.dx\ndxTuber	SolventFile	110_water.dx\ndxTuber	StepSize	1.0\ndxTuber	ScanType	2D\ndxTuber	MinDiameter	0\ndxTuber	MinProtDens	0.005\ndxTuber	MinSolvDens	0.0\ndxTuber	Filter		None\ndxTuber	Grouped		No\n'
			print """
Please add an "dxTuber" header to your file (e.g.): 
dxTuber	Version		0.25
dxTuber	OpenDXFile	None
dxTuber	ProteinFile	110_protein.dx
dxTuber	SolventFile	110_water.dx
dxTuber	StepSize	1.0
dxTuber	ScanType	2D
dxTuber	MinDiameter	0
dxTuber	MinProtDens	0.005
dxTuber	MinSolvDens	0.0
dxTuber	Filter		None
dxTuber	Grouped		No"""
#			
			sys.exit()
#			return (1)
			
# grid should not end directly after a cavity to make grouping possible 			
		maxCoord[0] = maxCoord[0] +2
		maxCoord[1] = maxCoord[1] +2
		maxCoord[2] = maxCoord[2] +2
			
		origin[0] = origin[0] -1
		origin[1] = origin[1] -1
		origin[2] = origin[2] -1
		
		dimention[0] = int(maxCoord[0] - origin[0])
		dimention[1] = int(maxCoord[1] - origin[1])
		dimention[2] = int(maxCoord[2] - origin[2])
		print 'Origin:'
		print origin 
		print 'Dimension:'
		print dimention
		density = [[[0 for zR in range(dimention[2])] for yR in range(dimention[1])] for xR in range(dimention[0])]
#groupGrid[x][y][z] = group array		
		groupGrid = [[[-1 for zR in range(dimention[2])] for yR in range(dimention[1])] for xR in range(dimention[0])]
#		fetching densities
		pdbFH = open(self.__pdbFile,"r")
		
		for line in  pdbFH.readlines():
			if (re.match('^ATOM',line)):
				x = int(float(line[31:38]) - origin[0])
				y = int(float(line[39:46]) - origin[1])
				z = int(float(line[47:54]) - origin[2])
				density[x][y][z] = float (line[61:66])
				if re.search('[0-9]+', line[13:16]):
					self.__grouped = 'Yes'
					if groupArray == []:
						tmp =[x,y,z] 
						groupArray.append([tmp]) 
					elif int(line[13:16]) == lastGroup:
						groupArray[lastGroup].append ([x,y,z])
					self.__grouped = 'Yes'
					if int(line[13:16]) != lastGroup: 
						tmp = [([x,y,z])]
						groupArray.append (tmp)
						lastGroup += 1
#groupGrid[x][y][z] = group array
					if groupGrid[x][y][z] != -1:
						groupGrid[x][y][z] +=' '+ str(int(line[13:16]))
					else:
						groupGrid[x][y][z] = str(int(line[13:16]))
		pdbFH.close()
		self.__density = density
		self.__origin = origin 
		self.__size = dimention
		if self.__scanType != 'None':
			self.scanned = 'Yes'
		try: 
			self.__dxFile
		except:
			self.__dxFile = 'None'
		if self.__grouped == 'Yes':
			self.__tubeDxObject = 	TubeDx ( self.getDxObject(), 
									filename=self.__dxFile,
									scanMethod = self.__scanType, 
									scanned = self.__scanType,
									solventThreshold = self.__minSolvDens , 
									protThreshold = self.__minProtDens,
									minDiameter = self.__minDiameter,
									protFile = self.__protFile,
									solvFile = self.__solvFile,
									version = self.__version,
									filterApplied = self.__filter,
									groupes = groupArray,
									VoxelGroupGrid = groupGrid,
									grouped = 'Yes'
									)		
		else:
			self.__tubeDxObject = 	TubeDx ( self.getDxObject(), 
									filename= self.__dxFile,
									scanMethod = self.__scanType, 
									scanned = self.__scanType,
									solventThreshold = self.__minSolvDens , 
									protThreshold = self.__minProtDens,
									minDiameter = self.__minDiameter,
									protFile = self.__protFile,
									solvFile = self.__solvFile,
									version = self.__version,
									filterApplied = self.__filter
						)		
		print "Finished importing: "+ self.__pdbFile
		return (0)
	def getDxObject(self=None):
		object = BuildOpenDx (self.__density, self.__stepSize, self.__origin,self.__size)
		return object
	def getTubeDxObject (self):
		return 	self.__tubeDxObject		
		
