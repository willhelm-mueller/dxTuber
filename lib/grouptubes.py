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
#####
# v0.15
# -excluded diagonals from grouping 
#


import sys
class GroupTubes():
	
	__tubeDensity = []
	__tubeGroup =[]
#	tubeVoxelGrouped =[]
	__groupCount = 0
	__groupVoxel= []
	def __init__(self, dxObjectTube):
		self.__tubeDensity = dxObjectTube.getDensity()

	def testIndex(self, string, array):
		try:
			i = array.index(string)
		except ValueError:
			i = -1 # string not found
		return i	
		
	def findGroups(self):
		print "Start grouping cavities"
#in tubeVoxelGrouped is [x][y][z] = group
		tubeVoxelGrouped =[[[-1 for zR in range(len (self.__tubeDensity[0][0]))] for yR in range(len (self.__tubeDensity[0]))] for xR in range(len (self.__tubeDensity))]
#self.__tubeGroup :
#[[x][y][z][x][y][z]]		
		self.__tubeGroup  = []
		for  xCount in range (len (self.__tubeDensity)):
			for  yCount in range (len (self.__tubeDensity[0])):
				for zCount in range (len (self.__tubeDensity[0][0])):
#analysing neighbourhood if there is allready a cluster:
					if (self.__tubeDensity[xCount][yCount][zCount]):
						list = [-1,0]
						zlist = [-1,0,1]
						foundGroup = -1
						for xPos in  list:
							for yPos in  list:
								for zPos in zlist:
									if (zPos == 0 and xPos == 0 and yPos == 0):
										continue
#not visited yet 										
									if (xPos == 0 and yPos == 0 and zPos == 1):
										continue

### excluding diagonals EXPERIMENTAL ##############
#									if (xPos == -1 and yPos == -1 and zPos == -1):
#										continue
#									if (xPos == 0 and yPos == -1 and zPos == -1):
#										continue
#									if (xPos == -1 and yPos == -1 and zPos == 0 ):
#										continue
#									if (xPos == -1 and yPos == -1 and zPos == +1  ):
#										continue
#									if (xPos == -1 and yPos == 0 and zPos == +1):
#										continue
#									if (xPos == -1 and yPos == 0 and zPos == -1 ):
#										continue
#########################################
	
										
#test if another group is defined in neighbourhood:		
									if (self.__tubeDensity[xCount+xPos][yCount+yPos][zCount+zPos] ):
										coordinate = (xCount+xPos,yCount+yPos,zCount+zPos)
										neighbourGrp =  tubeVoxelGrouped [coordinate[0]][coordinate[1]][coordinate[2]]
										
										if (foundGroup >= 0):
#											neighbourGrp =  tubeVoxelGrouped [coordinate[0]][coordinate[1]][coordinate[2]]
											if (neighbourGrp == foundGroup):									
												continue
# if another group is found, members will be copied from later found cluster to earlier found cluster
#											print "merging two groups: "+ str(neighbourGrp) + " " + str(foundGroup)
											if (neighbourGrp > foundGroup):
												
												for  x in range (len (tubeVoxelGrouped)):
													for  y in range (len (tubeVoxelGrouped[0])):
														for z in range (len (tubeVoxelGrouped[0][0])):
															if (tubeVoxelGrouped [x][y][z] >  neighbourGrp):
																tubeVoxelGrouped [x][y][z] -= 1	
#test if a goup has only one member 
#   member    member          member     
# [[x][y][z][x][y][z]]   OR [[x][y][z]]  
#      G R O U P             G R O U P

# a try catch block is nessasary to decide if a Group only has one member
# if a group has more than one member 
# member gets his own dimension
# if a group is only build up by one member is has not the dimension of member

												try:	
													x = self.__tubeGroup[neighbourGrp][0][0]
													oneMember = 0 
												except TypeError:
													x = self.__tubeGroup[neighbourGrp][0]
													y = self.__tubeGroup[neighbourGrp][1]
													z = self.__tubeGroup[neighbourGrp][2]
													self.__tubeGroup[foundGroup].append([x,y,z])	
													oneMember = 1
													tubeVoxelGrouped [x][y][z] = foundGroup	
														
												if (oneMember == 0):
													for member in range (len(self.__tubeGroup[neighbourGrp])):
														x = self.__tubeGroup[neighbourGrp][member][0]
														y = self.__tubeGroup[neighbourGrp][member][1]
														z = self.__tubeGroup[neighbourGrp][member][2]
														tubeVoxelGrouped [x][y][z] = foundGroup
													self.__tubeGroup[foundGroup].extend(self.__tubeGroup[neighbourGrp])
																																					
													
												del self. __tubeGroup[neighbourGrp]
												neighbourGrp = foundGroup
												continue
											if (neighbourGrp < foundGroup):
												for  x in range (len (tubeVoxelGrouped)):
													for  y in range (len (tubeVoxelGrouped[0])):
														for z in range (len (tubeVoxelGrouped[0][0])):
															if (tubeVoxelGrouped [x][y][z] >  foundGroup):
																tubeVoxelGrouped [x][y][z] -= 1													
												try:
													x = self.__tubeGroup[foundGroup][0][0]
													oneMember = 0 
												except TypeError:
													x = self.__tubeGroup[foundGroup][0]
													y = self.__tubeGroup[foundGroup][1]
													z = self.__tubeGroup[foundGroup][2]
													self.__tubeGroup[neighbourGrp].append([x,y,z])	
													oneMember = 1
													tubeVoxelGrouped [x][y][z] = neighbourGrp	
												if (oneMember == 0):
													for member in range (len(self.__tubeGroup[foundGroup])):
														x = self.__tubeGroup[foundGroup][member][0]
														y = self.__tubeGroup[foundGroup][member][1]
														z = self.__tubeGroup[foundGroup][member][2]
														tubeVoxelGrouped [x][y][z] = neighbourGrp
													self.__tubeGroup[neighbourGrp].extend(self.__tubeGroup[foundGroup])

												del self.__tubeGroup[foundGroup]
												foundGroup = neighbourGrp
												continue
# searching for an existing group in neighbourhood 		
										if (foundGroup < 0):
											self.__tubeGroup[neighbourGrp].append([xCount,yCount,zCount])
											foundGroup =  neighbourGrp
											tubeVoxelGrouped [xCount][yCount][zCount] = foundGroup
											
									
# if no group was found in neighbourhood a new group will be created 
						if (foundGroup == -1 ):
#							print "create new group: "+ str(len(self.__tubeGroup))
							foundGroup = len(self.__tubeGroup)
							tupelTMP = [([xCount,yCount,zCount])]
							self.__tubeGroup.append (tupelTMP)
							tubeVoxelGrouped [xCount][yCount][zCount] = foundGroup

#			outputLine = int ((xCount*100)/(len(self.__tubeDensity)))
			outputLine = int ((xCount*100)/(len(self.__tubeDensity)))
#			print str(outputLine)+" %\b\b\b\b\b",
			print str(outputLine)+" %\r",
			sys.stdout.flush()
		print "final groups: "+str(len(self.__tubeGroup))
		self.__groupVoxel = tubeVoxelGrouped
#returns
#   member    member          
# [[x][y][z][x][y][z]]   
#      G R O U P     
# groupes in TubeDx        
	def getTubeGroup(self):
		return self.__tubeGroup

#groupes
#[[x][y][z][x][y][z]]	

	def getGroupes (self):
		return  self.__tubeGroup
#### =====:-(  whoa scary those getters are

#voxelGroupGrid in tubeDX		
# returns [x][y][z] = group  
	def getGroups(self):
		return self.__groupVoxel
	


#voxelGroupGrid
#[x][y][z] = group
	
	def getVoxelGroupGrid (self):
		return self.__groupVoxel

