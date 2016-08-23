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
# v0.15 
# +supporting
#	 +dxObjectArray
#	 +groupesArray
#	 +VoxelGroupGridArray 


class TubeDx():
	def __init__(self, 
				openDxObject, 
				filename = 'None', 
				proteinObject=0, 
				waterObject=0, 
				scanMethod = '-1', 
				scanned='No',
				grouped='No',
				groupes=None, 
				VoxelGroupGrid = None, 
				minDiameter = '0' ,
				protThreshold = '0', 
				solventThreshold ='0', 
				version = 'unknown',
				protFile = 'None',
				solvFile = 'None', 
				filterApplied = 'None',

# following arrays could be used for filtering:
#
# position 0 contain the Voxels fullfilling the filter criterion openDxObjects / groupes / voxelgroupgrids 
# position 1 contain the Voxels not fullfilling the filter criterion openDxObjects / groupes / voxelgroupgrids 
#
# both posiotions will be grouped separately and written into PDB file 
#

				
#since v0.15 containing multiple dxObjects 
#
# minimum diameter scanning 
# dxObjectArray[0] densities bigger than minDiameter threshold
# dxObjectArray[1] densities smaler than minDiameter threshold
#		
				dxObjectArray = None,
				groupesArray = None,
				VoxelGroupGridArray = None 
				):
					
		self.__openDxObject = openDxObject
		self.__filename = filename
		self.__proteinObject = proteinObject
		self.__waterObject = waterObject
		self.__scanned = scanned   # if the cavity is scanned types are '1D[xyz] , 2D , 3D ....
		self.__grouped = grouped
		self.__version = version
		self.__scanMethod = str(scanMethod)
		self.__protThreshold = float(protThreshold)
		self.__solventThreshold = float(solventThreshold)
		self.__minDiameter = minDiameter
		self.__protFile = protFile
		self.__solvFile = solvFile
		self.__filterApplied = filterApplied
# Be aware of these different arrays ... 
#groupes
#[[x][y][z][x][y][z]]
		self.__groupes = groupes
#voxelGroupGrid
#[x][y][z] = group
		self.__VoxelGroupGrid = VoxelGroupGrid

# since v0.15: 
#
# [0] Voxels fullfilling the filter criterion
# [1] Voxels not fullfilling the filter criterion
		self.__dxObjectArray = dxObjectArray
		self.__groupesArray = groupesArray
		self.__VoxelGroupGridArray = VoxelGroupGridArray
		
		
	
	def getFilename(self):
		return self.__filename
	def getProtFile(self):
		return self.__protFile
	def getSolvFile(self):
		return self.__solvFile
	def setFilterApplied(self,filter):
		if (self.__filterApplied == 'None'):
			self.__filterApplied = filter
		else: self.__filterApplied += ', '+ filter
	def getFilterApplied(self):
		return 	self.__filterApplied
		
	def setFilename(self,filename):
		self.__filename = filename
	def setWater (self,condition = 0):
		self.__waterObject = condition
	def getWater (self):
		return self.__waterObject
	def getVersion(self):
		return self.__version
	def getProtThreshold(self):
		return self.__protThreshold
	def getSolventThreshold(self):
		return self.__solventThreshold
	def getMinDiameter(self):
		return self.__minDiameter	
	def setProtein (self,condition = 0):
		self.__proteinObject = condition
	def getProtein (self):
		return self.__proteinObject	
				
	def setScanned (self,condition = 0):
		self.__scanned = condition
	def setGrouped (self,condition = 0):
		self.__grouped = condition	
	def setScanMethod (self,condition = 0):
		self.__scanMethod = condition
	def getScanMethod (self):
		return self.__scanMethod
#groupes
#[[x][y][z][x][y][z]]	
	def setGroupes (self,condition = None):
		self.__groupes = condition		
	def getGroupes (self):
		return self.__groupes
#voxelGroupGrid
#[x][y][z] = group
	def setVoxelGroupGrid (self,condition = None):
		self.__VoxelGroupGrid = condition		
	def getVoxelGroupGrid (self):
		return self.__VoxelGroupGrid

		
	def getScanned (self):
		return self.__scanned 
	def getGrouped (self):
		return self.__grouped 	
			
	def getDxObject(self):
		return self.__openDxObject
	def setDxObject(self,dxObject):
		self.__openDxObject = dxObject
	
	def setProteinObject(self,openDxObject):
		self.__proteinObject = openDxObject
	def getProteinObject(self):
		return self.__proteinObject
	def setWaterObject(self,openDxObject):
		self.__waterObject = openDxObject
	def getWaterObject(self):
		return self.__waterObject
		
##### new in v0.15
#
#

	def getDxObjectArray(self):
		return self.__dxObjectArray 
		
#array of  array of groupes
#[ [[x][y][z][x][y][z]]	]   <--- 0   and more like them   1 ---->   [  [[x][y][z][x][y][z]] ]
	def getGroupesArray(self):			
		return self.__groupesArray
	def getVoxelGroupGridArray(self):
		return self.__VoxelGroupGridArray 
		
	def setDxObjectArray(self, condition):
		self.__dxObjectArray = condition
	def setGroupesArray(self,condition):			
		self.__groupesArray = condition
	def setVoxelGroupGridArray(self,condition):
		self.__VoxelGroupGridArray = condition
		
		
