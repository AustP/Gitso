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

import sys, platform, re


if sys.platform == 'darwin':
	# If we're on Snow Leopard, we want to use Python 2.5 until we figure out what Apple's doing with 2.6
	ver = platform.mac_ver()

	if re.match('10\.5', ver[0]) <> None:
		"""
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python26.zip')
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5')
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/plat-darwin')
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/plat-mac')
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/plat-mac/lib-scriptpackages')
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/Extras/lib/python')
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/lib-tk')
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/lib-old')
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/lib-dynload')
		sys.path.append('/Library/Python/2.5/site-packages')
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/Extras/lib/python/PyObjC')
		"""
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/Extras/lib/python/wx-2.8-mac-unicode')
	elif re.match('10\.6', ver[0]) <> None:
		sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.6/Extras/lib/python/wx-2.8-mac-unicode')

import wx
import ConnectionWindow, ArgsParser


if __name__ == "__main__":
	app = wx.PySimpleApp()
	args = ArgsParser.ArgsParser()
	ConnectionWindow.ConnectionWindow(None, -1, "Gitso", args.GetPaths(), args.GetPort())
	app.MainLoop()
	del app
