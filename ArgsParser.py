#! /usr/bin/env python

"""
Gisto - Gitso is to support others

Gitso is a utility to facilitate the connection of VNC

@author: Aaron Gerber ('gerberad') <gerberad@gmail.com>
@author: Derek Buranen ('burner') <derek@buranen.info>
@author: AustP
@copyright: 2008 - 2014

Gitso is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Gitso is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Gitso.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import signal
import os.path
import urllib
import re

class ArgsParser:
	def __init__(self):
		# Initialize Self.paths here.
		self.paths = dict()
		self.paths['resources'] = os.path.join(sys.path[0], "./")
		self.paths['preferences'] = ''
		self.paths['copyright'] = ''
		self.paths['main'] = ''
		self.paths['listen'] = False
		self.paths['connect'] = ''
		self.paths['list'] = []
		self.paths['mode'] = ''
		self.paths['low-colors'] = False
		self.port = "5500"
		
		if re.match('(?:open|free|net)bsd|linux',sys.platform):
			self.paths['main'] = os.path.join(sys.path[0], '..', 'share', 'gitso')
			self.paths['copyright'] = os.path.join(sys.path[0], '..', 'share', 'doc', 'gitso', 'COPYING')
		elif sys.platform == "darwin":
			self.paths['main'] = sys.path[0]
			self.paths['copyright'] = os.path.join(sys.path[0], 'COPYING')
		else:
			self.paths['main'] = os.path.join(sys.path[0], '..')
			self.paths['copyright'] = os.path.join(sys.path[0], '..', 'COPYING')
		
		#for i in range(1, len(sys.argv)):
		i = 1
		while i < len(sys.argv):
			if sys.argv[i] == '--help': # --help
				self.HelpMenu()
			elif sys.argv[i] == '--version': # --version
				print "Gitso 0.6.3  -- Copyright 2007 - 2014 Aaron Gerber and Derek Buranen and AustP."
				exit(0)
			elif sys.argv[i] == '--dev': # --dev
				print "Running in 'Development Mode'"
				self.paths['mode'] = 'dev'
				if sys.platform == "darwin":
					if not os.path.exists('build/OSXvnc'):
						os.popen("mkdir build; cp arch/osx/OSXvnc.tar.gz build ; cd build ; tar xvfz OSXvnc.tar.gz > /dev/null")
					if not os.path.exists('build/cotvnc.app'):
						os.popen("cp arch/osx/cotvnc.app.tar.gz build ; cd build ; tar xvfz cotvnc.app.tar.gz > /dev/null")
						
					self.paths['resources'] = 'build/'
					self.paths['main']		= sys.path[0]
					self.paths['copyright'] = os.path.join(sys.path[0], 'COPYING')
					
				elif sys.platform == "win32":
					self.paths['copyright'] = os.path.join(sys.path[0], 'COPYING')
					self.paths['main']		= os.path.join(sys.path[0])
					self.paths['resources'] = 'arch/win32/'
					
				else:
					self.paths['resources'] = 'arch/linux/'
					self.paths['main']		= os.path.join(sys.path[0])
					self.paths['copyright'] = os.path.join(sys.path[0], 'COPYING')

			elif sys.argv[i] == '--listen': # --listen
				if self.paths['connect'] <> "":
					print "Error: --connect and --listen can not be used at the same time."
					self.HelpMenu()

				i = i + 1
				if i >= len(sys.argv):
					self.port = "5500"
				else:
					if sys.argv[i][0] + sys.argv[i][1] <> "--":
						self.port = sys.argv[i]
					else:
						self.port = "5500"
						i = i - 1

				self.paths['listen'] = True

			elif sys.argv[i] == '--connect': # --connect
				i = i + 1
				if i >= len(sys.argv):
					print "Error: No IP or domain name given."
					self.HelpMenu()

				if self.paths['listen']:
					print "Error: --connect and --listen can not be used at the same time."
					self.HelpMenu()
				
				if sys.argv[i][0] + sys.argv[i][1] <> "--":
					self.paths['connect'] = sys.argv[i]
				else:
					print "Error: '" + sys.argv[i] + "' is not a valid host with '--connect'."
					self.HelpMenu()

			elif sys.argv[i] == '--low-colors': # --low-colors
				self.paths['low-colors'] = True;

			elif sys.argv[i] == '--list': # --list
				i = i + 1
				if i >= len(sys.argv):
					print "Error: No List file given."
					self.HelpMenu()
				
				if sys.argv[i][0] + sys.argv[i][1] <> "--":
					self.paths['list'] = self.getHosts(sys.argv[i])
				else:
					print "Error: '" + sys.argv[i] + "' is not a valid list with '--list'."
					self.HelpMenu()

			else:
				print "Error: '" + sys.argv[i] + "' is not a valid argument."
				self.HelpMenu()

			i = i + 1
		
		if sys.platform == "darwin":
				self.paths['preferences'] = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Gitso")
				if os.path.exists(self.paths['preferences']) != True:
						os.makedirs(self.paths['preferences'], 0700)
				self.paths['preferences'] = os.path.join(self.paths['preferences'], "hosts")
		elif sys.platform == "win32":
				self.paths['preferences'] = os.path.join(os.getenv('USERPROFILE'), "gitso-hosts")
		else:
				self.paths['preferences'] = os.path.join(os.path.expanduser("~"), ".gitso-hosts")

	#Help Menu
	def HelpMenu(self):
		print "Usage: " + os.path.basename(sys.argv[0]) + " [OPTION]"
		print "   OPTIONS"
		print "   --dev\t\tSet self.paths for development."
		print "   --listen {PORT}\tListen for incoming connections."
		print "   --connect {IP|DN}\tConnects to host (support giver)."
		print "   --list {URL|FILE}\tAlternative Support list."
		print "   --low-colors\t\tUse 8bit colors (for slow connections). Linux only."
		print "   --version\t\tThe current Gitso version."
		print "   --help\t\tThis Menu."
		sys.exit(1)
	
	def GetPaths(self):
		return self.paths
		
	def GetPort(self):
		return self.port
		
	def getHosts(self, file):
		list = []
		fileList = ""
		
		if len(file) > 3:
			prefix = file[0] + file[1] + file[2] + file[3]
		else:
			prefix = ""
		
		if prefix == "www." or prefix == "http":
			handle = urllib.urlopen(file)
			fileList = handle.read()
			handle.close()
		else:
			if os.path.exists(file):
				handle = open(file, 'r')
				fileList = handle.read()
				handle.close()
		
		parsedlist = fileList.split(",")
		for i in range(0, len(parsedlist)):
			if self.validHost(parsedlist[i].strip()):
				list.append(parsedlist[i].strip())
		
		return list

	def validHost(self, host):
		if host != "" and host.find(";") == -1 and host.find("/") == -1 and host.find("'") == -1 and host.find("`") == -1 and len(host) > 6:
			return True
		else:
			return False

