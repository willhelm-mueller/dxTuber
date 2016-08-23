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

#####
# v0.15 
# +setDensity
#
#since v0.065 dimention is a new mandatory parameter! 
#####
class BuildOpenDx():
#density array [x][y][z] = density as float [dx format]
	__density=[] 
#origin array [0] = x, [1] =y, [2] = z   as float
	__origin =[]
	__stepSize = ()
#dimention array [0] = x, [1] =y, [2] = z   as integer
	__dimention = []
	def __init__ (self, density, stepSize, origin,dimention):
		self.__density = density
		self.__stepSize = stepSize
		self.__origin = origin
		self.__dimention = dimention
		
	def getOrigin(self = None):			
		return self.__origin 
	def getDensity(self=None):
		return self.__density
	def setDensity(self, density):
		self.__density = density
		
	def getStepsize(self=None):
		return self.__stepSize
	def getDimention(self=None):
		return self.__dimention
