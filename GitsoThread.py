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

import threading, time
import os, sys, signal, os.path, re
import Processes

if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
	import NATPMP

class GitsoThread(threading.Thread):
	def __init__(self, window, paths, port):
		self.window  = window
		self.paths   = paths
		self.port    = port
		self.host    = ""
		self.error   = False
		self.pid     = 0
		self.running = True
		self.process = Processes.Processes(self.window, paths)
		threading.Thread.__init__(self)
		
		
	def run(self):
		"""
		This is where the beef is. Start the processes and check on them.
		
		@author: Aaron Gerber
		"""
		if self.host <> "":
			# Get Help
			self.pid = self.process.getSupport(self.host)
			time.sleep(.5)
			if self.checkStatus():
				self.window.setMessage("Connected.", True)
			else:
				self.window.setMessage("Could not connect.", False)
				self.error = True
		else:
			# Give Support
			if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
				if self.window.enablePMP:
					self.window.cb1.Enable(False)
					if self.window.cb1.GetValue() == True:
						self.NATPMP('request')
			
			self.pid = self.process.giveSupport(self.port)
			time.sleep(.5)
			if self.checkStatus():
				self.window.setMessage("Server running.", True)
			else:
				self.window.setMessage("Could not start server.", False)
				self.error = True

		print "GitsoThread.run(pid: " + str(self.pid) + ") running..."

		while(self.running and self.checkStatus()):
			time.sleep(.2)

		if not self.error:
			self.window.setMessage("Idle.", False)

		self.kill()

		
	def setHost(self, host=""):
		"""
		Set the object variable.
		
		@author: Aaron Gerber
		"""
		self.host = host
		
		
	def kill(self):
		"""
		Kill the process and general clean-up.
		
		@author: Aaron Gerber
		"""
		if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
			if self.window.enablePMP:
				if self.window.rb1.GetValue() == False: #give support
					if self.window.cb1.GetValue() == True:
						self.NATPMP('giveup')
					self.window.cb1.Enable(True)
	
		self.process.KillPID()
		self.pid = 0
		self.running = False


	def checkStatus(self):
		"""
		Check the status of the underlying process.
		
		@author: Aaron Gerber
		"""
		if self.pid == 0:
			return False
		
		connection = []
		listen = []
		if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
			if self.host <> "":
				connection = os.popen('LANG=C netstat -an | grep 5500 | grep ESTABLISHED').readlines()
			else:
				listen = os.popen('LANG=C netstat -an | grep 5500 | grep LISTEN').readlines()
		elif sys.platform == 'win32':
			#XP PRO only -- Need to fix the case where there is no process, it'll still return 1 line.
			#info = os.popen('WMIC PROCESS ' + str(self.pid) + ' get Processid').readlines()
			if self.host <> "":
				connection = os.popen('netstat -a | find "ESTABLISHED" | find "5500"').readlines()
			else:
				listen = os.popen('netstat -a | find "LISTEN" | find "5500"').readlines()
		else:
			print 'Platform not detected'
		
		if len(connection) == 0 and len(listen) == 0:
			return False
		else:
			return True


	def NATPMP(self, action):
		"""
		Call NAT-PMP on router to get port 5500 forwarded.
		
		@author: Dennis Koot
		"""
		if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
			if self.window.enablePMP:
				if action == 'request':
					lifetime = 3600
					print "Request port 5500 (NAT-PMP)."
				else:
					lifetime = 0
					print "Give up port 5500 (NAT-PMP)."
		
				pubpriv_port = int(5500)
				protocol = NATPMP.NATPMP_PROTOCOL_TCP
				
				try:
					gateway = NATPMP.get_gateway_addr()
					print NATPMP.map_port(protocol, pubpriv_port, pubpriv_port, lifetime, gateway_ip=gateway)
				except:
					print "Warning: Unable to automap port."

