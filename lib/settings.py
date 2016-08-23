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



# dxTuber v0.2
# +new routine to parse settings from $HOME/.dxTuber/dxTuber.conf
#

import os, re

class Settings():


	def getVersion(self):
		dxTuberConfFile = os.environ['HOME']+"/.dxTuber/dxTuber.conf"
		conf = open (dxTuberConfFile,'r')
		confLines = conf.readlines()

		for line in confLines:
			if re.match ('^#',line):
				continue
			if re.match('VERSION',line):
				tmpArray = re.split('\s',line,1)
				tmp = re.sub('\"','',tmpArray[1])
				tmp = re.sub('\n','',tmp)
				version = re.sub('^\s','',tmp)
		return version 
