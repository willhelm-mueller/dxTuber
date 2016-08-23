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
#
#since v0.073 all cavities will start at (choosen axis) = 1 (-> cavity_coord)
class AnalyseTube():
	__groups = []
	__chain = ()
	__voxelPlanes = []
	def __init__ (self, groups, chain):
		self.__chain = int(chain)  #### chain ? ? ?? ??  this should be cavity !!! 
		self.__groups = groups
	#	self.__method =''
	def analyseTubeArea(self, axis):
		print "Scanning cavity " + str(self.__chain)+" in "+axis+" direction areasize"	
		if (axis == 'x'):
			self.__voxelPlanes = [0 for m in range (len (self.__groups))]
			for  xCount in range (len (self.__groups)):
				for yCount in range (len (self.__groups[0])):
					for zCount in range (len (self.__groups[0][0])):
						if str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) != -1:
							self.__voxelPlanes [xCount] += 1
		if (axis == 'y'):
			self.__voxelPlanes = [0 for m in range (len (self.__groups[0]))]
			for  xCount in range (len (self.__groups)):
				for yCount in range (len (self.__groups[0])):
					for zCount in range (len (self.__groups[0][0])):
						if str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) != -1:				
							self.__voxelPlanes [yCount] += 1
		if (axis == 'z'):
			self.__voxelPlanes = [0 for m in range (len (self.__groups[0][0]))]
			for  xCount in range (len (self.__groups)):
				for yCount in range (len (self.__groups[0])):
					for zCount in range (len (self.__groups[0][0])):
						if str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) != -1:
							self.__voxelPlanes [zCount] += 1
								
		print  self.__voxelPlanes
	def analyseTubeDiameterMax(self, axis):
		print "Scanning cavity " + str(self.__chain)+" in "+axis+" direction for maximum diameter"		
		
		if (axis == 'x'):
			self.__voxelPlanes = [0 for m in range (len (self.__groups))]
			for  xCount in range (len (self.__groups)):
				maximum = 0
#find maximum diameter in z direction
				for yCount in range (len (self.__groups[0])):
					sum = 0 
					for zCount in range (len (self.__groups[0][0])):
#if a gap in the tunnel is found espacily at the corners ... 
						if (sum > 0 and str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) == -1):
							if sum > maximum:
								maximum = sum		
							sum = 0	
						if str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) != -1:
							sum += 1
					if sum > maximum:
						maximum = sum
				self.__voxelPlanes [xCount] = maximum
#find maximum diameter in y direction
				for zCount in range (len (self.__groups[0][0])):
					sum = 0 
					for yCount in range (len (self.__groups[0])):
#if a gap in the tunnel is found espacily at the corners ... 
						if (sum > 0 and str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) == -1):
							if sum > maximum:
								maximum = sum		
							sum = 0	
						if str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) != -1:
							sum += 1
					if sum > maximum:
						maximum = sum
				self.__voxelPlanes [xCount] = maximum

		if (axis == 'y'):
			self.__voxelPlanes = [0 for m in range (len (self.__groups[0]))]
			for yCount in range (len (self.__groups[0])):
				maximum = 0
#find maximum diameter in z direction
				for  xCount in range (len (self.__groups)):
					sum = 0 
					for zCount in range (len (self.__groups[0][0])):
#if a gap in the tunnel is found espacily at the corners ... 
						if (sum > 0 and str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) == -1):	
							if sum > maximum:
								maximum = sum		
							sum = 0	
						if str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) != -1:
							sum += 1
					if sum > maximum:
						maximum = sum
				self.__voxelPlanes [yCount] = maximum					
#find maximum diameter in x direction
				for zCount in range (len (self.__groups[0][0])):
					sum = 0 
					for  xCount in range (len (self.__groups)):
#if a gap in the tunnel is found espacily at the corners ... 
						if (sum > 0 and str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) == -1):	
							if sum > maximum:
								maximum = sum		
							sum = 0	
						if str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) != -1:
							sum += 1
					if sum > maximum:
						maximum = sum
				self.__voxelPlanes [yCount] = maximum
	
		if (axis == 'z'):
			self.__voxelPlanes = [0 for m in range (len (self.__groups[0][0]))]
			for zCount in range (len (self.__groups[0][0])):
				maximum = 0
#find maximum diameter in x direction
				for yCount in range (len (self.__groups[0])):
					sum = 0 
					for  xCount in range (len (self.__groups)):
#if a gap in the tunnel is found espacily at the corners ... 
						#if (sum > 0 and self.__groups[xCount-1][yCount][zCount] !=  self.__chain):
						if (sum > 0 and str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) == -1):
							if sum > maximum:
								maximum = sum		
							sum = 0	
						if str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) != -1:
							sum += 1
					if sum > maximum:
						maximum = sum
				self.__voxelPlanes [zCount] = maximum
				
#find maximum diameter in y direction
				for  xCount in range (len (self.__groups)):
					sum = 0 
					for yCount in range (len (self.__groups[0])):
#if a gap in the tunnel is found espacily at the corners ... 
						if (sum > 0 and str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) == -1):
							if sum > maximum:
								maximum = sum		
							sum = 0	
						if str(self.__groups[xCount][yCount][zCount]).find(str(self.__chain)) != -1:
							sum += 1
					if sum > maximum:
						maximum = sum
				self.__voxelPlanes [zCount] = maximum	
		print  self.__voxelPlanes		
		
# since v0.073 all cavities will start at (choosen axis) = 1 (-> cavity_coord)
	def writeStatistics(self, file):
		statisticFH = open  (file,'w')
		cavity_coord = 0
		for axisCount in range (len (self.__voxelPlanes)):
			if cavity_coord > 0:
				cavity_coord += 1
			if self.__voxelPlanes[axisCount] > 0:
				if cavity_coord == 0:
					cavity_coord = 1
				statisticFH.write (str(cavity_coord)+" " +str(self.__voxelPlanes[axisCount])+"\n")
#since 
			else:
				statisticFH.write (str(cavity_coord)+" 0\n")
		statisticFH.close()
		print "Saved analysed cavity "+ str(self.__chain) +" in\n" + file 
		
