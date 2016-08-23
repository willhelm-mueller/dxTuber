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
#
##



####
# not implemented yet 
# first draft
# untestet 
###
from buildopendx import *
class averageDx(): 
	__origin = []
	__densityObjectArray = []
	__dimention = []
	__average = []
	def __init__(self, dxObjectArray):
		self.__densityObjectArray = dxObjectArray
		self.calcNewOrigin()
		self.calcNewDimention()
		self.__calcAverages()
# getting the lowest origin :
	def calcNewOrigin(self):
		origin = self.__densityObjectArray[0].getOrigin()
		for i in range(len (self.__densityObjectArray)):
#x			
			if (self.__densityObjectArray[i].getOrigin()[0] < origin[0]):
				origin[0] = self.__densityObjectArray[i].getOrigin()[0]
#y
			if (self.__densityObjectArray[i].getOrigin()[1] < origin[1]):
				origin[1] = self.__densityObjectArray[i].getOrigin()[1]
#z
			if (self.__densityObjectArray[i].getOrigin()[2] < origin[0]):
				origin[2] = self.__densityObjectArray[i].getOrigin()[2]
		self.__origin = origin
		print "New Origin:\n"+str(origin[0])+" "+str(origin[1])+" "+str(origin[2])
	
#calc new size:
	def calcNewDimention(self):
		dimention = self.__densityObjectArray[0].getDimention()
		for i in range(len (self.__densityObjectArray)):
#x			
			if (self.__densityObjectArray[i].getDimention()[0] < dimention[0]):
				dimention[0] = self.__densityObjectArray[i].getDimention()[0]
#y
			if (self.__densityObjectArray[i].getDimention()[1] < Dimention[1]):
				dimention[1] = self.__densityObjectArray[i].getDimention()[1]
#z
			if (self.__densityObjectArray[i].getDimention()[2] < Dimention[0]):
				dimention[2] = self.__densityObjectArray[i].getDimention()[2]
		self.__dimention = dimention
		print "New Dimention:\n"+str(dimention[0])+" "+str(dimention[1])+" "+str(dimention[2])
	def __calcAverages(self):
		sum =[[[0 for zR in range(self.__origin[0][0])] for yR in range(self.__origin[0])] for xR in range(self.__origin)]
		average =[[[0 for zR in range(self.__origin[0][0])] for yR in range(self.__origin[0])] for xR in range(self.__origin)]
#looping over all dx files
		for dxObjectCount in range(len (self.__densityObjectArray)):
#loop over the new grid 
			print "Start summing densities on file"+ str(dxObjectCount)
			for  xCount in range (len (self.__dimention)):
				for  yCount in range (len (self.__dimention[0])):
					for zCount in range (len (self.__dimention[0][0])):
#testing if current voxel lies inside of current dx grid 
# "left side"
						if (self.__origin[0] + xCount > self.__densityObjectArray[dxObjectCount].getOrigin()[0] and
							self.__origin[1] + yCount > self.__densityObjectArray[dxObjectCount].getOrigin()[1] and
							self.__origin[2] + zCount > self.__densityObjectArray[dxObjectCount].getOrigin()[2] and
#"right side"
							self.__origin[0] + xCount <  self.__densityObjectArray[dxObjectCount].getOrigin()[0] + self.__densityObjectArray[dxObjectCount].getDimention[0] and
							self.__origin[1] + yCount <  self.__densityObjectArray[dxObjectCount].getOrigin()[1] + self.__densityObjectArray[dxObjectCount].getDimention[1] and 
							self.__origin[2] + zCount <  self.__densityObjectArray[dxObjectCount].getOrigin()[2] + self.__densityObjectArray[dxObjectCount].getDimention[2] ):
#calculating shift in x y z direction 
								xShift = self.__origin[0] - self.__densityObjectArray[dxObjectCount].getOrigin()[0]
								yShift = self.__origin[1] - self.__densityObjectArray[dxObjectCount].getOrigin()[1]
								zShift = self.__origin[2] - self.__densityObjectArray[dxObjectCount].getOrigin()[2]
								sum[xCount][yCount][zCount] += self.__densityObjectArray[dxObjectCount].getDensity()[xShift+xCount][yShift+yCount][zShift+zCount]
		print "Calculating averages"
		for  xCount in range (len (self.__dimention)):
			for  yCount in range (len (self.__dimention[0])):
				for zCount in range (len (self.__dimention[0][0])):
					average [xCount][yCount][zCount]=sum[xCount][yCount][zCount] / (len (self.__densityObjectArray)
		self.__average = average
	def getDxObject(self=None):
		object = BuildOpenDx (self.__average, self.__densityObjectArray[0].getStepsize(), self.__origin, self.__dimention)
		return object
		
