#!/usr/bin/env python
#
#	 This file is part of the dxTuber package
#    dxTuber v0.27  7. Jan 2013
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
####################################################################################
### This tool s written to detect cavities based on protein and solvent movement ###
###																				 ###
###																				 ###
### 1. flood your system with water (by using GROMACS)							 ###
###	2. Open your molecule in VMD												 ###
### 3. save 2 OpenDX (only solvent and only protein) files via VMD -> VolMap 	 ###
### 4. start this script  													     ###
###																			  	 ###
###	Contact: raunest@bit.uni-bonn.de or m.raunest@gmx.de   Martin Raunest		 ###
###																				 ###
####################################################################################


import sys
import os
import re
#######################
# only within gnome nessasary KDE ?
#######################
import gnome.ui    
gnome.init("dxTuber", "version")
#######################
import pygtk
try:
	import gtk
	import gtk.glade
except:
	print "You need to install pyGTK or GTKv2 ",
	print "or set your PYTHONPATH correctly."
	print "try: export PYTHONPATH=",
	print "/usr/local/lib/python2.X/site-packages/"
	sys.exit(1)

from lib.readopendx import *
from lib.planesearch import *
from lib.writepdb import *
from lib.writedx import *
from lib.grouptubes import *
from lib.filterdx import *
from lib.analysetube import *
from lib.filltube import *
from lib.tubedx import *
from lib.readpdb import * 

class appgui:
	__dxTubeArray = []
	__proteinSelected = 0
	__waterSelected = 0
	__fileSelected = 0 
	__scanMethod = 2 
	__analyseAxis=0
	__analyseMethod = 0
	def toggleProteinCB(self,widget):
		list = widget.get_group()
		list.reverse()
		for button in range (len(list)):
			if (list[button].get_active()):
				self.__proteinSelected = button
				
	def toggleWaterCB(self,widget):
		list = widget.get_group()
		list.reverse()
		for button in range (len(list)):
			if (list[button].get_active()):
				self.__waterSelected = button

	def toggleFileCB(self,widget):
		list = widget.get_group()
		list.reverse()
		for button in range (len(list)):
			if (list[button].get_active()):
				self.__fileSelected = button
### Scan Methods
#1: 1D
#2: 2D
#3: 3D
###
	def toggleScan1D(self,widget):
		xButton = self.wTree.get_widget("search1DXCheckBox")
		yButton = self.wTree.get_widget("search1DYCheckBox")
		zButton = self.wTree.get_widget("search1DZCheckBox")
		
		xButton.set_sensitive(1)
		yButton.set_sensitive(1)
		zButton.set_sensitive(1)
		self.__scanMethod = 1 
	def toggleScan2D(self,widget):
		xButton = self.wTree.get_widget("search1DXCheckBox")
		yButton = self.wTree.get_widget("search1DYCheckBox")
		zButton = self.wTree.get_widget("search1DZCheckBox")
		
		xButton.set_sensitive(0)
		yButton.set_sensitive(0)
		zButton.set_sensitive(0)
		self.__scanMethod = 2 
	def toggleScan3D(self,widget):
		xButton = self.wTree.get_widget("search1DXCheckBox")
		yButton = self.wTree.get_widget("search1DYCheckBox")
		zButton = self.wTree.get_widget("search1DZCheckBox")
		
		xButton.set_sensitive(0)
		yButton.set_sensitive(0)
		zButton.set_sensitive(0)
		self.__scanMethod = 3 
	
	def toggleAnalyseAxisCB(self,widget):
		list = widget.get_group()
		list.reverse()
		for axis in range (len(list)):
			if (list[axis].get_active()):
				self.__analyseAxis = axis
	def toggleAnalyseMethodCB(self,widget):
		list = widget.get_group()
		list.reverse()
		for method in range (len(list)):
			if (list[method].get_active()):
				self.__analyseMethod = method					
				
	def __readSettings(self):
#		self.__version = '0.09'
#		self.__vDate = '17.Mar.2011'
		dxTuberConfFile = os.environ['HOME']+"/.dxTuber/dxTuber.conf"
		conf = open (dxTuberConfFile,'r')
		confLines = conf.readlines()
		for line in confLines:
			if re.match ('^#',line):
				continue
			if re.match('INSTALL_DIR',line):
				tmpArray = re.split('\s',line,1)
				tmp = re.sub('\"','',tmpArray[1])
				tmp = re.sub('\n','',tmp)
				self.instPath = re.sub('^\s','',tmp)
			if re.match('VERSION',line):
#				print line
				tmpArray = re.split('\s',line,1)
				tmp = re.sub('\"','',tmpArray[1])
				tmp = re.sub('\n','',tmp)
				self.__version = re.sub('^\s','',tmp)
		print "dxTuber v" + self.__version 
		
	def __init__(self):
		self.__readSettings()
		glade = self.instPath+"/dxTuber.libglade"
		self.wTree=gtk.glade.XML (fname=str(glade), domain="app1")
		self.__tableWidget = self.wTree.get_widget("newTable")
		scanButton = self.wTree.get_widget("scanButton")
		scanButton.connect("clicked", self.scanTube)
		
		dic = { "py_open_file" : self.openDx, 
				"OPEN_PDB" : self.openPDB,
				"FILE_CHOOSER_ACTION_SAVE": self.savePDB, 
				"SAVE_TO_DX" : self.saveDx, 
				"GROUPE_DX" : self.groupTube,
				"SCAN_1D_CLICKED" : self.toggleScan1D,
				"SCAN_2D_CLICKED" : self.toggleScan2D,
				"SCAN_3D_CLICKED" : self.toggleScan3D,
				"ANALYSE_TUBE_BUTTON_CLICKED" :self.startAnalysePopUp,
				"FILTER_TUBE_BUTTON_CLICKED": self.filterTube,
				}
		self.wTree.signal_autoconnect(dic)
	def filterTube(self,widget):
		filterNeighbourRadio = self.wTree.get_widget("filterNeighbourRadio")	
		filterDistanceSpinBox = self.wTree.get_widget("filterDistanceSpinBox")	
		filter = FilterDx (self.__dxTubeArray[self.__fileSelected].getDxObject(), filterDistanceSpinBox.get_value_as_int())
		if filterNeighbourRadio.get_active():
			filterSpinBox =  self.wTree.get_widget("filterNeighbourSpinbox")
			filterValue = filterSpinBox.get_value_as_int()
			filter.filterTunnelNeighbour(neighbourMin=filterValue)   #parameter of neighbours should be set in future
			filterName = 'Neighbor ' + str(filterSpinBox.get_value_as_int())
		else:
			filter.filterDistance()
			filterName = 'Distance '+ str(filterDistanceSpinBox.get_value_as_int())
			
		self.__dxTubeArray.append (TubeDx(filter.getDxObject(),filename="None",
									scanMethod = self.__dxTubeArray[self.__fileSelected].getScanMethod(), 
									scanned = self.__dxTubeArray[self.__fileSelected].getScanned(),
									solventThreshold = self.__dxTubeArray[self.__fileSelected].getSolventThreshold(), 
									protThreshold = self.__dxTubeArray[self.__fileSelected].getProtThreshold(),
									minDiameter = self.__dxTubeArray[self.__fileSelected].getMinDiameter(),
									protFile = self.__dxTubeArray[self.__fileSelected].getProtFile(),
									solvFile = self.__dxTubeArray[self.__fileSelected].getSolvFile(),
									version = self.__version,
									filterApplied = self.__dxTubeArray[self.__fileSelected].getFilterApplied()
									)
									)
		self.__dxTubeArray[(len(self.__dxTubeArray)-1)].setFilterApplied(filterName)
		print "Done"
		self.gtkDrawFileTable()
	def scanTube (self,widget = None):
		proteinDx = self.__dxTubeArray[self.__proteinSelected].getDxObject()
		waterDx = self.__dxTubeArray[self.__waterSelected].getDxObject()
		protThreshEntry = self.wTree.get_widget("proteinThresholdEntry")
###### implement solvent densities and min diameter:
		solventThreshEntry = self.wTree.get_widget("solventThresholdEntry")
 		minDiameterEntry = self.wTree.get_widget("minDiameterEntry")
		scanDx = PlaneSearch (dxObjectWater = waterDx, dxObjectProtein = proteinDx,
								minDiameter = minDiameterEntry.get_text(), 
								minProteinDens = protThreshEntry.get_text(), 
								minSolventDens = solventThreshEntry.get_text()
								)
		oneDimRadio = self.wTree.get_widget("search1DRadio")
		if self.__scanMethod == 1:
			scanType = "1D"
			xButton = self.wTree.get_widget("search1DXCheckBox")
			yButton = self.wTree.get_widget("search1DYCheckBox")
			zButton = self.wTree.get_widget("search1DZCheckBox")
			if xButton.get_active():
				scanDx.oneDimension ('x')
				scanType += " x"	
			if yButton.get_active():
				scanDx.oneDimension ('y')	
				scanType += " y"		
			if zButton.get_active():
				scanDx.oneDimension ('z')
				scanType += " z"	
		if self.__scanMethod == 2:		
			scanDx.twoDimension()
			scanType = "2D"
		if self.__scanMethod == 3:
			scanDx.threeDimension()
			scanType = "3D"
		filename = 'None'
		self.__dxTubeArray.append (TubeDx(scanDx.getDxObject(),filename,scanMethod = self.__scanMethod,scanned =scanType,waterObject = self.__dxTubeArray[self.__waterSelected].getDxObject(), proteinObject=self.__dxTubeArray[self.__proteinSelected].getDxObject(),minDiameter = minDiameterEntry.get_text() ,protThreshold =  protThreshEntry.get_text(), solventThreshold = solventThreshEntry.get_text(), protFile = proteinDx.getFilename(), solvFile = waterDx.getFilename(), version = self.__version))
		self.gtkDrawFileTable()
	
	def startAnalysePopUp(self,widget):
		glade = self.instPath+"/analyseDialog.libglade"
		print glade
		self.analyseDialog=gtk.glade.XML (fname=str(glade), domain="analyseDialog")	
		analysePopup = self.analyseDialog.get_widget("analysePopup")
		tablePopup = self.analyseDialog.get_widget("table1")
		
		tubeObject = self.__dxTubeArray[self.__fileSelected]
		self.groupeCombobox = gtk.combo_box_new_text()
		for tube in range (len (tubeObject.getGroupes() )):
			self.groupeCombobox.append_text(str(tube))
		tablePopup.attach(self.groupeCombobox,1,2,1,2,yoptions=0)
		
		analysePopup.show()
		self.groupeCombobox.show()
		dic = { "ANALYSE_TUBE_BUTTON_CLICKED" : self.startAnalyse,
				"ANALYSE_X" : self.toggleAnalyseAxisCB,
				"ANALYSE_Y" : self.toggleAnalyseAxisCB,
				"ANALYSE_Z" : self.toggleAnalyseAxisCB,
				"ANALYSE_METHOD_0": self.toggleAnalyseMethodCB,
				"ANALYSE_METHOD_1": self.toggleAnalyseMethodCB
				}
		self.analyseDialog.signal_autoconnect(dic)
		
	def startAnalyse (self,widget=None):
		tubeCounter = int( self.groupeCombobox.get_active() )
#voxelGroupGrid
#[x][y][z] = group		
		analyse = AnalyseTube (self.__dxTubeArray[self.__fileSelected].getVoxelGroupGrid(),tubeCounter)
		chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
		chooser.run()
		filename = chooser.get_filename()
# method 0 is area
		if self.__analyseMethod == 0:
			if self.__analyseAxis == 0:
				analyse.analyseTubeArea('x')
				analyse.writeStatistics(filename)
			if self.__analyseAxis == 1:
				analyse.analyseTubeArea('y')
				analyse.writeStatistics(filename)
			if self.__analyseAxis == 2:
				analyse.analyseTubeArea('z')
				analyse.writeStatistics(filename)
#method 1 is max diameter
		if self.__analyseMethod == 1:
			if self.__analyseAxis == 0:
				analyse.analyseTubeDiameterMax('x')
				analyse.writeStatistics(filename)
			if self.__analyseAxis == 1:
				analyse.analyseTubeDiameterMax('y')
				analyse.writeStatistics(filename)
			if self.__analyseAxis == 2:
				analyse.analyseTubeDiameterMax('z')
				analyse.writeStatistics(filename)				
		chooser.destroy()
		self.analyseDialog.get_widget("analysePopup").destroy()
	def groupTube (self,widget = None):
		dxTube = self.__dxTubeArray[self.__fileSelected]
		tubes = GroupTubes (dxTube.getDxObject())
		tubes.findGroups()
		dxTube.setGroupes (tubes.getTubeGroup())
		dxTube.setVoxelGroupGrid (tubes.getGroups())
		fillTubeButton = self.wTree.get_widget("fillTubeCheckButton")
		if fillTubeButton.get_active():
			protThreshEntry = self.wTree.get_widget("proteinThresholdEntry")
			protThresh = protThreshEntry.get_text()
			solvThreshEntry = self.wTree.get_widget("solventThresholdEntry")
			solvThresh = solvThreshEntry.get_text()
			fill = FillTube(dxObjectWater = dxTube.getWaterObject(),
							dxObjectProtein = dxTube.getProteinObject(), 
							dxObjectTube = dxTube.getDxObject(), 
							scanMethod = dxTube.getScanMethod(), 
							minProteinDensity = protThresh,
							minSolvDensity =  solvThresh,
							groups = dxTube.getGroupes(), 
							voxelGroupGrid  = dxTube.getVoxelGroupGrid()
							)
			fill.fillGroups()
			dxTube.setVoxelGroupGrid(fill.getVoxelGroupGrid())
			dxTube.setGroupes(fill.getGroups())
			dxTube.setDxObject(fill.getNewTubeObject())
			print "Finished cavity filling" 
		dxTube.setGrouped("Yes")
		self.gtkDrawFileTable()
	def openDx (self,file):
		chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		chooser.run()
		filename = chooser.get_filename()
		chooser.destroy()
		readDx = ReadOpenDx (filename)
		readDx.importDx()
		self.__dxTubeArray.append (TubeDx(readDx,filename))
		self.gtkDrawFileTable()
	def openPDB (self, widget = None):
		chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,
				  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		chooser.run()
		filename = chooser.get_filename()
		chooser.destroy()
		readPDB = ReadPDB ( filename)
		if readPDB.readPDB() == 0:
			self.__dxTubeArray.append (readPDB.getTubeDxObject())
			self.gtkDrawFileTable()	
	def saveDx(self,widget=None):
		dxObject = self.__dxTubeArray[self.__fileSelected].getDxObject()
		chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
		chooser.run()
		filename = chooser.get_filename()
		chooser.destroy()
		saveToDx = WriteDx (dxObject)
		saveToDx.write(filename)
		if ( re.match("^None",self.__dxTubeArray[self.__fileSelected].getFilename())):
			self.__dxTubeArray[self.__fileSelected].setFilename(filename)
			self.gtkDrawFileTable()
	def savePDB(self,file):
		chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
		chooser.run()
		filename = chooser.get_filename()
		temp = self.__dxTubeArray[self.__fileSelected]
		savePDB = WritePDB (temp)
		if self.__dxTubeArray[self.__fileSelected].getGrouped() == 'Yes':
			savePDB.writeGroups(self.__dxTubeArray[self.__fileSelected].getGroupes(),filename)
		else:
			savePDB.write(filename)
		chooser.destroy()
		
	def gtkDrawFileTable (self):
#this will also destroy the notebooklabel ! 
		self.__tableWidget.destroy()
		noteWidget = self.wTree.get_widget("notebook1")
		newTable = gtk.Table (rows = (len (self.__dxTubeArray)+1), columns= 9)
		
		noteLabel = gtk.Label (str="Files")
		fileLabel = gtk.Label (str="Files")
		setAsProtLabel = gtk.Label (str="Set as protein")
		setAsWaterLabel = gtk.Label (str="Set as water")
		setAsScannedLabel= gtk.Label (str="Scanned")
		groupedLabel = gtk.Label (str="Grouped")
		setCalcAvLabel = gtk.Label (str="Calc averages")
		minDiameterLabel = gtk.Label (str="Min diameter")
		minProtThresholdLabel = gtk.Label (str="Min protein density")
		minSolventLabel = gtk.Label (str="Min solvent density")
		

		noteWidget.insert_page(newTable, tab_label = noteLabel, position =0)
		newTable.show ()
		noteLabel.show()		
		newTable.attach (fileLabel,0,1,0,1,yoptions=0)
		newTable.attach (setAsProtLabel,1,2,0,1,yoptions=0)
		newTable.attach (setAsWaterLabel,2,3,0,1,yoptions=0)
		newTable.attach (setAsScannedLabel,3,4,0,1,yoptions=0)
		newTable.attach (groupedLabel,4,5,0,1,yoptions=0)
		newTable.attach (minDiameterLabel,5,6,0,1,yoptions=0)
		newTable.attach (minProtThresholdLabel,6,7,0,1,yoptions=0)
		newTable.attach (minSolventLabel,7,8,0,1,yoptions=0)
#		newTable.attach (setCalcAvLabel,5,6,0,1,yoptions=0)
		
		setAsScannedLabel.show()
		fileLabel.show()		
		setAsProtLabel.show()		
		setAsWaterLabel.show()		
		groupedLabel.show()	
		minDiameterLabel.show()
		minProtThresholdLabel.show()
		minSolventLabel.show()
#		setCalcAvLabel.show()
		selectProtein = self.__proteinSelected
#		print selectProtein
		for lineCounter in range (len (self.__dxTubeArray)):
			if (lineCounter == 0):
				self.__firstFileRadio = gtk.RadioButton (label=self.__dxTubeArray[lineCounter].getFilename(), use_underline=False)
				newTable.attach (self.__firstFileRadio,0,1,lineCounter+1,lineCounter+2,yoptions=0)
				self.__firstFileRadio.show()
				self.__firstFileRadio.connect("toggled", self.toggleFileCB)
				self.toggleFileCB (self.__firstFileRadio)
			else:
				fileRadio = gtk.RadioButton (group = self.__firstFileRadio, label=self.__dxTubeArray[lineCounter].getFilename(), use_underline=False)
				newTable.attach (fileRadio,0,1,lineCounter+1,lineCounter+2,yoptions=0)
				fileRadio.show()
				fileRadio.connect("toggled", self.toggleFileCB)
			if (lineCounter == 0):
				self.__firstProtRadioButton = gtk.RadioButton ()
				newTable.attach (self.__firstProtRadioButton,1,2,lineCounter+1,lineCounter+2,yoptions=0)
				self.__firstProtRadioButton.show()
				self.__firstProtRadioButton.connect("toggled", self.toggleProteinCB)
				self.toggleProteinCB(self.__firstProtRadioButton)
			else:
				setAsProtRadioButton = gtk.RadioButton (group = self.__firstProtRadioButton)	
				newTable.attach (setAsProtRadioButton,1,2,lineCounter+1,lineCounter+2,yoptions=0)
				setAsProtRadioButton.show()
				setAsProtRadioButton.connect("toggled", self.toggleProteinCB)
				
			if (lineCounter == 0):
				self.__firstWaterRadioButton = gtk.RadioButton ()
				newTable.attach (self.__firstWaterRadioButton,2,3,lineCounter+1,lineCounter+2,yoptions=0)
				self.__firstWaterRadioButton.show()
				self.__firstWaterRadioButton.connect("toggled", self.toggleWaterCB)
				self.toggleWaterCB(self.__firstWaterRadioButton)
			else:
				setAsWaterRadioButton = gtk.RadioButton (group = self.__firstWaterRadioButton)
				newTable.attach (setAsWaterRadioButton,2,3,lineCounter+1,lineCounter+2,yoptions=0)
				setAsWaterRadioButton.show()
				setAsWaterRadioButton.connect("toggled", self.toggleWaterCB)
			
			groupedLabel = gtk.Label (str=self.__dxTubeArray[lineCounter].getGrouped())
			setAsScannedLabel= gtk.Label (str=self.__dxTubeArray[lineCounter].getScanned())
			minDiameterValue = gtk.Label (str = self.__dxTubeArray[lineCounter].getMinDiameter())
			minProtThresholdValue = gtk.Label (str = self.__dxTubeArray[lineCounter].getProtThreshold())
			minSolventValue = gtk.Label (str = self.__dxTubeArray[lineCounter].getSolventThreshold())
			
			newTable.attach (setAsScannedLabel,3,4,lineCounter+1,lineCounter+2,yoptions=0)
			newTable.attach (groupedLabel,4,5,lineCounter+1,lineCounter+2,yoptions=0)
			newTable.attach (minDiameterValue,5,6,lineCounter+1,lineCounter+2,yoptions=0)
			newTable.attach (minProtThresholdValue,6,7,lineCounter+1,lineCounter+2,yoptions=0)
			newTable.attach (minSolventValue,7,8,lineCounter+1,lineCounter+2,yoptions=0)
			
			setAsScannedLabel.show()
			groupedLabel.show()	
			minDiameterValue.show()
			minProtThresholdValue.show()
			minSolventValue.show()
			
		self.__tableWidget = newTable
		noteWidget.set_current_page(0)
app=appgui()
gtk.main()

