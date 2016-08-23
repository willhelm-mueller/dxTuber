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
###
#
# v0.2
# -ungrouped cavites have group id '0' instead of 'DEN' -> analyzeCavity.py can process ungrouped cavities now
# +writeMultiGroupeArray  (implemented  for mdk (minimum distance keep))
# -groupe id's are not printed anymore to cmd // stop spamming 
# -densities > 99 are now supported // densities  > 99 6.2f    > 999 6.1f     > 9999 6.0f      > 999999 strange things could will happen :>
#
# v0.09
#
# +Grouped Yes / No  field in header
# +saved as <filename>
#
# v0.085
# +'cryst' entry to enable pbc in molecular viewer
#
# v0.082
# +dxTuber settings are saved in pdb files
#
# v0.08
# +user defined solvent min densities are filtered already during scanningmethod ! 
#  
#
##
class WritePDB ():
	__density=[] 
	__origin =[]
	__stepSize = ()
	__origin = ()
	__dimention = []
	def __init__(self, tubeDx):
		dxObject = tubeDx.getDxObject()
		self.__density = dxObject.getDensity()
		self.__stepSize = dxObject.getStepsize()
		self.__origin = dxObject.getOrigin()
		self.__tubeDx = tubeDx
	def write (self, filename):
		i=0
		pdbFH = open(filename,"w")
		atomCount = 1
#begin dxTuber parameter section

		pdbFH.write("dxTuber\tVersion\t\t"+self.__tubeDx.getVersion()+"\n")
		pdbFH.write("dxTuber\tOpenDXFile\t"+self.__tubeDx.getFilename()+"\n")
		pdbFH.write("dxTuber\tProteinFile\t"+self.__tubeDx.getProtFile()+"\n")
		pdbFH.write("dxTuber\tSolventFile\t"+self.__tubeDx.getSolvFile()+"\n")
		pdbFH.write("dxTuber\tStepSize\t"+str(self.__tubeDx.getDxObject().getStepsize())+"\n")
		pdbFH.write("dxTuber\tScanType\t"+self.__tubeDx.getScanned()+"\n")
		pdbFH.write("dxTuber\tMinDiameter\t"+self.__tubeDx.getMinDiameter()+"\n")
		pdbFH.write("dxTuber\tMinProtDens\t"+str(self.__tubeDx.getProtThreshold())+"\n")
		pdbFH.write("dxTuber\tMinSolvDens\t"+str(self.__tubeDx.getSolventThreshold())+"\n")
		pdbFH.write("dxTuber\tFilter\t\t"+self.__tubeDx.getFilterApplied()+"\n")
		pdbFH.write("dxTuber\tGrouped\t\tNo\n")
#CRYST1   98.959   98.084  186.817  90.00  90.00  90.00 P 1           1		
		pdbFH.write ("CRYST1%9.3f%9.3f%9.3f  90.00  90.00  90.00 P 1           1\n" %(len (self.__density),len (self.__density[0]),len (self.__density[0][0])))
		pdbFH.write("\n")			
		
		for  xCount in range (len (self.__density)):
			for  yCount in range (len (self.__density[0])):
				for zCount in range (len (self.__density[0][0])):
#For visual representation we considered only voxels exceeding a cutoff density 
#of 0.015 H2O/A3, which is ~50% of the value for bulk water under standard conditions
#http://www.pubmedcentral.nih.gov/articlerender.fcgi?tool=pubmed&pubmedid=14747309
#
#Dynamics of Water Molecules in the Bacteriorhodopsin Trimer in Explicit Lipid/Water Environment
#Christian Kandt, Juergen Schlitter, and Klaus Gerwert
#so here cutoff 0.01 H_2O was choosen
# not nessaccary here, user can define this via gui / cmd and is done by planesearch !!
					if (self.__density[xCount][yCount][zCount] > 0):
						x = float (xCount) * float(self.__stepSize) + float(self.__origin[0])
						y = float (yCount) * float(self.__stepSize) + float(self.__origin[1])
						z = float (zCount) * float(self.__stepSize) + float(self.__origin[2])
						if (atomCount > 99999):
							atomCount = 1
#						pdbFH.write ("ATOM  %5i  DEN DEN H   1    %8.3f%8.3f%8.3f  1.00%6.3f           D\n" %( atomCount,x, y, z, self.__density[xCount][yCount][zCount]) )
						if self.__density[xCount][yCount][zCount] < 100:
							pdbFH.write ("ATOM  %5i    0 DEN H   1    %8.3f%8.3f%8.3f  1.00%6.3f           D\n" %( atomCount,x, y, z, self.__density[xCount][yCount][zCount]) )
						elif self.__density[xCount][yCount][zCount] < 1000:
							pdbFH.write ("ATOM  %5i    0 DEN H   1    %8.3f%8.3f%8.3f  1.00%6.2f           D\n" %( atomCount,x, y, z, self.__density[xCount][yCount][zCount]) )
						elif self.__density[xCount][yCount][zCount] < 10000:
							pdbFH.write ("ATOM  %5i    0 DEN H   1    %8.3f%8.3f%8.3f  1.00%6.1f           D\n" %( atomCount,x, y, z, self.__density[xCount][yCount][zCount]) )
						else:
							pdbFH.write ("ATOM  %5i    0 DEN H   1    %8.3f%8.3f%8.3f  1.00%6.0f           D\n" %( atomCount,x, y, z, self.__density[xCount][yCount][zCount]) )
						atomCount += 1
		pdbFH.write("TER\n") 
		pdbFH.write("END\n") 	

		pdbFH.close()
		print "saved "+filename
		
## group array  
#groupes
#[[x][y][z][x][y][z]]		
	def writeGroups(self, groupArray, filename):
		atomCount = 1
		chain =0
		maxChain = len (groupArray)
		pdbFH = open(filename, "w")
		
		pdbFH.write("dxTuber\tVersion\t\t"+self.__tubeDx.getVersion()+"\n")
		pdbFH.write("dxTuber\tOpenDXFile\t"+self.__tubeDx.getFilename()+"\n")
		pdbFH.write("dxTuber\tProteinFile\t"+self.__tubeDx.getProtFile()+"\n")
		pdbFH.write("dxTuber\tSolventFile\t"+self.__tubeDx.getSolvFile()+"\n")
		pdbFH.write("dxTuber\tStepSize\t"+str(self.__tubeDx.getDxObject().getStepsize())+"\n")
		pdbFH.write("dxTuber\tScanType\t"+self.__tubeDx.getScanned()+"\n")
		pdbFH.write("dxTuber\tMinDiameter\t"+self.__tubeDx.getMinDiameter()+"\n")
		pdbFH.write("dxTuber\tMinProtDens\t"+str(self.__tubeDx.getProtThreshold())+"\n")
		pdbFH.write("dxTuber\tMinSolvDens\t"+str(self.__tubeDx.getSolventThreshold())+"\n")
		pdbFH.write("dxTuber\tFilter\t\t"+self.__tubeDx.getFilterApplied()+"\n")
		pdbFH.write("dxTuber\tGrouped\t\tYes\n")
#CRYST1   98.959   98.084  186.817  90.00  90.00  90.00 P 1           1		
		pdbFH.write ("CRYST1%9.3f%9.3f%9.3f  90.00  90.00  90.00 P 1           1\n" %(len (self.__density),len (self.__density[0]),len (self.__density[0][0])))
		
		pdbFH.write("\n")
		
		
		while (chain < maxChain):
#			print chain  #// stop spamming ... ;)
			for mCounter in range (len (groupArray[chain])):
				if (atomCount > 99999):
					atomCount = 1
				try:
					x = float (float(groupArray[chain][mCounter][0]) * float(self.__stepSize)) + float(self.__origin[0])
					y = float (float(groupArray[chain][mCounter][1]) * float(self.__stepSize)) + float(self.__origin[1])
					z = float (float(groupArray[chain][mCounter][2]) * float(self.__stepSize)) + float(self.__origin[2])
### scaling output format for densities ... 
# v0.2	densities up to 999999 are now supported ...				
					if self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]] < 100:
						pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.3f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]]) )
					elif self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]] < 1000:	
						pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.2f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]]) )
					elif self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]] < 10000:	
						pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.1f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]]) )
					else:
						pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.0f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]]) )
						
				except TypeError:
					x = float (float(groupArray[chain][0]) * float(self.__stepSize)) + float(self.__origin[0])
					y = float (float(groupArray[chain][1]) * float(self.__stepSize)) + float(self.__origin[1])
					z = float (float(groupArray[chain][2]) * float(self.__stepSize)) + float(self.__origin[2])
					
					if self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]] < 100:
						pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.3f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]]) )
					elif self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]] < 1000:
						pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.2f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]]) )
					elif self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]] < 10000:
						pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.1f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]]) )
					else:
						pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.0f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]]) )

				atomCount += 1
			chain += 1
		pdbFH.write("TER\n") 
		pdbFH.write("END\n") 

		pdbFH.close
		print "saved "+filename
## MultiGroupArray contains arrays of groups // [0] array one [1]array two .... 
# 
# Multiple groups may contain 
# [0] groups of isv that fullfill a mindiameter threshold
# [1] groups of isv that do not fullfill a mindiameter threshold
# 
##   member    member          
# { [[x][y][z][x][y][z]]   } {   [[x][y][z][x][y][z]]   } 
#      G R O U P          Array
#
	def writeMultiGroups(self, multiGroupArray, filename):
		print "Saving multiple Groups" 
		atomCount = 1
		chain =0        #### GROAAAR this row took 1 week of bug fixing/searching  m( 
		pdbFH = open(filename, "w")
		
		pdbFH.write("dxTuber\tVersion\t\t"+self.__tubeDx.getVersion()+"\n")
		pdbFH.write("dxTuber\tOpenDXFile\t"+self.__tubeDx.getFilename()+"\n")
		pdbFH.write("dxTuber\tProteinFile\t"+self.__tubeDx.getProtFile()+"\n")
		pdbFH.write("dxTuber\tSolventFile\t"+self.__tubeDx.getSolvFile()+"\n")
		pdbFH.write("dxTuber\tStepSize\t"+str(self.__tubeDx.getDxObject().getStepsize())+"\n")
		pdbFH.write("dxTuber\tScanType\t"+self.__tubeDx.getScanned()+"\n")
		pdbFH.write("dxTuber\tMinDiameter\t"+self.__tubeDx.getMinDiameter()+"\n")
		pdbFH.write("dxTuber\tMinProtDens\t"+str(self.__tubeDx.getProtThreshold())+"\n")
		pdbFH.write("dxTuber\tMinSolvDens\t"+str(self.__tubeDx.getSolventThreshold())+"\n")
		pdbFH.write("dxTuber\tFilter\t\t"+self.__tubeDx.getFilterApplied()+"\n")
		pdbFH.write("dxTuber\tGrouped\t\tYes\n")
#CRYST1   98.959   98.084  186.817  90.00  90.00  90.00 P 1           1		
		pdbFH.write ("CRYST1%9.3f%9.3f%9.3f  90.00  90.00  90.00 P 1           1\n" %(len (self.__density),len (self.__density[0]),len (self.__density[0][0])))
		
		pdbFH.write("\n")
		
		for groupArray in multiGroupArray:
			chain =0
			print str(len(multiGroupArray))+" len multiGroupArray"
			maxChain = len(groupArray) 
			while (chain < maxChain):
#				print chain       #// stop spamming ... ;)
				for mCounter in range (len (groupArray[chain])):
					if (atomCount > 99999):
						atomCount = 1
					try:
						x = float (float(groupArray[chain][mCounter][0]) * float(self.__stepSize)) + float(self.__origin[0])
						y = float (float(groupArray[chain][mCounter][1]) * float(self.__stepSize)) + float(self.__origin[1])
						z = float (float(groupArray[chain][mCounter][2]) * float(self.__stepSize)) + float(self.__origin[2])

						if self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]] < 100:
							pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.3f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]]) )
						elif self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]] < 1000:	
							pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.2f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]]) )
						elif self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]] < 10000:	
							pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.1f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]]) )
						else:
							pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.0f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][mCounter][0]][groupArray[chain][mCounter][1]][groupArray[chain][mCounter][2]]) )
							
	
					except TypeError:
						x = float (float(groupArray[chain][0]) * float(self.__stepSize)) + float(self.__origin[0])
						y = float (float(groupArray[chain][1]) * float(self.__stepSize)) + float(self.__origin[1])
						z = float (float(groupArray[chain][2]) * float(self.__stepSize)) + float(self.__origin[2])
					
						if self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]] < 100:
							pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.3f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]]) )
						elif self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]] < 1000:
							pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.2f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]]) )
						elif self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]] < 10000:
							pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.1f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]]) )
						else:
							pdbFH.write ("ATOM  %5i %4i DEN a   1    %8.3f%8.3f%8.3f  1.00%6.0f           D\n" %( atomCount,chain,x, y, z, self.__density[groupArray[chain][0]][groupArray[chain][1]][groupArray[chain][2]]) )

					atomCount += 1
### chain should not be bigger than 99999 ... ehm shall be handeld in following versions .... *hust hust*				
				chain += 1
		pdbFH.write("TER\n") 
		pdbFH.write("END\n") 

		pdbFH.close
		print "saved "+filename
