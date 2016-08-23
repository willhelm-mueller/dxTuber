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


from buildopendx import *
#######
# This class fills cavities along principle axis after grouping
#
# v0.12 
# +int(scanMethod)
########
class FillTube():
	__dxObjectTube =()
	__dxObjectProtein =()
	__scanMethod =()
	__minProteinDensity =()
	__newTubeDensity = []
#voxelGroupGrid
#[x][y][z] = group	
	__voxelGroupGrid =()
#groups
#[[x][y][z][x][y][z]]
	__groups =()
	def __init__(self,dxObjectWater,dxObjectProtein, dxObjectTube, scanMethod, minProteinDensity, minSolvDensity, groups = None, voxelGroupGrid  = None):
		self.__dxObjectTube = dxObjectTube
		self.__dxObjectWater = dxObjectWater
		self.__dxObjectProtein = dxObjectProtein
		self.__scanMethod = int (scanMethod)
		self.__minProteinDensity = float(minProteinDensity)
		self.__groups = groups
		self.__voxelGroupGrid = voxelGroupGrid
		self.__minSolvDensity = float(minSolvDensity)
	def getNewTubeObject(self):
		object = BuildOpenDx (self.__newTubeDensity, self.__dxObjectTube.getStepsize(), self.__dxObjectTube.getOrigin(), self.__dxObjectTube.getDimention())
		return object
	def getVoxelGroupGrid(self):
		return self.__voxelGroupGrid
	def getGroups(self):
		return self.__groups

		
	def fillGroups(self):
		if self.__scanMethod == 2:
			self.__fill2d()
		if self.__scanMethod == 3:
			self.__fill3d()
	def __fill2d(self):
		print "Filling cavities after 2D scanning"
		oldTube = self.__dxObjectTube.getDensity()
		newTube  = [[[-1 for zR in range(len(oldTube[0][0]))] for yR in range(len(oldTube[0]))] for xR in range(len(oldTube))]
		newVoxelGroupGrid = [[[-1 for zR in range(len(oldTube[0][0]))] for yR in range(len(oldTube[0]))] for xR in range(len(oldTube))]
		densityProtein = self.__dxObjectProtein.getDensity()
		densityWater = self.__dxObjectWater.getDensity()
############ X ###############
		print "X"
		for  yCount in range (len (densityProtein[0])):
			for zCount in range (len (densityProtein[0][0])):
				for  xCount in range (len (densityProtein)):
#### filling X+	
#### xPlus xMinus indicates if a cavity will be filled in plus or minus direction 

					xPlus = 1
					xMinus = 1 
					if xCount == (len  (densityProtein)-1):
						xPlus = 0
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity) or
						densityProtein[xCount+1][yCount][zCount] > float(self.__minProteinDensity) ):
						xPlus = 0	
					
####### this block is taken from planesearch to indicate towards which principle directions cavities can be filled 
					xProteinLeft = 0 #x-
					xProteinRight = 0	#x+				
					j = xCount	
					while (j > 0):
						j -=1
						if (densityProtein[j][yCount][zCount] >=  float(self.__minProteinDensity)):
							xProteinLeft = xCount - j						
							break
							
					for k in range (xCount,len(densityProtein)):
						 if (densityProtein[k][yCount][zCount] >=  float(self.__minProteinDensity)  ):
							xProteinRight = k- xCount
							break 					
					if xProteinLeft < 1:
						xMinus = 0
					if xProteinRight <1:
						xPlus = 0
#### end of planesearch block####
		

						
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]+1][convertPosition[1]][convertPosition[2]] > 0):
						xPlus = 0
					if (densityWater[convertPosition[0]+1][convertPosition[1]][convertPosition[2]] < self.__minSolvDensity):
						xPlus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and xPlus == 1):
						i = 1
						oldGroup =  self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						while ( i > -1):
							if (densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] > self.__minSolvDensity):
								newTube[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]]
#adding new voxel to existing group definitions
								if self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] < 0 or self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
## adding voxel to groups 
#[[x][y][z][x][y][z]]
								x = convertPosition[0]+i
								y = convertPosition[1]
								z = convertPosition[2]
								self.__groups[oldGroup].append([x,y,z])	
							i +=1
							if (oldTube[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] > 0):
								i = -1 	
							if (densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] < self.__minSolvDensity):
								i = -1
							if (densityProtein[xCount+i][yCount][zCount] > float(self.__minProteinDensity)):
								i = -1

#### filling X-
					
					if xCount == 0:
						xMinus = 0
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity) or
					#if (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity) or
						densityProtein[xCount-1][yCount][zCount] > float(self.__minProteinDensity) ):
						xMinus = 0
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]-1][convertPosition[1]][convertPosition[2]] > 0):
						xMinus = 0
					if (densityWater[convertPosition[0]-1][convertPosition[1]][convertPosition[2]] < self.__minSolvDensity):
						xMinus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and xMinus == 1):
						i = -1
						oldGroup =  self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						while ( i < 1):
							if (densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] > self.__minSolvDensity):
								newTube[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]]
#adding new voxel to existing group definitions
								if self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] < 0 or self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
## adding voxel to groups 
#[[x][y][z][x][y][z]]
								x = convertPosition[0]+i
								y = convertPosition[1]
								z = convertPosition[2]
								self.__groups[oldGroup].append([x,y,z])	
							i -=1
							if (oldTube[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] > 0):
								i = 1 	
							if (densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] < self.__minSolvDensity):
								i = 1
							if (densityProtein[xCount+i][yCount][zCount] > float(self.__minProteinDensity)):
								i = 1





############ Y ###############
		print "Y"
		for  xCount in range (len (densityProtein)):
			for zCount in range (len (densityProtein[0][0])):
				for  yCount in range (len (densityProtein[0])):

##### filling Y+
					yPlus = 1 
					yMinus = 1
					
					yProteinLeft = 0 #y-
					yProteinRight = 0	#y+	
					j = yCount
					while (j > 0):
						j -=1
						if (densityProtein[xCount][j][zCount] >=  float(self.__minProteinDensity)  ):
							yProteinLeft = yCount - j	
							break
							
					for k in range (yCount,len(densityProtein[0])):
						 if (densityProtein[xCount][k][zCount] >=  float(self.__minProteinDensity)  ):
							yProteinRight = k - yCount
							break 					
					if yProteinLeft < 1:
						yMinus = 0
					if xProteinRight <1:
						yPlus = 0
					
					
					
					if yCount == (len  (densityProtein[0])-1):
						yPlus = 0
#					if (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity)or
#						densityProtein[xCount][yCount+1][zCount] > float(self.__minProteinDensity) ):
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity)or
						densityProtein[xCount][yCount+1][zCount] > float(self.__minProteinDensity) ):
						yPlus = 0
						
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]][convertPosition[1]+1][convertPosition[2]] > 0):
						yPlus = 0
					if (densityWater[convertPosition[0]][convertPosition[1]+1][convertPosition[2]] < self.__minSolvDensity):
						yPlus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and yPlus ==1):
						i = 1
						oldGroup = self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						while ( i > -1):
							if (densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] > self.__minSolvDensity):
								newTube[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] = densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]]
#adding new voxel to existing group definitions
								if self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] < 0 or self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
## adding voxel to groups 
#[[x][y][z][x][y][z]]
								x = convertPosition[0]
								y = convertPosition[1]+i
								z = convertPosition[2]
								self.__groups[oldGroup].append([x,y,z])	
							i +=1
							if (densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] < self.__minSolvDensity):
								i = -1								
							if (oldTube[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] > 0):
								i = -1 	
							if (densityProtein[xCount][yCount+i][zCount] > float(self.__minProteinDensity)):
								i = -1


###### filling Y- 
					 
					if yCount == 0:
						yMinus = 0
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity)or
						densityProtein[xCount][yCount-1][zCount] > float(self.__minProteinDensity) ):
						yMinus = 0
						
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]][convertPosition[1]-1][convertPosition[2]] > 0):
						yMinus = 0
					if (densityWater[convertPosition[0]][convertPosition[1]-1][convertPosition[2]] < self.__minSolvDensity):
						yMinus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and yMinus == 1):
						i = -1
						oldGroup = self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						while ( i < 1):
							if (densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] > self.__minSolvDensity):
								newTube[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] = densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]]
#adding new voxel to existing group definitions
								if self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] < 0 or self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
## adding voxel to groups 
#[[x][y][z][x][y][z]]
								x = convertPosition[0]
								y = convertPosition[1]+i
								z = convertPosition[2]
								self.__groups[oldGroup].append([x,y,z])	
							i -=1
							if (densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] < self.__minSolvDensity):
								i = 1								
							if (oldTube[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] > 0):
								i = 1 	
							if (densityProtein[xCount][yCount+i][zCount] > float(self.__minProteinDensity)):
								i = 1


####### Z ########
		print "Z"
		for  xCount in range (len (densityProtein)):
			for  yCount in range (len (densityProtein[0])):
				for zCount in range (len (densityProtein[0][0])):
					
########## filling Z+
					zPlus = 1 
					zMinus = 1
					
					zProteinLeft = 0#z-
					zProteinRight = 0#z+				
					j = zCount
					while (j > 0):
						j -=1
						if (densityProtein[xCount][yCount][j] >=  float(self.__minProteinDensity)  ):
							zProteinLeft = zCount - j	
							break

					for k in range (zCount,len(densityProtein[0][0])):
						 if (densityProtein[xCount][yCount][k] >= float(self.__minProteinDensity)  ):
							zProteinRight =k- zCount
							break 					
					
					if zProteinLeft < 1:
						zMinus = 0
					if zProteinRight <1:
						zPlus = 0
					
					if zCount == (len  (densityProtein[0][0])-1):
						zPlus = 0
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity) or
						densityProtein[xCount][yCount][zCount+1] > float(self.__minProteinDensity) ):
						zPlus = 0
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]+1] > 0):
						zPlus = 0
					if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+1] < self.__minSolvDensity):
						zPlus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and zPlus == 1):
						i = 1
						oldGroup =  self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						while ( i > -1):
							if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] > self.__minSolvDensity):
								newTube[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] = densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i]
#adding new voxel to existing group definitions
								if self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] < 0 or self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
## adding voxel to groups 
#[[x][y][z][x][y][z]]
								x = convertPosition[0]
								y = convertPosition[1]
								z = convertPosition[2]+i
								self.__groups[oldGroup].append([x,y,z])	
							i +=1
							if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] < self.__minSolvDensity):
								i = -1
							if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] > 0):
								i = -1 			 
							if (densityProtein[xCount][yCount][zCount+i] > float(self.__minProteinDensity)):
								i = -1
########### filliung Z-
					
					if zCount == 0:
						zMinus = 0
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity) or
						densityProtein[xCount][yCount][zCount-1] > float(self.__minProteinDensity) ):
						zMinus = 0
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]-1] > 0):
						zMinus = 0
					if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]-1] < self.__minSolvDensity):
						zMinus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and zMinus == 1):
						i = -1 
						while ( i < 0):
							if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] > self.__minSolvDensity):
								newTube[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] = densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i]
								if self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] < 0 or self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
								## adding voxel to groups 
								#[[x][y][z][x][y][z]]
								x = convertPosition[0]
								y = convertPosition[1]
								z = convertPosition[2]+i
								self.__groups[oldGroup].append([x,y,z])	
							i -=1
							if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] < self.__minSolvDensity):
								i = 1	
							if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] > 0):
								i = 1 			 
							if (densityProtein[xCount][yCount][zCount+i] > float(self.__minProteinDensity)):
								i = 1


		for  xCount in range (len (newTube)):
			for  yCount in range (len (newTube[0])):
				for zCount in range (len (newTube[0][0])):
					if newTube[xCount][yCount][zCount] > 0:
						oldTube[xCount][yCount][zCount] = newTube[xCount][yCount][zCount]
						self.__voxelGroupGrid[xCount][yCount][zCount] = newVoxelGroupGrid[xCount][yCount][zCount]
		self.__newTubeDensity = oldTube	
		
			
	def __fill3d(self):
		print "Filling cavities after 3D scanning"
		oldTube = self.__dxObjectTube.getDensity()
		newTube  = [[[-1 for zR in range(len(oldTube[0][0]))] for yR in range(len(oldTube[0]))] for xR in range(len(oldTube))]
		newVoxelGroupGrid = [[[-1 for zR in range(len(oldTube[0][0]))] for yR in range(len(oldTube[0]))] for xR in range(len(oldTube))]
		densityProtein = self.__dxObjectProtein.getDensity()
		densityWater = self.__dxObjectWater.getDensity()
############ X ###############
		print "X"
		for  yCount in range (len (densityProtein[0])):
			for zCount in range (len (densityProtein[0][0])):
				for  xCount in range (len (densityProtein)):
#### filling X+	
#### xPlus xMinus indicates if a cavity will be filled in plus or minus direction 

					xPlus = 1
					if xCount == (len  (densityProtein)-1):
						xPlus = 0
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity) or
						densityProtein[xCount+1][yCount][zCount] > float(self.__minProteinDensity) ):
						xPlus = 0
						
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]+1][convertPosition[1]][convertPosition[2]] > 0):
						xPlus = 0
					if (densityWater[convertPosition[0]+1][convertPosition[1]][convertPosition[2]] < self.__minSolvDensity):
						xPlus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and xPlus == 1):
						i = 1
						oldGroup =  self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						while ( i > -1):
							if (densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] > self.__minSolvDensity):
								newTube[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]]
#adding new voxel to existing group definitions
								if self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] < 0 or self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
## adding voxel to groups 
#[[x][y][z][x][y][z]]
								x = convertPosition[0]+i
								y = convertPosition[1]
								z = convertPosition[2]
								self.__groups[oldGroup].append([x,y,z])	
							i +=1
							if (oldTube[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] > 0):
								i = -1 	
							if (densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] < self.__minSolvDensity):
								i = -1
							if (densityProtein[xCount+i][yCount][zCount] > float(self.__minProteinDensity)):
								i = -1

#### filling X-
					xMinus = 1 
					if xCount == 0:
						xMinus = 0
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity) or
					#if (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity) or
						densityProtein[xCount-1][yCount][zCount] > float(self.__minProteinDensity) ):
						xMinus = 0
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]-1][convertPosition[1]][convertPosition[2]] > 0):
						xMinus = 0
					if (densityWater[convertPosition[0]-1][convertPosition[1]][convertPosition[2]] < self.__minSolvDensity):
						xMinus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and xMinus == 1):
						i = -1
						oldGroup =  self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						while ( i < 1):
							if (densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] > self.__minSolvDensity):
								newTube[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]]
#adding new voxel to existing group definitions
								if self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] < 0 or self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
## adding voxel to groups 
#[[x][y][z][x][y][z]]
								x = convertPosition[0]+i
								y = convertPosition[1]
								z = convertPosition[2]
								self.__groups[oldGroup].append([x,y,z])	
							i -=1
							if (oldTube[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] > 0):
								i = 1 	
							if (densityWater[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] < self.__minSolvDensity):
								i = 1
							if (densityProtein[xCount+i][yCount][zCount] > float(self.__minProteinDensity)):
								i = 1


############ Y ###############
		print "Y"
		for  xCount in range (len (densityProtein)):
			for zCount in range (len (densityProtein[0][0])):
				for  yCount in range (len (densityProtein[0])):

##### filling Y+
					yPlus = 1 
					if yCount == (len  (densityProtein[0])-1):
						yPlus = 0
#					if (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity)or
#						densityProtein[xCount][yCount+1][zCount] > float(self.__minProteinDensity) ):
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity)or
						densityProtein[xCount][yCount+1][zCount] > float(self.__minProteinDensity) ):
						yPlus = 0
						
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]][convertPosition[1]+1][convertPosition[2]] > 0):
						yPlus = 0
					if (densityWater[convertPosition[0]][convertPosition[1]+1][convertPosition[2]] < self.__minSolvDensity):
						yPlus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and yPlus ==1):
						i = 1
						oldGroup = self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						while ( i > -1):
							if (densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] > self.__minSolvDensity):
								newTube[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] = densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]]
#adding new voxel to existing group definitions
								if self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] < 0 or self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
## adding voxel to groups 
#[[x][y][z][x][y][z]]
								x = convertPosition[0]
								y = convertPosition[1]+i
								z = convertPosition[2]
								self.__groups[oldGroup].append([x,y,z])	
							i +=1
							if (densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] < self.__minSolvDensity):
								i = -1								
							if (oldTube[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] > 0):
								i = -1 	
							if (densityProtein[xCount][yCount+i][zCount] > float(self.__minProteinDensity)):
								i = -1

###### filling Y- 
					yMinus = 1 
					if yCount == 0:
						yMinus = 0
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity)or
						densityProtein[xCount][yCount-1][zCount] > float(self.__minProteinDensity) ):
						yMinus = 0
						
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]][convertPosition[1]-1][convertPosition[2]] > 0):
						yMinus = 0
					if (densityWater[convertPosition[0]][convertPosition[1]-1][convertPosition[2]] < self.__minSolvDensity):
						yMinus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and yMinus == 1):
						i = -1
						oldGroup = self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						while ( i < 1):
							if (densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] > self.__minSolvDensity):
								newTube[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] = densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]]
#adding new voxel to existing group definitions
								if self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] < 0 or self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
## adding voxel to groups 
#[[x][y][z][x][y][z]]
								x = convertPosition[0]
								y = convertPosition[1]+i
								z = convertPosition[2]
								self.__groups[oldGroup].append([x,y,z])	
							i -=1
							if (densityWater[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] < self.__minSolvDensity):
								i = 1								
							if (oldTube[convertPosition[0]][convertPosition[1]+i][convertPosition[2]] > 0):
								i = 1 	
							if (densityProtein[xCount][yCount+i][zCount] > float(self.__minProteinDensity)):
								i = 1


####### Z ########
		print "Z"
		for  xCount in range (len (densityProtein)):
			for  yCount in range (len (densityProtein[0])):
				for zCount in range (len (densityProtein[0][0])):
					
########## filling Z+
					zPlus = 1 
					if zCount == (len  (densityProtein[0][0])-1):
						zPlus = 0
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity) or
						densityProtein[xCount][yCount][zCount+1] > float(self.__minProteinDensity) ):
						zPlus = 0
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]+1] > 0):
						zPlus = 0
					if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+1] < self.__minSolvDensity):
						zPlus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and zPlus == 1):
						i = 1
						oldGroup =  self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						while ( i > -1):
							if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] > self.__minSolvDensity):
								newTube[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] = densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i]
#adding new voxel to existing group definitions
								if self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] < 0 or self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
## adding voxel to groups 
#[[x][y][z][x][y][z]]
								x = convertPosition[0]
								y = convertPosition[1]
								z = convertPosition[2]+i
								self.__groups[oldGroup].append([x,y,z])	
							i +=1
							if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] < self.__minSolvDensity):
								i = -1
							if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] > 0):
								i = -1 			 
							if (densityProtein[xCount][yCount][zCount+i] > float(self.__minProteinDensity)):
								i = -1
########### filliung Z-
					zMinus = 1
					if zCount == 0:
						zMinus = 0
					elif (densityProtein[xCount][yCount][zCount] > float(self.__minProteinDensity) or
						densityProtein[xCount][yCount][zCount-1] > float(self.__minProteinDensity) ):
						zMinus = 0
#calculating shift between water & tube coordienates towards protein coordinates
					proteinOrigin = self.__dxObjectProtein.getOrigin()
					tubeOrigin = self.__dxObjectTube.getOrigin()
					tubeToProteinOrigin = (int (proteinOrigin[0] - tubeOrigin[0]),int (proteinOrigin[1] - tubeOrigin[1]),int (proteinOrigin[2] - tubeOrigin[2]))						
					convertPosition = (xCount+tubeToProteinOrigin[0], yCount+tubeToProteinOrigin[1],zCount+tubeToProteinOrigin[2])
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]-1] > 0):
						zMinus = 0
					if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]-1] < self.__minSolvDensity):
						zMinus = 0
					if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]] > 0 and zMinus == 1):
						i = -1 
						while ( i < 0):
							if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] > self.__minSolvDensity):
								newTube[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] = densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i]
								if self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] < 0 or self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] == oldGroup:
									newVoxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] = oldGroup
								else:
									tmp = str(self.__voxelGroupGrid[convertPosition[0]][convertPosition[1]][convertPosition[2]+i])
									tmp += " "+str(oldGroup)
									newVoxelGroupGrid[convertPosition[0]+i][convertPosition[1]][convertPosition[2]] = tmp
								## adding voxel to groups 
								#[[x][y][z][x][y][z]]
								x = convertPosition[0]
								y = convertPosition[1]
								z = convertPosition[2]+i
								self.__groups[oldGroup].append([x,y,z])	
							i -=1
							if (densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] < self.__minSolvDensity):
								i = 1	
							if (oldTube[convertPosition[0]][convertPosition[1]][convertPosition[2]+i] > 0):
								i = 1 			 
							if (densityProtein[xCount][yCount][zCount+i] > float(self.__minProteinDensity)):
								i = 1
		for  xCount in range (len (newTube)):
			for  yCount in range (len (newTube[0])):
				for zCount in range (len (newTube[0][0])):
					if newTube[xCount][yCount][zCount] > 0:
						oldTube[xCount][yCount][zCount] = newTube[xCount][yCount][zCount]
						self.__voxelGroupGrid[xCount][yCount][zCount] = newVoxelGroupGrid[xCount][yCount][zCount]
		self.__newTubeDensity = oldTube
