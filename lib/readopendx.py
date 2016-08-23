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
######
# v. 0.083
#- floats as stepsize are now supported
#
# v. 0.066 
#- setting density to 0 if a negative density is read
#- removed bug if last row contains fever than 3 entries
######
import re
from buildopendx import *
class ReadOpenDx():
	__dxfile =()
	__origin =[]
	__transformMatrix = []
	__size = []
	__stepSize = 0
	def __init__ (self, dxFile):
		if (not dxFile):
			print "Error no intputfile"
#			exit 
		self.__dxFile = dxFile

		
# For details OpenDx fileformat visit opendx.org 
# and http://apbs.wustl.edu/MediaWiki/index.php/OpenDX_scalar_data_format
# http://www.poissonboltzmann.org/file-formats/mesh-and-data-formats/opendx-scalar-data
				
	def importDx(self=None):
		dxFile = self.__dxFile
		dxFH = open(dxFile,"r")
		dxlines = dxFH.readlines()
		transformMatrix = []
		x=0
		y=0
		z=0
		row = 1
		for line in dxlines:
			regExp = re.compile ('object 1')
			if (regExp.match(line)):
				self.__size = re.findall('\d+', line)
				del self.__size[0]
				for i in range(3):
					self.__size[i] = int(self.__size[i])
				continue

			if (re.match('origin',line)):
				self.__origin = re.findall('(-?[0-9]*\.?-?[0-9]+)', line)
				self.__origin[0] = float(self.__origin[0])
				self.__origin[1] = float(self.__origin[1])
				self.__origin[2] = float(self.__origin[2])
				print 'Origin \nx: '+str(self.__origin[0])+'\ny: '+str(self.__origin[1])+'\nz: '+str(self.__origin[2])
				continue 
				
#  transformMatrix:
#  transformMatrix[0] transformation to get to middle of the continue boxes x-value
#  transformMatrix[1] transformation to get to middle of the continue boxes y-value etc ... 
			if (re.match('delta',line)):
				if self.__stepSize > 0:
					continue
#				self.__transformMatrix.append (re.findall('(-?[0-9]*\.?-?[0-9]+)', line))
#				self.__transformMatrix.append (re.findall('\d*\.*\d+', line))
				self.__stepSize = (re.findall('\d*\.*\d+', line)) [0]
				print "Stepsize: " + str(self.__stepSize)
				continue
			if (re.match('^-*[0-9]', line)): 
#				initialysing density array [x][y][z] = density 
				if (x == 0 and y == 0 and z == 0):
					density = [[[0 for zR in range(self.__size[2])] for yR in range(self.__size[1])] for xR in range(self.__size[0])]
# 3 densitys in one row ... z is increasing fastest y medium x slowest 
# for openDx file format read : http://apbs.wustl.edu/MediaWiki/index.php/OpenDX_scalar_data_format
# Remember x y and z are multipliers for transformmatrix to get to the middle of the continue box 
				densityRow = (re.split('\s', line))
				densityRow.pop()
				for i in range (len(densityRow)):
					if (densityRow[i] == '' ):
						densityRow.pop()
						continue
					if float(densityRow[i]) < 0:
						densityRow[i] = 0
				if (z >= self.__size[2]):
					z = 0
					y += 1
				if (y >= self.__size[1]):
					y = 0
					x += 1
				if (x >= self.__size[0]):
					x = 0
				density[x][y][z] = float(densityRow[0])
				z += 1
				
				if (x >= self.__size[0] -1 and y >= self.__size[1] - 1 and z >= self.__size[2] -1):
					break
				if (z >= self.__size[2]):
					z = 0
					y += 1
				if (y >= self.__size[1]):
					y = 0
					x += 1
				if (x >= self.__size[0]):
					x = 0
				density[x][y][z] = float(densityRow[1])
				z += 1
				
				if (x >= self.__size[0] -1 and y >= self.__size[1] - 1 and z >= self.__size[2] -1):
					break			
				if (z >= self.__size[2]):
					z = 0
					y += 1
				if (y >= self.__size[1]):
					y = 0
					x += 1
				if (x >= self.__size[0]):
					x = 0
				density[x][y][z] = float(densityRow[2])
				z += 1
				outputLine = int ((row*100)/(( (self.__size[0] *self.__size[1]*self.__size[2])/3) ))
				print str(outputLine)+" %\b\b\b\b\b",
				row += 1
		dxFH.close()
		self.__density = density
		print "Done"
	def getOrigin(self = None):			
		return self.__origin 
	def getSize(self=None):
		tmp = int(int(self.__size[0])* int(self.__size[1])*int(self.__size[2]))
		return tmp
	def getDimention(self=None):
		return self.__size
	def getStepsize(self=None):
		return float(self.__stepSize)
	def getDensity(self=None):
		return self.__density
				
	def setDxfile(self,dxFile):
		if (not dxFile):
			print "Error no intputfile"
			exit 	
		self.__dxFile = dxFile
		self.__converted = ()
		self.__origin =()
		self.__transformMatrix = []
		self.__size = ()	
	def getFilename(self):
		return self.__dxFile
	def getDxObject(self=None):
		object = BuildOpenDx (self.__density, float(self.__stepSize), self.__origin,self.__size)
		return object
