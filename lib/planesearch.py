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
#####
# 
#
# v0.2 
# - __storeOverLappingISV = False    <--- switches if ISV will be deleted if a protein Voxels > protMinDens is located at the very same position 
#
#
# v0.15
# +new method "
# -minSolventDens(default)= 0 now  
#
# v.0.091
# +support solvent files smaller than protein files
#
# v.0.08
# +user adjustable solvent density


class PlaneSearch():
	__densityWater = []
	__densityProtein = []
	__stepSize = ()
	__tube = []
	__dxObjectWater =()
	__dxObjectProtein =()
	__minDiameter = () 
	__minProteinDensity =()
	__secondDensities= False
### Trigger that switches between old mode ( deleting ISV overlapping with protein Voxels) and new mode (ignore overlap)	
	__storeOverLappingISV = False
	
	def __init__(self, dxObjectWater, dxObjectProtein, minDiameter="0",minProteinDens = "0.005",minSolventDens = "0.00", mdk = False, storeOverLappingISV = False):
		self.__minProteinDensity = float(minProteinDens)
		self.__densityWater = dxObjectWater.getDensity()
		self.__stepSize = dxObjectWater.getStepsize()
		self.__minDiameter = int (float(minDiameter) / float(self.__stepSize))
		print 'Protein Threshold = ' + minProteinDens+'\nSolvent Threshold = ' + minSolventDens
		print 'minDiameter: '+ str(minDiameter)+ ' Angstrom \nVolmap Stepsize: '+str(self.__stepSize)+ '\nResulting minimum voxel minDiameter: ' +str(self.__minDiameter)
#		self.__minDiameter = minDiameter
#implementing solvent user adjustable
		self.__minSolventDens= float(minSolventDens)
		self.__densityProtein = dxObjectProtein.getDensity()
		self.__dxObjectWater = dxObjectWater
		self.__dxObjectProtein = dxObjectProtein
		self.__tube = [[[0 for zR in range(len (self.__densityWater[0][0]))] for yR in range(len (self.__densityWater[0]))] for xR in range(len (self.__densityWater))]
		self.__mdk = mdk
		self.__storeOverLappingISV = storeOverLappingISV
# plane must be 'x' 'y' or 'z'
	def oneDimension(self, plane):
		proteinOrigin = self.__dxObjectProtein.getOrigin()
#stepsize multiplier need to be implemented if stepsize !=1
		stepMultiplier = 1 / self.__stepSize 		
		waterOrigin = self.__dxObjectWater.getOrigin()
		waterToProteinOrigin = (int ((proteinOrigin[0] - waterOrigin[0])*stepMultiplier),int ((proteinOrigin[1] - waterOrigin[1])*stepMultiplier),int ((proteinOrigin[2] - waterOrigin[2])*stepMultiplier))
		print 'Scanning '+ plane +' plane minimum diameter is set to: '+ str (self.__minDiameter)+ ' voxels'
		row = ()
		if (plane == 'z'):
			for  xCount in range (len (self.__densityProtein)):
				for  yCount in range (len (self.__densityProtein[0])):
					row =[]
					for zCount in range (len (self.__densityProtein[0][0])):
						row.append (self.__densityProtein[xCount][yCount][zCount])
					for i in range (len(row)):
						if (self.__densityProtein[xCount][yCount][i] > self.__minProteinDensity and not self.__storeOverLappingISV ):
							continue
						convertPosition = (xCount+waterToProteinOrigin[0], yCount+waterToProteinOrigin[1],i+waterToProteinOrigin[2])
						try:
							self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] 
						except IndexError:
							continue 						
## implementing solvent variables:
						if (self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] < self.__minSolventDens):
#						if (self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] < 0.01):
							continue
						proteinLeft = 0
						proteinRight = 0
						
						j= i

						while (j > 0):
							j -=1
							if (self.__densityProtein[xCount][yCount][j] >=  self.__minProteinDensity):
								proteinLeft = i - j	
								break

						for k in range (i,len (row)):
							 if (self.__densityProtein[xCount][yCount][k] >= self.__minProteinDensity ):
								proteinRight =k-i
								break 
						borderSum = proteinLeft+proteinRight
#						print 'borderSum: ' + str(borderSum)
						if (proteinLeft > 0 and proteinRight > 0 and borderSum > self.__minDiameter ):
							self.__tube[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
			

		if (plane == 'y'):
			for  xCount in range (len (self.__densityProtein)):
				for  zCount in range (len (self.__densityProtein[0][0])):
					row =[]
					for yCount in range (len (self.__densityProtein[0])):
						row.append (self.__densityProtein[xCount][yCount][zCount])
					for i in range (len(row)):
						if (self.__densityProtein[xCount][i][zCount] >  self.__minProteinDensity  and not self.__storeOverLappingISV):
							continue
						convertPosition = (xCount+waterToProteinOrigin[0], i+waterToProteinOrigin[1],zCount+waterToProteinOrigin[2])
						try:
							self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] 
						except IndexError:
							continue 						
## implementing solvent variables:
						if (self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] < self.__minSolventDens):						
#						if (self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] < 0.01):
							continue						
#						testing if water lies inside the protein
						proteinLeft = 0
						proteinRight = 0
						j= i
						while (j > 0):
							j -=1
							if (self.__densityProtein[xCount][j][zCount] >= self.__minProteinDensity ):
								proteinLeft = i - j	
								break
								
						for k in range (i,len (row)):
							 if (self.__densityProtein[xCount][k][zCount] >= self.__minProteinDensity ):
								proteinRight = k - i
								break 
						borderSum = proteinLeft+proteinRight
						if (proteinLeft > 0 and proteinRight > 0 and borderSum > self.__minDiameter ):
							self.__tube[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]

		if (plane == 'x'):
			for  yCount in range (len (self.__densityProtein[0])):
				for  zCount in range (len (self.__densityProtein[0][0])):
					row =[]
					for xCount in range (len (self.__densityProtein)):
						row.append (self.__densityProtein[xCount][yCount][zCount])
					for i in range (len(row)):
						if (self.__densityProtein[i][yCount][zCount] > self.__minProteinDensity  and not self.__storeOverLappingISV):
							continue
						convertPosition = (i+waterToProteinOrigin[0], yCount+waterToProteinOrigin[1],zCount+waterToProteinOrigin[2])
						try:
							self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] 
						except IndexError:
							continue 						
## implementing solvent variables:
						if (self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] < self.__minSolventDens):						
#						if (self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] < 0.01):
							continue						
#						testing if water lies inside the protein
						proteinLeft = 0
						proteinRight = 0
						j= i
						while (j > 0):
							j -=1
							if (self.__densityProtein[j][yCount][zCount] >=  self.__minProteinDensity ):
								proteinLeft = i - j						
								break
								
						for k in range (i,len (row)):
							 if (self.__densityProtein[k][yCount][zCount] >=  self.__minProteinDensity ):
								proteinRight = k-i
								break 
						borderSum = proteinLeft+proteinRight
						if (proteinLeft > 0  and proteinRight > 0 and borderSum > self.__minDiameter):
							self.__tube[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
		print "Done"
		
	def twoDimension(self = None):
		print "Scanning 2D"
		proteinOrigin = self.__dxObjectProtein.getOrigin()
		waterOrigin = self.__dxObjectWater.getOrigin()
#stepsize multiplier need to be implemented if stepsize !=1
		stepMultiplier = 1 / self.__stepSize 
		waterToProteinOrigin = (int ((proteinOrigin[0] - waterOrigin[0])*stepMultiplier),int ((proteinOrigin[1] - waterOrigin[1])*stepMultiplier),int ((proteinOrigin[2] - waterOrigin[2])*stepMultiplier))
		for  xCount in range (len (self.__densityProtein)):
			for  yCount in range (len (self.__densityProtein[0])):
				for zCount in range (len (self.__densityProtein[0][0])):

					convertPosition = (xCount+waterToProteinOrigin[0], yCount+waterToProteinOrigin[1],zCount+waterToProteinOrigin[2])
					try:
						self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] 
					except IndexError:
						continue 					
					if (self.__densityProtein[xCount][yCount][zCount] > self.__minProteinDensity  and not self.__storeOverLappingISV):
						continue
					xProteinLeft = 0
					xProteinRight = 0					
					j = xCount	
					while (j > 0):
						j -=1
						if (self.__densityProtein[j][yCount][zCount] >=  self.__minProteinDensity):
							xProteinLeft = xCount - j						
							break
							
					for k in range (xCount+1,len(self.__densityProtein)):    #### xcount +1 !!! to test neighbours and not the voxel itself !!! 
						 if (self.__densityProtein[k][yCount][zCount] >=  self.__minProteinDensity  ):
							xProteinRight = k- xCount
							break 					
					xBorderSum = xProteinLeft+xProteinRight
					
					yProteinLeft = 0
					yProteinRight = 0		
					j = yCount
					while (j > 0):
						j -=1
						if (self.__densityProtein[xCount][j][zCount] >=  self.__minProteinDensity  ):
							yProteinLeft = yCount - j	
							break
							
					for k in range (yCount+1,len(self.__densityProtein[0])):
						 if (self.__densityProtein[xCount][k][zCount] >=  self.__minProteinDensity  ):
							yProteinRight = k - yCount
							break 
					yBorderSum = yProteinLeft+yProteinRight	
						
					zProteinLeft = 0
					zProteinRight = 0					
					j = zCount
					while (j > 0):
						j -=1
						if (self.__densityProtein[xCount][yCount][j] >=  self.__minProteinDensity  ):
							zProteinLeft = zCount - j	
							break

					for k in range (zCount+1,len(self.__densityProtein[0][0])):
						 if (self.__densityProtein[xCount][yCount][k] >=  self.__minProteinDensity  ):
							zProteinRight =k- zCount
							break 
					zBorderSum = zProteinLeft+zProteinRight				
					if (xProteinLeft > 0  and xProteinRight > 0 ):
						if (yProteinLeft > 0  and yProteinRight > 0):
							if (xBorderSum > self.__minDiameter and yBorderSum > self.__minDiameter and self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens):
#							if (xBorderSum > self.__minDiameter and yBorderSum > self.__minDiameter):
								self.__tube[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						if (zProteinLeft > 0  and zProteinRight > 0):	
							if (xBorderSum > self.__minDiameter and zBorderSum > self.__minDiameter and self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens):
								self.__tube[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]

					if (yProteinLeft > 0  and yProteinRight > 0 and zProteinLeft > 0  and zProteinRight > 0 ):
						if (yBorderSum > self.__minDiameter and zBorderSum > self.__minDiameter and self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens):
#						if (yBorderSum > self.__minDiameter and zBorderSum > self.__minDiameter):
							self.__tube[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
				outputLine = int ((xCount*100)/len(self.__densityProtein))
				print str(outputLine)+" %\b\b\b\b\b",
		print "Done"
##
##  This methods saves isv below a required minDiameter neighvborhood in a separate density file 
##  2 dxobjects will be created and can be procecced via grouping separatly 
##	
	def twoDimensionMinDiaArray(self = None):
		print "Scanning 2D \nKeeping ISV < " + str(self.__minDiameter)+ " Angstrom"
		proteinOrigin = self.__dxObjectProtein.getOrigin()
		waterOrigin = self.__dxObjectWater.getOrigin()
		
		belowMinDiameterArray = [[[0 for zR in range(len (self.__densityWater[0][0]))] for yR in range(len (self.__densityWater[0]))] for xR in range(len (self.__densityWater))]
#stepsize multiplier need to be implemented if stepsize !=1
		stepMultiplier = 1 / self.__stepSize 
		waterToProteinOrigin = (int ((proteinOrigin[0] - waterOrigin[0])*stepMultiplier),int ((proteinOrigin[1] - waterOrigin[1])*stepMultiplier),int ((proteinOrigin[2] - waterOrigin[2])*stepMultiplier))
		for  xCount in range (len (self.__densityProtein)):
			for  yCount in range (len (self.__densityProtein[0])):
				for zCount in range (len (self.__densityProtein[0][0])):

					convertPosition = (xCount+waterToProteinOrigin[0], yCount+waterToProteinOrigin[1],zCount+waterToProteinOrigin[2])
					try:
						self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] 
					except IndexError:
						continue 					
					if (self.__densityProtein[xCount][yCount][zCount] > self.__minProteinDensity  and not self.__storeOverLappingISV):
						continue
					xProteinLeft = 0
					xProteinRight = 0					
					j = xCount	
					while (j > 0):
						j -=1
						if (self.__densityProtein[j][yCount][zCount] >=  self.__minProteinDensity):
							xProteinLeft = xCount - j						
							break
							
					for k in range (xCount+1,len(self.__densityProtein)):
						 if (self.__densityProtein[k][yCount][zCount] >=  self.__minProteinDensity  ):
							xProteinRight = k- xCount
							break 					
					xBorderSum = xProteinLeft+xProteinRight
					
					yProteinLeft = 0
					yProteinRight = 0		
					j = yCount
					while (j > 0):
						j -=1
						if (self.__densityProtein[xCount][j][zCount] >=  self.__minProteinDensity  ):
							yProteinLeft = yCount - j	
							break
							
					for k in range (yCount+1,len(self.__densityProtein[0])):
						 if (self.__densityProtein[xCount][k][zCount] >=  self.__minProteinDensity  ):
							yProteinRight = k - yCount
							break 
					yBorderSum = yProteinLeft+yProteinRight	
						
					zProteinLeft = 0
					zProteinRight = 0					
					j = zCount
					while (j > 0):
						j -=1
						if (self.__densityProtein[xCount][yCount][j] >=  self.__minProteinDensity  ):
							zProteinLeft = zCount - j	
							break

					for k in range (zCount+1,len(self.__densityProtein[0][0])):
						 if (self.__densityProtein[xCount][yCount][k] >=  self.__minProteinDensity  ):
							zProteinRight =k- zCount
							break 
					zBorderSum = zProteinLeft+zProteinRight	
							
					if (xProteinLeft > 0  and xProteinRight > 0  and yProteinLeft > 0  and yProteinRight > 0):
						if (xBorderSum >= self.__minDiameter and yBorderSum >= self.__minDiameter and self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens):
							self.__tube[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
#
# keeping isv below required diameter  in a separete Array 
# v0.2
						elif self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens:
							belowMinDiameterArray[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
#############################################								
					if (xProteinLeft > 0  and xProteinRight > 0 and zProteinLeft > 0  and zProteinRight > 0):	
						if (xBorderSum >= self.__minDiameter and zBorderSum >= self.__minDiameter and self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens):
							self.__tube[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						elif self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens:
							belowMinDiameterArray[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]

					if (yProteinLeft > 0  and yProteinRight > 0 and zProteinLeft > 0  and zProteinRight > 0 ):
						if (yBorderSum >= self.__minDiameter and zBorderSum >= self.__minDiameter and self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens):
							self.__tube[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						elif self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens:
							belowMinDiameterArray[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
				
				
###
# mdk block 
###							
#					if (xProteinLeft > 0  and xProteinRight > 0) and (yProteinLeft > 0  and yProteinRight > 0):
#						if ((xBorderSum <= self.__minDiameter or yBorderSum <= self.__minDiameter)#  or (xBorderSum < self.__minDiameter or yBorderSum <= self.__minDiameter)
#						and self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens):
#							belowMinDiameterArray[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
#							
##					if (xProteinLeft > 0  and xProteinRight > 0) and (zProteinLeft > 0  and zProteinRight > 0):
#						if ((xBorderSum <= self.__minDiameter or zBorderSum <= self.__minDiameter) #or (xBorderSum < self.__minDiameter or zBorderSum <= self.__minDiameter) 
#						
#						and self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens):
#							belowMinDiameterArray[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[c#onvertPosition[0]][convertPosition[1]][convertPosition[2]]
#
#					if (yProteinLeft > 0  and yProteinRight > 0) and (zProteinLeft > 0  and zProteinRight > 0):
#						if ((yBorderSum <= self.__minDiameter or zBorderSum <= self.__minDiameter)# or  (yBorderSum < self.__minDiameter or zBorderSum <= self.__minDiameter) 
#						and self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens):
#							belowMinDiameterArray[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
							
				outputLine = int ((xCount*100)/len(self.__densityProtein))
				print str(outputLine)+" %\b\b\b\b\b",
		self.__secondDensities = belowMinDiameterArray
		print "Done"		
		
		
											
	def threeDimension(self = None):
		print "Scanning 3D"
#stepsize multiplier need to be implemented if stepsize !=1
		stepMultiplier = 1 / self.__stepSize 	
		proteinOrigin = self.__dxObjectProtein.getOrigin()
		waterOrigin = self.__dxObjectWater.getOrigin()
		
		if self.__mdk:
			belowMinDiameterArray = [[[0 for zR in range(len (self.__densityWater[0][0]))] for yR in range(len (self.__densityWater[0]))] for xR in range(len (self.__densityWater))]
		
		waterToProteinOrigin = (int ((proteinOrigin[0] - waterOrigin[0])*stepMultiplier),int ((proteinOrigin[1] - waterOrigin[1])*stepMultiplier),int ((proteinOrigin[2] - waterOrigin[2])*stepMultiplier))
		for  xCount in range (len (self.__densityProtein)):
			for  yCount in range (len (self.__densityProtein[0])):
				for zCount in range (len (self.__densityProtein[0][0])):
					convertPosition = (xCount+waterToProteinOrigin[0], yCount+waterToProteinOrigin[1],zCount+waterToProteinOrigin[2])
					try:
						self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] 
					except IndexError:
						continue
						
					if (self.__densityProtein[xCount][yCount][zCount] > self.__minProteinDensity  and not self.__storeOverLappingISV):
						continue 
					xProteinLeft = 0
					xProteinRight = 0					
					j = xCount	
					while (j > 0):
						j -=1
						if (self.__densityProtein[j][yCount][zCount] >=  self.__minProteinDensity):
							xProteinLeft = xCount - j						
							break
							
					for k in range (xCount+1,len(self.__densityProtein)):
						 if (self.__densityProtein[k][yCount][zCount] >=  self.__minProteinDensity  ):
							xProteinRight = k- xCount
							break 					
					xBorderSum = xProteinLeft+xProteinRight
					
					yProteinLeft = 0
					yProteinRight = 0		
					j = yCount
					while (j > 0):
						j -=1
						if (self.__densityProtein[xCount][j][zCount] >=  self.__minProteinDensity  ):
							yProteinLeft = yCount - j	
							break
							
					for k in range (yCount+1,len(self.__densityProtein[0])):
						 if (self.__densityProtein[xCount][k][zCount] >=  self.__minProteinDensity  ):
							yProteinRight = k - yCount
							break 
					yBorderSum = yProteinLeft+yProteinRight	
						
					zProteinLeft = 0
					zProteinRight = 0					
					j = zCount
					while (j > 0):
						j -=1
						if (self.__densityProtein[xCount][yCount][j] >=  self.__minProteinDensity  ):
							zProteinLeft = zCount - j	
							break

					for k in range (zCount+1,len(self.__densityProtein[0][0])):
						 if (self.__densityProtein[xCount][yCount][k] >=  self.__minProteinDensity  ):
							zProteinRight =k- zCount
							break 
					zBorderSum = zProteinLeft+zProteinRight				
					if (xProteinLeft > 0  and xProteinRight > 0 and yProteinLeft > 0  and yProteinRight > 0 and zProteinLeft > 0  and zProteinRight > 0 ):
						if (xBorderSum >= self.__minDiameter and yBorderSum >= self.__minDiameter and zBorderSum >= self.__minDiameter and self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens):
#						if (xBorderSum > self.__minDiameter and xBorderSum > self.__minDiameter and zBorderSum > self.__minDiameter):
							self.__tube[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
						elif self.__mdk:
							if self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]] > self.__minSolventDens:
								belowMinDiameterArray[convertPosition[0]][convertPosition[1]][convertPosition[2]] = self.__densityWater[convertPosition[0]][convertPosition[1]][convertPosition[2]]
				outputLine = int ((xCount*100)/len(self.__densityProtein))
				print str(outputLine)+" %\b\b\b\b\b",
				
		if self.__mdk:
			self.__secondDensities = belowMinDiameterArray
		print "Done"	
	def getDxObject(self=None):
		object = BuildOpenDx (self.__tube, self.__dxObjectWater.getStepsize(), self.__dxObjectWater.getOrigin(),self.__dxObjectWater.getDimention())
		return object
	def getDxObjectArray(self=None):
		object1 = BuildOpenDx (self.__tube, self.__dxObjectWater.getStepsize(), self.__dxObjectWater.getOrigin(),self.__dxObjectWater.getDimention())
		object2 = BuildOpenDx (self.__secondDensities, self.__dxObjectWater.getStepsize(), self.__dxObjectWater.getOrigin(),self.__dxObjectWater.getDimention())
		object = [object1,object2]
		return object
	
