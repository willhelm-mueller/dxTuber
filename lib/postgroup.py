
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
#  +'core_cavities_after_filter.pdb' stores the grouped core cavities 
#
# dxTuber v0.2
# +new routine to postgroup / seperate existing cavities, deviding cavities in subcavities 
#
#

import re, math 
from tubedx import *
from grouptubes import *
from buildopendx import * 
from settings import *
### for testing only ... 
from writepdb import * 
####





#### this class seperates previously detected cavities. Postgrouping. 
class PostGroup():
#groupes
#[[x][y][z][x][y][z]]		
	__cavityGroup =[]
#	tubeVoxelGrouped =[]
	__groupCount = 0
	
	
# returns [x][y][z] = group 	
	__groupVoxel= []
	
## opendx Object containing the cavity voxels	
	__cavitysDxObject = ()
	
# the input tubedx	
	__tubeDx = () 
	__version = ()
	def __init__(self, tubeDx):
# returns [x][y][z] = group 
		self.__groupVoxel = tubeDx.getVoxelGroupGrid()
#groupes
#[[x][y][z][x][y][z]]	
		self.__cavityGroup = tubeDx.getGroupes()
		
		self.__cavitysDxObject = tubeDx.getDxObject() 
		self.__tubeDx = tubeDx 
		settings = Settings()
		self.__version = settings.getVersion()
		
		
## postgroupArray contains a collection of cavityID's to postgroup  [int]	
#returns an "density" array containung Neighborhod filtered values 	
	def calcNeighbors (self, cavityID, edgeLength = 2 ):
		
#		cubicSize = (edgeLength+edgeLength+1 )  * (edgeLength+edgeLength+1 ) * (edgeLength+edgeLength+1 )    #fix this !!! 
#		print "Calculating for each voxel the sum of its neighbors in a "+ str(cubicSize) +" cubic box"   #  fix this ... 
		
		boxArray = [[[-1 for zR in range(len (self.__cavitysDxObject.getDensity()[0][0]))] for yR in range(len (self.__cavitysDxObject.getDensity()[0]))] for xR in range(len (self.__cavitysDxObject.getDensity()))]
#		for cavityID in postGroupArray:
		for x in range (len (self.__cavitysDxObject.getDensity())):
			for y in range (len (self.__cavitysDxObject.getDensity()[0])):
				for z in range (len (self.__cavitysDxObject.getDensity()[0][0])):
#					if not re.match(cavityID , str(self.__groupVoxel[x][y][z])) :
#					if not ( cavityID == str(self.__groupVoxel[x][y][z]) ):

## if not cavity   : all cavities will be regrouped :)
					if cavityID != 'all':
						if not ( cavityID == str(self.__groupVoxel[x][y][z]) ):
							continue
					currentBox = 1 
					negEdgeLenght = edgeLength - edgeLength - edgeLength
					for xCurrent in range (negEdgeLenght, (edgeLength+1)):
						for yCurrent in range (negEdgeLenght, (edgeLength+1)):
							for zCurrent in range (negEdgeLenght, (edgeLength+1)):
								
								if xCurrent == 0 and yCurrent == 0 and zCurrent == 0 :
									continue
								try:
									if cavityID == str(self.__groupVoxel[x+xCurrent][y+yCurrent][z+zCurrent]) :
										currentBox += 1
									elif cavityID == 'all' and  self.__cavitysDxObject.getDensity()[x+xCurrent][y+yCurrent][z+zCurrent] > 0:
										currentBox += 1
								except IndexError:
# Donothing 						
									a = 1
# wuha nothing done :> 									
					boxArray[x][y][z] = currentBox
		return boxArray
		
## 
# devides current dxObject into 2 groups containing voxels below (<) threshold and (>=) greater or equal the threshold
	def separateByValue(self, threshold,  dxObject = __cavitysDxObject):
		firstGroup  = [[[0 for zR in range(len (dxObject.getDensity()[0][0]))] for yR in range(len (dxObject.getDensity()[0]))] for xR in range(len (dxObject.getDensity()))]
		secondGroup = [[[0 for zR in range(len (dxObject.getDensity()[0][0]))] for yR in range(len (dxObject.getDensity()[0]))] for xR in range(len (dxObject.getDensity()))]
		for x in range (len (dxObject.getDensity())):
			for y in range (len (dxObject.getDensity()[0])):
				for z in range (len (dxObject.getDensity()[0][0])):
					if dxObject.getDensity()[x][y][z] < threshold:
						secondGroup[x][y][z] = dxObject.getDensity()[x][y][z]
					else:
						firstGroup[x][y][z]  = dxObject.getDensity()[x][y][z]
		tmpArray = [firstGroup, secondGroup]
		return tmpArray
#		return firstGroup, secondGroup

### 
# it seems that this method has an malfunction 
###
	def joinByDistance (self, firstTubeDx, secondOpenDx, distCutoff = -1):
		
#         first group             second group  ..... 
#[ [x][y][z] [x][y][z] [x][y][z] ]
		newGroupes = firstTubeDx.getGroupes()

#[x][y][z] = groupID
		newVoxelGroupGrid = firstTubeDx.getVoxelGroupGrid()
		firstDensities = firstTubeDx.getDxObject().getDensity()
		
		for x in range (len (self.__cavitysDxObject.getDensity())):
			for y in range (len (self.__cavitysDxObject.getDensity()[0])):
				for z in range (len (self.__cavitysDxObject.getDensity()[0][0])):
					if firstTubeDx.getDxObject().getDensity()[x][y][z] > 0:   # voxel is member of the "major" (first) selection 
						continue  
					size = 1
					foundOneGroup = False
					foundOneGroupXYZ = []
					
					foundMultipleGroups = []
					foundMultipleGroupsXYZ = []
##
#
# scanning neighborhood for major cavities .... 
##					
					
					while (size <= distCutoff and foundOneGroup == False):
#					if distCutoff > 0 and distCutoff > size:
#						
# a routine which gathers voxels obove cutoff range should be implemented   
#
						negLen = size -size -size 
						posLen = size
						
	# searching for "major" cavities until the cutOff is reached					
						for xCurrent in range (negLen, (posLen+1)):
							for yCurrent in range (negLen, (posLen+1)):
								for zCurrent in range (negLen, (posLen+1)):
									
									if (x+xCurrent < len(firstTubeDx.getDxObject().getDensity()) and  
										y+yCurrent < len (firstTubeDx.getDxObject().getDensity()[0]) and  
										z+zCurrent < len( firstTubeDx.getDxObject().getDensity()[0][0]) and # checking if voxel is in array ... ... index out of bound error ... 
										x+xCurrent >= 0 and y+yCurrent >= 0 and  z+zCurrent >= 0 and 
										self.__tubeDx.getDxObject().getDensity()[x+xCurrent][y+yCurrent][z+zCurrent] >= self.__tubeDx.getSolventThreshold()   # only voxels above previosly defined threshold !! 
										
										):
#										print "do"

#										if firstTubeDx.getDxObject().getDensity()[x+xCurrent][y+yCurrent][z+zCurrent] > 0 and not foundOneGroup:
#											foundOneGroupXYZ = [x+xCurrent, y+yCurrent, z+zCurrent]
#											foundOneGroup = firstTubeDx.getVoxelGroupGrid()[x+xCurrent][y+yCurrent][z+zCurrent]
#											print "yo" 
#											continue
#										if firstTubeDx.getDxObject().getDensity()[x+xCurrent][y+yCurrent][z+zCurrent] > 0 and foundOneGroup:
#											foundMultipleGroupsXYZ.append([x+xCurrent, y+yCurrent, z+zCurrent])		
#											foundMultipleGroupsXYZ.append(firstTubeDx.getVoxelGroupGrid()[x+xCurrent][y+yCurrent][z+zCurrent])
#											print "yo2" 
#											print foundMultipleGroupsXYZ
			#							if firstTubeDx.getDxObject().getDensity()[x+xCurrent][y+yCurrent][z+zCurrent] > 0:
										if firstDensities[x+xCurrent][y+yCurrent][z+zCurrent] > 0:
											tmpArray = [x+xCurrent, y+yCurrent, z+zCurrent]
											foundMultipleGroupsXYZ.append(tmpArray)		
											foundMultipleGroups.append(firstTubeDx.getVoxelGroupGrid()[x+xCurrent][y+yCurrent][z+zCurrent])


						size +=1
#					print "finished while" 
#### Evaluating to which major group the current voxel belongs : 
					
	#				if foundOneGroup:
#						print "found" 
					if len(foundMultipleGroups) > 1:
# do something							
						#a= 1 
# inserting current voxel into existing group:
# compare all groups get the smalest distance vector ! 
# 
#			
#						print "Ja"
						minLength = -1
						minGroup = -1
						for member in range (len(foundMultipleGroupsXYZ)):
							xG = foundMultipleGroupsXYZ[member][0]
							yG = foundMultipleGroupsXYZ[member][1]
							zG = foundMultipleGroupsXYZ[member][2]
							length = math.sqrt( (x-xG)**2 +(y-yG)**2 +(z-zG)**2 )
							if minLength == -1 :
								minLenght = length
								minGroup = foundMultipleGroups[member]
								minGroupIndex = member
								continue
							if minLength > length:
								
								minlegth = length 
								minGroup = foundMultipleGroups[member]
								minGroupIndex = member
#
# the mighty try catch block !
#
#
						try:
							xG =  firstTubeDx.getGroupes()[minGroup][0][0]
							oneMember = 0 
						except TypeError:
							xG = foundMultipleGroupsXYZ[minGroupIndex][0]
							yG = foundMultipleGroupsXYZ[minGroupIndex][1]
							zG = foundMultipleGroupsXYZ[minGroupIndex][2]
	#						newGroupes[minGroup].append([xG,yG,zG])	
							newGroupes[minGroup].append([x,y,z])	
							oneMember = 1
							newVoxelGroupGrid[x][y][z] = minGroup	
						if (oneMember == 0):
#### test this !!!
#							print foundMultipleGroupsXYZ
							#newGroupes[minGroup].append(foundMultipleGroupsXYZ[minGroupIndex])
							newGroupes[minGroup].append([x,y,z])	
							newVoxelGroupGrid[x][y][z] = minGroup
#### this passage could be buggy either extend or append .... 		
	




					elif len(foundMultipleGroups) == 1: #### only one group was found 
						
						try:
							xG =  firstTubeDx.getGroupes()[foundMultipleGroupsXYZ[0]][0][0]
							oneMember = 0 
						except TypeError:
#							print foundMultipleGroupsXYZ
							xG = foundMultipleGroupsXYZ[0][0]
							yG = foundMultipleGroupsXYZ[0][1]
							zG = foundMultipleGroupsXYZ[0][2]
#							newGroupes[foundMultipleGroups[0]].append([xG,yG,zG])	
							newGroupes[foundMultipleGroups[0]].append([x,y,z])	
							oneMember = 1
							newVoxelGroupGrid[x][y][z] = foundMultipleGroupsXYZ[0]
						if (oneMember == 0):
#### test this !!!
							#newGroupes[minGroup].append(foundMultipleGroupsXYZ)
							newGroupes[minGroup].append([x,y,z])	
							newVoxelGroupGrid[x][y][z] = minGroup	
#### this passage could be buggy either extend or append .... 		
			outputLine = int ((x*100)/(len (self.__cavitysDxObject.getDensity())))
			print str(outputLine)+" %\r",
			sys.stdout.flush()			
			len (self.__cavitysDxObject.getDensity())
						
		print "Done"
		newCavitiesTubeDx = TubeDx (
							openDxObject =self.__cavitysDxObject ,      # real densities
							filename = self.__tubeDx.getFilename(), 
							proteinObject= self.__tubeDx.getProteinObject(), 
							waterObject= self.__tubeDx.getWaterObject(), 
							scanMethod = self.__tubeDx.getScanMethod(), 
							scanned=self.__tubeDx.getScanned(),
							grouped='Yes', 
							groupes= newGroupes, 
							VoxelGroupGrid = newVoxelGroupGrid, 
							minDiameter = self.__tubeDx.getMinDiameter(), 
							protThreshold = self.__tubeDx.getProtThreshold(), 
							solventThreshold =self.__tubeDx.getSolventThreshold(), 
							version = self.__version, 
							protFile =self.__tubeDx.getProtFile(), 
							solvFile = self.__tubeDx.getSolvFile(), 
							filterApplied = self.__tubeDx.getFilterApplied(), 
							)


		return newCavitiesTubeDx
					

	def joinByDistanceMajorGroup(self, firstTubeDx, secondOpenDx, distCutoff = 8):
		
#         first group             second group  ..... 
#[ [x][y][z] [x][y][z] [x][y][z] ]
		newGroupes = firstTubeDx.getGroupes()

#[x][y][z] = groupID
		newVoxelGroupGrid = firstTubeDx.getVoxelGroupGrid()
		
#[x][y][z] = distance to a major group before 
		newVoxelGroupGridMinDist = [[[-1 for zR in range(len (self.__cavitysDxObject.getDensity()[0][0]))] for yR in range(len (self.__cavitysDxObject.getDensity()[0]))] for xR in range(len (self.__cavitysDxObject.getDensity()))]
		i = 0
		groupLength = len (firstTubeDx.getGroupes()) 
		print "Cavities to process",groupLength
		for groupID in firstTubeDx.getGroupes():
			
			try:
				xG =  groupID[0][0]
				oneMember = 0 
			except TypeError:
				oneMember = 1
				
				
			if oneMember:
				size = 1
				while (size <= distCutoff):
					negLen = size -size -size 
					posLen = size
					
					for xCurrent in range (negLen, (posLen+1)):
						for yCurrent in range (negLen, (posLen+1)):
							for zCurrent in range (negLen, (posLen+1)):
								if xCurrent == 0 and yCurrent == 0 and zCurrent == 0:
									continue
								if firstTubeDx.getDxObject().getDensity()[xCurrent][yCurrent][zCurrent] > 0:   # voxel is member of the "major" (first) selection 
									continue  
								xG = groupID[0]
								yG = groupID[1]
								zG = groupID[2]
								
								
#								try :
#									a = newVoxelGroupGrid[xCurrent+xG][yCurrent+yG][zCurrent+zG]
#									if a == i:
#										continue
#								except IndexError:
#									continue
								
								if (xG+xCurrent < len(firstTubeDx.getDxObject().getDensity()) and  
									yG+yCurrent < len (firstTubeDx.getDxObject().getDensity()[0]) and  
									zG+zCurrent < len( firstTubeDx.getDxObject().getDensity()[0][0]) and # checking if voxel is in array ... ... index out of bound error ... 
									xG+xCurrent >= 0 and yG+yCurrent >= 0 and  zG+zCurrent >= 0 and 
									self.__tubeDx.getDxObject().getDensity()[xG+xCurrent][yG+yCurrent][zG+zCurrent] >= self.__tubeDx.getSolventThreshold()
									):
#								x = xCurrent + xG
# xCurrent   & yCurrent & zCurrent contain already  delta x,y,z .... 
									length = math.sqrt( (xCurrent)**2 +(yCurrent)**2 +(zCurrent)**2 )
										
									if ((length < newVoxelGroupGridMinDist[xCurrent+xG][yCurrent+yG][zCurrent+zG] and newVoxelGroupGridMinDist[xCurrent+xG][yCurrent+yG][zCurrent+zG] != -1) 
												or newVoxelGroupGridMinDist[xCurrent+xG][yCurrent+yG][zCurrent+zG] == -1):
										newVoxelGroupGridMinDist[xCurrent+xG][yCurrent+yG][zCurrent+zG] = length
										newVoxelGroupGrid[xCurrent+xG][yCurrent+yG][zCurrent+zG] = i
										
				
			if oneMember == 0:
				memberCount = 0 
				currentGroupLength = len (groupID)
				for member in groupID:
					
					size = 1
					while (size <= distCutoff):
						negLen = size -size -size 
						posLen = size
						
						for xCurrent in range (negLen, (posLen+1)):
							for yCurrent in range (negLen, (posLen+1)):
								for zCurrent in range (negLen, (posLen+1)):
									if xCurrent == 0 and yCurrent == 0 and zCurrent == 0:
										continue
#									if firstTubeDx.getDxObject().getDensity()[xCurrent][yCurrent][zCurrent] > 0:   # voxel is member of the "major" (first) selection 
#										continue  
										
 # only voxels above previosly defined threshold !! 
									xG = member[0]
									yG = member[1]
									zG = member[2]

#									try :
#										a = newVoxelGroupGrid[xCurrent+xG][yCurrent+yG][zCurrent+zG]
#										if a == i:
#											continue
#									except IndexError:#
										#continue
										
									if (xG+xCurrent < len (firstTubeDx.getDxObject().getDensity()) and  
										yG+yCurrent < len (firstTubeDx.getDxObject().getDensity()[0]) and  
										zG+zCurrent < len (firstTubeDx.getDxObject().getDensity()[0][0]) and # checking if voxel is in array ... ... index out of bound error ... 
										xG+xCurrent >= 0 and yG+yCurrent >= 0 and  zG+zCurrent >= 0 and
										self.__tubeDx.getDxObject().getDensity()[xG+xCurrent][yG+yCurrent][zG+zCurrent] >= self.__tubeDx.getSolventThreshold()
										):
																	
	#								x = xCurrent + xG
	# xCurrent   & yCurrent & zCurrent contain already  delta x,y,z .... 
										length = math.sqrt( (xCurrent)**2 +(yCurrent)**2 +(zCurrent)**2 )
#										print "yo" 
										if ((length < newVoxelGroupGridMinDist[xCurrent+xG][yCurrent+yG][zCurrent+zG] and newVoxelGroupGridMinDist[xCurrent+xG][yCurrent+yG][zCurrent+zG] != -1) 
													or newVoxelGroupGridMinDist[xCurrent+xG][yCurrent+yG][zCurrent+zG] == -1):
											newVoxelGroupGridMinDist[xCurrent+xG][yCurrent+yG][zCurrent+zG] = length
											newVoxelGroupGrid[xCurrent+xG][yCurrent+yG][zCurrent+zG] = i				
						size += 1
						
					memberCount += 1
#					outputLine = int ((memberCount*100)/(currentGroupLength))
#					print str(outputLine)+" %\r",			
					print "Analysing member",memberCount,"/",currentGroupLength,"\r",
					sys.stdout.flush()
					
					
					
#			outputLine = int ((i*100)/(len (firstTubeDx.getGroupes())))
#			print str(outputLine)+" %\r",
			print  "\nProcessed cavity",i
			i += 1 
			
			
									
		for x in range (len (newVoxelGroupGridMinDist)):
			for y in range (len (newVoxelGroupGridMinDist[0])):
				for z in range (len (newVoxelGroupGridMinDist[0][0])):	
					if newVoxelGroupGridMinDist[x][y][z]  >= self.__tubeDx.getSolventThreshold() :
						newGroupes[newVoxelGroupGrid[x][y][z]].append([x,y,z])
							
							
		newCavitiesTubeDx = TubeDx (
							openDxObject =self.__cavitysDxObject ,      # real densities
							filename = self.__tubeDx.getFilename(), 
							proteinObject= self.__tubeDx.getProteinObject(), 
							waterObject= self.__tubeDx.getWaterObject(), 
							scanMethod = self.__tubeDx.getScanMethod(), 
							scanned=self.__tubeDx.getScanned(),
							grouped='Yes', 
							groupes= newGroupes, 
							VoxelGroupGrid = newVoxelGroupGrid, 
							minDiameter = self.__tubeDx.getMinDiameter(), 
							protThreshold = self.__tubeDx.getProtThreshold(), 
							solventThreshold =self.__tubeDx.getSolventThreshold(), 
							version = self.__version, 
							protFile =self.__tubeDx.getProtFile(), 
							solvFile = self.__tubeDx.getSolvFile(), 
							filterApplied = self.__tubeDx.getFilterApplied(), 
							)


		return newCavitiesTubeDx							

###
# This routine regroups cavities, each previously defined will be regrouped by grouptubes.py 
# Regrouping is an advantage for join by distance routines cause theire results contain where not all voxels are connected
###


	def reGroup(self, tubeDx):
		print "Regrouping"
#groupes
#[[x][y][z][x][y][z]]			
		groupes =[]
#voxelGroupGrid
#[x][y][z] = group
		densities = tubeDx.getDxObject().getDensity()
		voxelGroupGrid = [[[-1 for zR in range(len (densities[0][0]))] for yR in range(len (densities[0]))] for xR in range(len (densities))]
		for i in range (len(tubeDx.getGroupes())):
			print "Group",i,"/",len(tubeDx.getGroupes())
			
			currentGroupDensities = [[[0 for zR in range(len (densities[0][0]))] for yR in range(len (densities[0]))] for xR in range(len (densities))]
			try:
				xG =  tubeDx.getGroupes()[i][0][0]
				oneMember = 0 
			except TypeError:
				oneMember = 1			
			if oneMember:
				groupes.append(tubeDx.getGroupes()[i])
				voxelGroupGrid[tubeDx.getGroupes()[i][0]][tubeDx.getGroupes()[i][1]][tubeDx.getGroupes()[i][2]] = len(groupes)
			if not oneMember:
				oldLen = len (groupes)
				
				for member in tubeDx.getGroupes()[i]:
#					x = member[0]
#					y = member[1]
#					z = member[2]
					currentGroupDensities[member[0]][member[1]][member[2]] = tubeDx.getDxObject().getDensity()[member[0]][member[1]][member[2]]
	
				currentOpenDxObject = BuildOpenDx (density = currentGroupDensities, 
													stepSize = tubeDx.getDxObject().getStepsize() , 
													origin = tubeDx.getDxObject().getOrigin(),
													dimention = tubeDx.getDxObject().getDimention()
													)
				groupThis = GroupTubes (currentOpenDxObject)
				groupThis.findGroups()
				groupes.extend(groupThis.getTubeGroup())
				newLen = len (groupes)
				if newLen - oldLen > 1:
#					print "huh"
					for groupIndex in range (oldLen, newLen-1):
						for member in groupes[groupIndex]:
#							print member,member[0],member[1],member[2]
							voxelGroupGrid[member[0]][member[1]][member[2]] = groupIndex
				else:
					for member in groupes[newLen-1]:
#						print member,member[0]
						voxelGroupGrid[member[0]][member[1]][member[2]] = newLen-1	
						
		print len (groupes)					
### grouping the rest ... :)	
		print "Grouping none core cavities"
#		dxObject = tubeDx.getDxObject()
		dxObject = self.__cavitysDxObject
		currentGroupDensities = [[[0 for zR in range(len (densities[0][0]))] for yR in range(len (densities[0]))] for xR in range(len (densities))]
		for x in range (len (dxObject.getDensity())):
			for y in range (len (dxObject.getDensity()[0])):
				for z in range (len (dxObject.getDensity()[0][0])):
					if voxelGroupGrid[x][y][z] == -1 and dxObject.getDensity()[x][y][z] > 0:
#						print "hu"
						currentGroupDensities[x][y][z] = dxObject.getDensity()[x][y][z]
						
		currentOpenDxObject = BuildOpenDx (density = currentGroupDensities, 
											stepSize = tubeDx.getDxObject().getStepsize() , 
											origin = tubeDx.getDxObject().getOrigin(),
											dimention = tubeDx.getDxObject().getDimention()
											)		
		oldLen  = len (groupes)
		groupThis = GroupTubes (currentOpenDxObject)
		groupThis.findGroups()
		groupes.extend(groupThis.getTubeGroup())
		newLen = len (groupes)
		if newLen - oldLen > 1:
#					print "huh"
			for groupIndex in range (oldLen, newLen-1):
				for member in groupes[groupIndex]:
#							print member,member[0],member[1],member[2]
					voxelGroupGrid[member[0]][member[1]][member[2]] = groupIndex
		else:
			for member in groupes[newLen-1]:
#						print member,member[0]
				voxelGroupGrid[member[0]][member[1]][member[2]] = newLen-1			



		print len (groupes)	
#		print groupes
		newCavitiesTubeDx = TubeDx (
							openDxObject = tubeDx.getDxObject() ,      # real densities
							filename = tubeDx.getFilename(), 
							proteinObject= tubeDx.getProteinObject(), 
							waterObject= tubeDx.getWaterObject(), 
							scanMethod = tubeDx.getScanMethod(), 
							scanned=tubeDx.getScanned(),
							grouped='Yes', 
							groupes= groupes, 
							VoxelGroupGrid = voxelGroupGrid, 
							minDiameter = tubeDx.getMinDiameter(), 
							protThreshold = tubeDx.getProtThreshold(), 
							solventThreshold =tubeDx.getSolventThreshold(), 
							version = self.__version, 
							protFile =tubeDx.getProtFile(), 
							solvFile = tubeDx.getSolvFile(), 
							filterApplied = tubeDx.getFilterApplied(), 
							)
		return newCavitiesTubeDx

				
#### 
#
# this is the "main" method for neighborhood driven postprocessing .... 
#


	def postGroup_Neighbor(self, threshold, cavityID, edgeLength = 2 ,  distCutoff = 8):
		
		neighborOpenDx = BuildOpenDx (density = self.calcNeighbors (cavityID = cavityID, edgeLength = edgeLength), 
									stepSize = self.__cavitysDxObject.getStepsize() , 
									origin = self.__cavitysDxObject.getOrigin(),
									dimention = self.__cavitysDxObject.getDimention()
									)
		print "Deviding cavity",cavityID,"in subcavites. Threshold =",threshold
		densityArray = self.separateByValue (threshold, neighborOpenDx)
		
		firstOpenDx = BuildOpenDx (density = densityArray[0], 
									stepSize = self.__cavitysDxObject.getStepsize() , 
									origin = self.__cavitysDxObject.getOrigin(),
									dimention = self.__cavitysDxObject.getDimention()
		 						)
		secondOpenDx = BuildOpenDx (density = densityArray[1], 
									stepSize = self.__cavitysDxObject.getStepsize() , 
									origin = self.__cavitysDxObject.getOrigin(),
									dimention = self.__cavitysDxObject.getDimention()
		 						)
# above threshold ! 


		firstGrouped = GroupTubes(firstOpenDx)
#		print densityArray[0]
		firstGrouped.findGroups()


		tmpTubeDx = TubeDx (
							openDxObject =firstOpenDx ,      # <<<<----- neighbor values
							filename = self.__tubeDx.getFilename(), 
							proteinObject= self.__tubeDx.getProteinObject(), 
							waterObject= self.__tubeDx.getWaterObject(), 
							scanMethod = self.__tubeDx.getScanMethod(), 
							scanned=self.__tubeDx.getScanned(),
							grouped='Yes', 
							groupes= firstGrouped.getTubeGroup(), 
							VoxelGroupGrid = firstGrouped.getVoxelGroupGrid(), 
							minDiameter = self.__tubeDx.getMinDiameter(), 
							protThreshold = self.__tubeDx.getProtThreshold(), 
							solventThreshold =self.__tubeDx.getSolventThreshold(), 
							version = self.__version, 
							protFile =self.__tubeDx.getProtFile(), 
							solvFile = self.__tubeDx.getSolvFile(), 
							filterApplied = self.__tubeDx.getFilterApplied(), 
							)

#
# test ... lemme see if this can be written into pdb 
#		
		print "### Debugging ###"
		test = WritePDB (tmpTubeDx)
		test.writeGroups(filename = 'core_cavities_after_filter.pdb', groupArray = firstGrouped.getTubeGroup())
		print "###/Debugging ###"
		

		
		
		firstGroupedTubeDx = TubeDx (
							openDxObject =firstOpenDx ,      # <<<<----- neighbor values
							filename = self.__tubeDx.getFilename(), 
							proteinObject= self.__tubeDx.getProteinObject(), 
							waterObject= self.__tubeDx.getWaterObject(), 
							scanMethod = self.__tubeDx.getScanMethod(), 
							scanned=self.__tubeDx.getScanned(),
							grouped='Yes',  
							groupes= firstGrouped.getTubeGroup(), 
							VoxelGroupGrid = firstGrouped.getGroups(), 
							minDiameter = self.__tubeDx.getMinDiameter(), 
							protThreshold = self.__tubeDx.getProtThreshold(), 
							solventThreshold =self.__tubeDx.getSolventThreshold(), 
							version = self.__version, 
							protFile =self.__tubeDx.getProtFile(), 
							solvFile = self.__tubeDx.getSolvFile(), 
							filterApplied = self.__tubeDx.getFilterApplied(), 
							)
		print "Separating ... " 
#		return self.joinByDistance (firstTubeDx = firstGroupedTubeDx, secondOpenDx = secondOpenDx   , distCutoff = 3)
### be carefull hard coded distance cutoff !!!  
##
# this makes sence for acrb ... in future the distCutoff should be a cmd parameter ... 
#
		joinedTubeDx = self.joinByDistanceMajorGroup (firstTubeDx = firstGroupedTubeDx, secondOpenDx = secondOpenDx   , distCutoff = distCutoff)  
		
		return self.reGroup (tubeDx = joinedTubeDx)  


