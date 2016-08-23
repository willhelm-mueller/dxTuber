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

class WriteDx():
	__dxObject = ()
	def __init__(self, dxObject):
		self.__dxObject = dxObject
	def write(self,filename):
		dxFH = open(filename,"w")
		density = self.__dxObject.getDensity()
		origin = self.__dxObject.getOrigin()
		atomCount = len (density)*len (density[0])*len (density[0][0])
		triple = ()
		dxFH.write ("# Created via dxTuber\n")
		dxFH.write ("object 1 class gridpositions counts %i %i %i\n" %(len (density),len (density[0]),len (density[0][0])))
		dxFH.write ("origin %.1f %.1f %.1f\n" %(origin[0],origin[1],origin[2]))
#writing transformation matrx
		dxFH.write ("delta %s 0 0\n" %(self.__dxObject.getStepsize()) )
		dxFH.write ("delta 0 %s 0\n" %(self.__dxObject.getStepsize()) )
		dxFH.write ("delta 0 0 %s\n" %(self.__dxObject.getStepsize()) )
		dxFH.write ("object 2 class gridconnections counts %i %i %i\n" %(len (density),len (density[0]),len (density[0][0])))
		dxFH.write ("object 3 class array type double rank 0 items %i data follows\n" %(atomCount))

#header complete
		triple= []
		for  xCount in range (len (density)):
			for  yCount in range (len (density[0])):
				for zCount in range (len (density[0][0])):
					triple.append (density[xCount][yCount][zCount])
					if (len (triple) == 3):
						for i in range (len (triple)):
							if i < 2:
								if (triple[i] == 0):
									dxFH.write ("0 ")
								else:
									dxFH.write ("%e " %(triple[i]))
							else:
								if (triple[i] == 0):
									dxFH.write ("0")
								else:
									dxFH.write ("%e" %(triple[i]))								
						dxFH.write ("\n")
						triple = []
	
#if one entry missing 
		if (len (triple)  == 1 ):
			if (triple[0] == 0):
				dxFH.write ("0")
			else:
				dxFH.write ("%e" %(triple[0]))
			dxFH.write ("\n")
	
#if 2 entries missing			
		if (len (triple)  == 2 ):
			if (triple[0] == 0):
				dxFH.write ("0 ")
			else:
				dxFH.write ("%e " %(triple[0]))
			if (triple[1] == 0):
				dxFH.write ("0")
			else:
				dxFH.write ("%e" %(triple[1]))				
			dxFH.write ("\n")	
				
				
		dxFH.write ("\nobject \"density (protein) [A^-3]\" class field")			
		dxFH.close ()	
		print "Saved OpenDX in "+str(filename)
		
