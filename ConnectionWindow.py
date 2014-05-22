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
import os, sys, signal, os.path, time, thread, re
import AboutWindow, GitsoThread

class GitsoTaskBarIcon(wx.TaskBarIcon):
	def __init__(self, icon, frame):
		wx.TaskBarIcon.__init__(self)
		self.SetIcon(icon, "Gitso")
		self.frame = frame
		
	def CreatePopupMenu(self):
		self.menu = wx.Menu()
		self.menu.Append(20, "Restore Gitso")
		self.menu.Append(21, "Quit Gitso")
		wx.EVT_MENU(self.menu, 20, self.frame.RestoreWindow)
		wx.EVT_MENU(self.menu, 21, self.frame.OnCloseWindow)
		return self.menu

class ConnectionWindow(wx.Frame):
	"""
	Main Window for Gitso
	
	@author: Derek Buranen
	@author: Aaron Gerber
	"""
	def __init__(self, parent, id, title, paths, port):
		"""
		Setup Application Window
		
		@author: Derek Buranen
		@author: Aaron Gerber
		@author: Markus Roth
		"""
		self.ToggleValue = 0
		self.paths = paths
		self.port = port
		self.thread = None
		self.threadLock = thread.allocate_lock()
		
		# Disable until 0.7 release
		self.enablePMP = False
		
		if re.match('(?:open|free|net)bsd|linux',sys.platform):
			width = 165
			height = 350
			xval1 = 155
			xval2 = 250
		else:
			height = 350
			width = 175
			xval1 = 180
			xval2 = 265
		
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(height,width), style=wx.DEFAULT_FRAME_STYLE & ~(wx.FRAME_SHAPED | wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX))
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		self.Bind(wx.EVT_ICONIZE, self.OnIconizeWindow)
		
		if sys.platform == 'win32':
			icon = wx.Icon(os.path.join(self.paths['main'], 'icon.ico'), wx.BITMAP_TYPE_ICO)
			self.SetBackgroundColour(wx.Colour(236,233,216))
		else:
			icon = wx.Icon(os.path.join(self.paths['main'], 'icon.ico'), wx.BITMAP_TYPE_ICO)
			
		self.SetIcon(icon)
		self.TrayIcon = GitsoTaskBarIcon(icon, self)
		wx.EVT_TASKBAR_LEFT_UP(self.TrayIcon, self.RestoreWindow)
		
		#Buttons
		self.connectButton = wx.Button(self, 10, "Start", wx.Point(xval1, 81))
		self.connectButton.SetDefault()
		wx.EVT_BUTTON(self, 10, self.ConnectSupport)
		self.stopButton = wx.Button(self, wx.ID_STOP, "", wx.Point(xval2, 81))
		self.stopButton.Enable(False)
		wx.EVT_BUTTON(self, wx.ID_STOP, self.KillPID)
		
		# Radio Boxes
		self.rb1 = wx.RadioButton(self, -1, 'Get Help', (10, 15), style=wx.RB_GROUP)
		self.rb2 = wx.RadioButton(self, -1, 'Give Support', (10, 48))
		self.rb1.SetValue(True)
		
		self.Bind(wx.EVT_RADIOBUTTON, self.RadioToggle, id=self.rb1.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.RadioToggle, id=self.rb2.GetId())
		
		# checkbox for natpmp
		if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
			if self.enablePMP:
				self.cb1 = wx.CheckBox(self, -1, 'Use NAT-PMP', (130, 48))
				self.cb1.Enable(False)

		# Checkbox for low color
		self.cb2 = wx.CheckBox(self, -1, 'Use low colors', (10, 81))
		self.cb2.Set3StateValue(False)
		self.cb2.SetValue(self.paths['low-colors']) # Use value of --low-colors from command line
		self.cb2.Enable(False)
		
		# the combobox Control
		self.sampleList = self.paths['list']
		
		self.sampleList = self.getHosts(self.sampleList, os.path.join(self.paths['main'], 'hosts.txt'))
		self.sampleList = self.getHosts(self.sampleList, self.paths['preferences'])
		self.displayHostBox(self.sampleList, "Enter/Select Support Address")
		
		# Menu      
		menuBar = wx.MenuBar()
		fileMenu = wx.Menu()
		
		editMenu = wx.Menu()
		editMenu.Append(11, "&Cut\tCtrl+X", "Cut IP Address")
		editMenu.Append(12, "&Copy\tCtrl+C", "Copy IP Address")
		editMenu.Append(wx.ID_PASTE, "&Paste\tCtrl+V", "Paste IP Address")
		wx.EVT_MENU(self, 11, self.SetClipboard)
		wx.EVT_MENU(self, 12, self.SetClipboard)
		wx.EVT_MENU(self, wx.ID_PASTE, self.GetClipboard)
		
		fileMenu.Append(13, "&Clear History", "Clear History")
		if sys.platform == 'darwin':
			fileMenu.Append(wx.ID_ABOUT, "&About", "About Gitso")
			wx.EVT_MENU(self, wx.ID_ABOUT, self.ShowAbout)
		else:       
			fileMenu.Append(wx.ID_EXIT, "&Quit\tCtrl+Q", "Quit Gitso")
			wx.EVT_MENU(self, wx.ID_EXIT, self.OnCloseWindow)
		
		helpMenu = wx.Menu()
		helpMenu.Append(wx.ID_ABOUT, "&About", "About Gitso")
		wx.EVT_MENU(self, wx.ID_ABOUT, self.ShowAbout)
		
		wx.EVT_MENU(self, 13, self.clearHistory)
		
		menuBar.Append(fileMenu, "&File")
		menuBar.Append(editMenu, "&Edit")
		
		if re.match('(?:open|free|net)bsd|linux',sys.platform) or sys.platform == 'win32':
			menuBar.Append(helpMenu, "&Help")
		
		self.SetMenuBar(menuBar)
		
		self.statusBar = self.CreateStatusBar()
		self.statusBar.SetStatusWidths([350])
		self.setMessage("Idle", False)
		
		self.SetDefaultItem(self.hostField)
		self.hostField.SetFocus()
		
		self.SetThemeEnabled(True)
		self.Centre()
		self.Show(True)
		
		if self.paths['listen']:
			self.Iconize(True)
			self.rb2.Value = True
			self.RadioToggle(None)
			self.ConnectSupport(None)
		elif self.paths['connect'] <> "":
			self.rb1.Value = True
			self.RadioToggle(None)
			self.hostField.Value = self.paths['connect']
			self.ConnectSupport(None)


	def RadioToggle(self, event):
		"""
		Toggles Radio Buttons
		
		@author: Derek Buranen
		@author: Aaron Gerber
		@author: Markus Roth
		"""
		if self.rb1.GetValue():
			self.ToggleValue = 0
			self.hostField.Enable(True)
			self.cb2.Enable(False)
			if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
				if self.enablePMP:
					self.cb1.Enable(False)
		else:
			self.ToggleValue = 1
			self.hostField.Enable(False)
			self.cb2.Enable(True)
			if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
				if self.enablePMP:
					self.cb1.Enable(True)


	def ConnectSupport(self, event):
		"""
		Call VNC in a thread.
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		if self.rb1.GetValue(): # Get Help
			if self.validHost(self.hostField.GetValue().strip()) and self.hostField.GetValue() != "Enter/Select Support Address":
				self.setMessage("Connecting...", True)
				
				host = self.hostField.GetValue().strip()
				
				self.sampleList = []
				self.sampleList = self.getHosts(self.sampleList, os.path.join(self.paths['main'], 'hosts.txt'))
				self.sampleList = self.getHosts(self.sampleList, self.paths['preferences'])
				
				if self.sampleList.count(host) == 0:
					self.saveHost(self.paths['preferences'], host)
					self.sampleList.append(host)
					self.hostField.Destroy()
					self.displayHostBox(self.sampleList, host)
				
				self.createThread(host)
			else:
				self.setMessage("Invalid Support Address", False)
		else: # Give Suppport
			self.setMessage("Starting Server...", True)
			self.createThread()


	def ShowAbout(self,e):
		"""
		Display About Dialog
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		about = AboutWindow.AboutWindow(self, wx.ID_ABOUT, "About Gitso", self.paths)
	
	
	def clearHistory(self, event):
		handle = open(self.paths['preferences'], 'w')
		handle.write("")
		handle.close()
		
		text = self.hostField.GetValue()
		self.hostField.Destroy()

		self.sampleList = []
		self.sampleList = self.getHosts(self.sampleList, os.path.join(self.paths['main'], 'hosts.txt'))
		self.sampleList = self.getHosts(self.sampleList, self.paths['preferences'])

		self.displayHostBox(self.sampleList, text)
	
	
	def GetClipboard(self, menu, data=None):
		"""
		Paste clipboard text in Support Entry Field
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		do = wx.TextDataObject()
		wx.TheClipboard.Open()
		clip = wx.TheClipboard.GetData(do)
		wx.TheClipboard.Close()
		
		if clip:
			self.hostField.SetValue(do.GetText())
	
	
	def SetClipboard(self, menu, data=None):
		"""
		Set the value of the clipboard
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		self.clipdata = wx.TextDataObject()
		self.clipdata.SetText(self.hostField.GetValue())
		wx.TheClipboard.Open()
		wx.TheClipboard.SetData(self.clipdata)
		wx.TheClipboard.Close()
		if menu.GetId() == 11:
			self.hostField.SetValue("")
	
	
	def KillPID(self, showMessage=True):
		"""
		Kill VNC instance, called by the Stop Button or Application ends.
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		if self.thread <> None:
			self.thread.kill()
			# If you don't wait 0.5+ seconds, the interface won't reload and it'll freeze.
			# Possibly on older systems you should wait longer, it works fine on mine...
			time.sleep(.5)
		self.thread = None
		if showMessage :
			self.setMessage("Idle.", False)
		return
	
	def OnCloseWindow(self, evt):
		self.KillPID()
		self.Destroy()
	
	def OnIconizeWindow(self, evt):
		self.Hide()
	
	def RestoreWindow(self, evt):
		if self.IsIconized():
			self.Iconize(False)
			if not self.IsShown():
				self.Show(True)
				self.Raise()
	
	def validHost(self, host):
		if host != "" and host.find(";") == -1 and host.find("/") == -1 and host.find("'") == -1 and host.find("`") == -1 and len(host) > 6:
			return True
		else:
			return False
	
	
	def getHosts(self, arr, file):
		list = arr
		if os.path.exists(file):
			handle = open(file, 'r')
			fileList = handle.read()
			parsedlist = fileList.split(",")
			for i in range(0, len(parsedlist)):
				if self.validHost(parsedlist[i].strip()):
					list.append(parsedlist[i].strip())
			handle.close()
		return list
	
	
	def saveHost(self, file, host):
		if os.path.exists(file):
			handle = open(file, 'a')
			handle.write(", %s" % host)
			handle.close()
	
	def displayHostBox(self, list, text):
		self.hostField = wx.ComboBox(self, 30, "", wx.Point(105, 12), wx.Size(230, -1), list, wx.CB_DROPDOWN)
		self.hostField.SetValue(text)

	def setMessage(self, message, status):
		if self.threadLock.locked():
			return

		self.threadLock.acquire()

		self.statusBar.SetStatusText(message, 0)

		if status:
			self.connectButton.Enable(False)
			self.stopButton.Enable(True)
		else:
			self.connectButton.Enable(True)
			self.stopButton.Enable(False)

		
		if self.ToggleValue == 0:
			self.rb1.SetValue(True)
		else:
			self.rb2.SetValue(True)
		
		self.threadLock.release()

	def createThread(self, host=""):
		self.paths['low-colors'] = self.cb2.GetValue() # Set low-colors to value of checkbox
		self.KillPID(False)
		self.thread = GitsoThread.GitsoThread(self, self.paths, self.port)
		self.thread.setHost(host)
		self.thread.start()

		# If you don't wait 1+ seconds, the interface won't reload and it'll freeze.
		# Possibly on older systems you should wait longer, it works fine on mine...
		time.sleep(1)

