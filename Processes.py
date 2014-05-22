#! /usr/bin/env python

"""
Gisto - Gitso is to support others

Gitso is a utility to facilitate the connection of VNC

@author: Aaron Gerber ('gerberad') <gerberad@gmail.com>
@author: Derek Buranen ('burner') <derek@buranen.info>
@copyright: 2008 - 2010

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

import wx
import os, sys, signal, os.path, re

class Processes:
	def __init__(self, window, paths):
		self.returnPID = 0
		self.window = window
		self.paths = paths

	def getSupport(self, host):
		if sys.platform == 'darwin':
			self.returnPID = os.spawnl(os.P_NOWAIT, '%sOSXvnc/OSXvnc-server' % self.paths['resources'], '%sOSXvnc/OSXvnc-server' % self.paths['resources'], '-connectHost', '%s' % host)
		elif re.match('(?:open|free|net)bsd|linux',sys.platform):
			# We should include future versions with options for speed.
			#self.returnPID = os.spawnlp(os.P_NOWAIT, 'x11vnc', 'x11vnc','-nopw','-ncache','20','-solid','black','-connect','%s' % host)
			
			self.returnPID = os.spawnlp(os.P_NOWAIT, 'x11vnc', 'x11vnc','-nopw','-ncache','20','-connect','%s' % host)
			
			# Added for OpenBSD compatibility
			import time
			time.sleep(3)
		elif sys.platform == 'win32':
			import subprocess
                        self.returnPID = subprocess.Popen(['WinVNC.exe'])
			print "Launched WinVNC.exe, waiting to run -connect command..."
			import time
			time.sleep(3)
			
			if self.paths['mode'] == 'dev':
				subprocess.Popen(['%sWinVNC.exe' % self.paths['resources'], '-connect', '%s' % host])
			else:
				subprocess.Popen(['WinVNC.exe', '-connect', '%s' % host])
		else:
			print 'Platform not detected'
		return self.returnPID
	
	def giveSupport(self, port):
		if sys.platform == 'darwin':
			vncviewer = '%scotvnc.app/Contents/MacOS/cotvnc' % self.paths['resources']
			self.returnPID = os.spawnlp(os.P_NOWAIT, vncviewer, vncviewer, '--listen', port)
		elif re.match('(?:open|free|net)bsd|linux',sys.platform):
			
			# These are the options for low-res connections.
			# In the future, I'd like to support cross-platform low-res options.
			# What aboot a checkbox in the gui
			if self.paths['low-colors'] == False:
				self.returnPID = os.spawnlp(os.P_NOWAIT, 'vncviewer', 'vncviewer', '-listen', port)
			else:
				self.returnPID = os.spawnlp(os.P_NOWAIT, 'vncviewer', 'vncviewer', '-bgr233', '-listen', port)
		elif sys.platform == 'win32':
			import subprocess
			if self.paths['mode'] == 'dev':
				self.returnPID = subprocess.Popen(['%svncviewer.exe' % self.paths['resources'], '-listen', port])
			else:
				self.returnPID = subprocess.Popen(['vncviewer.exe', '-listen', port])
		else:
			print 'Platform not detected'
		
		return self.returnPID

	def KillPID(self):
		"""
		Kill VNC instance, called by the Stop Button or Application ends.
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		if self.returnPID != 0:
			print "Processes.KillPID(" + str(self.returnPID) + ")"
			if sys.platform == 'win32':
				import win32api
				PROCESS_TERMINATE = 1
				handle = win32api.OpenProcess(PROCESS_TERMINATE, False, self.returnPID.pid)
				win32api.TerminateProcess(handle, -1)
				win32api.CloseHandle(handle)
			elif re.match('(?:open|free|net)bsd|linux',sys.platform):
				# New processes are created when you made connections. So if you kill self.returnPID,
				# you're just killing the dispatch process, not the one actually doing business...
				os.spawnlp(os.P_NOWAIT, 'pkill', 'pkill', '-f', 'vncviewer')
				os.spawnlp(os.P_NOWAIT, 'pkill', 'pkill', '-f', 'x11vnc')
			else:
				os.kill(self.returnPID, signal.SIGKILL)
			self.returnPID = 0
		return

