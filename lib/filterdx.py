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
# v0.12
# +FilterByDensity 
#
#version 0.066
#- filter by neighbourmin varriable is now adjustable from gui 
#version 0.062 
#  changelog
#- protein & water dxObject are not nessasary any more 
###
from buildopendx import *
class FilterDx():
	__stepSize = ()
	__tube = []
	__minDiameter = ()
	__dxObjectTube =()
	
	def __init__(self, dxObjectTube, minDiameter=0):
		self.__tube = dxObjectTube.getDensity()
		self.__dxObjectTube = dxObjectTube
		self.__stepSize = dxObjectTube.getStepsize()
		self.__minDiameter = int (float(minDiameter) / float(self.__stepSize))
		
	def filterTunnelNeighbour(self = None,neighbourMin=10):
		print "Start filtering cavities by neighbour "+str(neighbourMin)
		tube  = [[[0 for zR in range(len(self.__tube[0][0]))] for yR in range(len(self.__tube[0]))] for xR in range(len(self.__tube))]
		for  xCount in range (len (self.__tube)):
			for  yCount in range (len (self.__tube[0])):
				for zCount in range (len (self.__tube[0][0])):
# counting neighbour voxels with densities 		
					counter = 0
					if (self.__tube[xCount][yCount][zCount] < 0.01):
						continue
					list = [-1,0,1]
					for xPos in  list:
						for yPos in  list:
							for zPos in list:
								if (self.__tube[xCount+xPos][yCount+yPos][zCount+zPos] > 0.01):
										counter +=1
					if (counter > neighbourMin):
						tube[xCount][yCount][zCount] =  self.__tube[xCount][yCount][zCount]
#			outputLine = int ((xCount*100)/(len(self.__tube)))
#			print str(outputLine)+" %\b\b\b\b\b",
		self.__tube = tube	
					
	def filterDistance(self = None):
		print "Start filtering by Distance "+str(self.__minDiameter)
		tube  = [[[0 for zR in range(len(self.__tube[0][0]))] for yR in range(len(self.__tube[0]))] for xR in range(len(self.__tube))]
		for  xCount in range (len (self.__tube)):
			for  yCount in range (len (self.__tube[0])):
				for zCount in range (len (self.__tube[0][0])):
# scanning x direction 		
					xDiameter = 1
					for xScan in range (xCount,len (self.__tube)):
						if (self.__tube[xScan][yCount][zCount] > 0.01 ):
							xDiameter += 1
						if (self.__tube[xScan][yCount][zCount] < 0.01 ):
							break
					
					xScan = xCount
					while (xScan > 0):
						xScan -=1
						if (self.__tube[xScan][yCount][zCount] > 0.01 ):
							xDiameter +=1			
						if (self.__tube[xScan][yCount][zCount] < 0.01 ):
							break	
#scanning y direction 
					yDiameter = 1
					for yScan in range (yCount,len (self.__tube[0])):
						if (self.__tube[xCount][yScan][zCount] > 0.01 ):
							yDiameter += 1
						if (self.__tube[xCount][yScan][zCount] < 0.01 ):
							break
					yScan = yCount
					while (yScan > 0):
						yScan -=1
						if (self.__tube[xCount][yScan][zCount] > 0.01 ):
							yDiameter +=1			
						if (self.__tube[xCount][yScan][zCount] < 0.01 ):
							break	
#scanning z direction 
					zDiameter = 1
					for zScan in range (zCount,len (self.__tube[0][0])):
						if (self.__tube[xCount][yCount][zScan] > 0.01 ):
							zDiameter += 1
						if (self.__tube[xCount][yCount][zScan] < 0.01 ):
							break					
					zScan = zCount
					while (zScan > 0):
						zScan -=1
						if (self.__tube[xCount][yCount][zScan] > 0.01 ):
							zDiameter +=1			
						if (self.__tube[xCount][yCount][zScan] < 0.01 ):
							break
					if (xDiameter +yDiameter+zDiameter < 2*self.__minDiameter):
						continue
# 2D could be implemented in future
#					if (xDiameter > self.__minDiameter and yDiameter > self.__minDiameter and zDiameter > 1):
#							tube[xCount][yCount][zCount] =  self.__tube[xCount][yCount][zCount]
#					if (xDiameter > self.__minDiameter and zDiameter > self.__minDiameter and yDiameter > 1):
#							tube[xCount][yCount][zCount] =  self.__tube[xCount][yCount][zCount]
#							
#					if (yDiameter > self.__minDiameter and zDiameter > self.__minDiameter and xDiameter > 1):
#							tube[xCount][yCount][zCount] =  self.__tube[xCount][yCount][zCount]			
#

#3D
					if (xDiameter > self.__minDiameter and yDiameter > self.__minDiameter and zDiameter > self.__minDiameter):
						tube[xCount][yCount][zCount] =  self.__tube[xCount][yCount][zCount]


#			outputLine = int ((xCount*100)/(len(self.__tube)))
#			print str(outputLine)+" %\b\b\b\b\b",		
		self.__tube = tube
		
	def filterByDensity(self,densityThreshold):
		print "Minimum residence probability: "+densityThreshold
		print "Start filtering..."
		densities = self.__dxObjectTube.getDensity()
		densities_filtered = [[[-1 for zR in range(len (densities[0][0]))] for yR in range(len (densities[0]))] for xR in range(len (densities))]
		for  xCount in range (len (densities)):
			for  yCount in range (len (densities[0])):
				for zCount in range (len (densities[0][0])):
					if float(densities[xCount][yCount][zCount]) > float(densityThreshold):
						densities_filtered[xCount][yCount][zCount] = densities[xCount][yCount][zCount]
				outputLine = int ((xCount*100)/len(densities))
				print str(outputLine)+" %\r",
#		tmp = (BuildOpenDx (density = densities_filtered,  stepSize = tubeDx.getDxObject().getStepsize(), origin = tubeDx.getDxObject().getOrigin(),dimention = tubeDx.getDxObject().getDimention()))
		self.__dxObjectTube.setDensity(densities_filtered)
	
# This routine deletes all densities INSIDE the given rectangle defined by (xmin,ymin,zmin) and (xmax,ymax,zmax) UNTESTET ROUTINE BEWARE !!!!!!! 	
	def deleteRectangleInside(self,minArray,mayArray):
		densities = self.__dxObjectTube.getDensity()
#		densities_filtered = [[[-1 for zR in range(len (densities[0][0]))] for yR in range(len (densities[0]))] for xR in range(len (densities))]
		origin = self.__dxObjectTube.getOrigin()
		for  xCount in range (len (densities)):
			for  yCount in range (len (densities[0])):
				for zCount in range (len (densities[0][0])):	
					x = float (float(xCount) * float(self.__stepSize)) + float(origin[0])
					y = float (float(yCount) * float(self.__stepSize)) + float(origin[1])
					z = float (float(zCount) * float(self.__stepSize)) + float(origin[2])					
					if x > float(minArray[0]) and x < float(maxArray[0]):
						if y > float(minArray[1]) and y < float(maxArray[1]):
							if z > float(minArray[2]) and z < float(maxArray[2]):
								densities[xCount][yCount][zCount] = 0
		self.__dxObjectTube.setDensity(densities)
		
	def getDxObject(self=None):
		object = BuildOpenDx (self.__dxObjectTube.getDensity(), self.__dxObjectTube.getStepsize(), self.__dxObjectTube.getOrigin(), self.__dxObjectTube.getDimention())
		return object
