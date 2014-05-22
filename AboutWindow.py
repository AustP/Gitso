import wx
import os, os.path, sys, cStringIO


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

class InfoPage(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		infostring = "Authors:" + "\n\tAaron Gerber\n\tDerek Buranen"
		infostring = infostring + "\n\nContributors:" + "\n\tNick Verbeck" + "\n\tTroy Frew" + "\n\tDennis Koot"
		infostring = infostring + "\n\nCopyright (C) 2007 - 2014 by Aaron Gerber and Derek Buranen and AustP"
		if sys.platform == "darwin":
			infostring = infostring + "\n\n+++++++++++++++++++++++"
			infostring = infostring + "\nChicken Of The VNC:"
			infostring = infostring + "\n\tCopyright (C) 2002-2006 by Jason Harris"
			infostring = infostring + "\n\tCopyright (C) 1998-2000 by Helmut Maierhofer"

			infostring = infostring + "\n\nlibJPEG: Independent JPEG Group's JPEG software"
			infostring = infostring + "\n\tCopyright (C) 1991-1998, Thomas G. Lane."

			infostring = infostring + "\n\nOSXvnc:"
			infostring = infostring + "\n\tCopyright (C) 2002-2007 by Redstone Software: "
			infostring = infostring + "\n\t\tDoug Simons and Jonathan Gillaspie"
	
			infostring = infostring + "\n\nechoWare:"
			infostring = infostring + "\n\tCopyright (C) 2004-2007 Echogent Systems, Inc"
		elif sys.platform == "win32":
			infostring = infostring + "\n\n+++++++++++++++++++++++"
			infostring = infostring + "\nTightVNC && VNCviewer:"
			infostring = infostring + "\n\tCopyright (C) 1999 AT&T Laboratories Cambridge."

			infostring = infostring + "\n\nVNCHooks:"
			infostring = infostring + "\n\tCopyright (C) 2000-2007 TightVNC Group"

		info = wx.TextCtrl(self, -1, infostring, style=wx.TE_MULTILINE | wx.ST_NO_AUTORESIZE)
		
		pagesizer = wx.BoxSizer(wx.VERTICAL);
		pagesizer.Add(info, 1, wx.EXPAND)
		self.SetSizer(pagesizer);
		pagesizer.SetSizeHints(self);
		

class LicensePage(wx.Panel):
	def __init__(self, parent, paths):
		wx.Panel.__init__(self, parent)

		license = open(paths['copyright'], 'r')
		copyright = wx.TextCtrl(self, -1, license.read(), style=wx.TE_MULTILINE | wx.ST_NO_AUTORESIZE)
		copyright.SetEditable(False)
		
		pagesizer = wx.BoxSizer(wx.VERTICAL);
		pagesizer.Add(copyright, 1, wx.EXPAND);

		self.SetSizer(pagesizer);
		pagesizer.SetSizeHints(self);



class AboutWindow(wx.Frame):
	def __init__(self, parent, id, title, paths):
		"""
		Setup About Window for Gitso
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(525,400), style=wx.CLOSE_BOX | wx.MINIMIZE_BOX)
		
		if sys.platform == 'win32':
			self.SetBackgroundColour(wx.Colour(236,233,216))

		icon = wx.Icon(os.path.join(paths['main'], 'icon.ico'), wx.BITMAP_TYPE_ICO)
		self.SetIcon(icon)

		## Headings ##
		text1 = wx.StaticText(self, wx.ID_ANY, 'Gitso')
		font1 = wx.Font(24, wx.NORMAL, wx.NORMAL, wx.BOLD)
		text1.SetFont(font1)

		text2 = wx.StaticText(self, -1, "Gitso is to Support Others")
		text3 = wx.StaticText(self, -1, "Version 0.6.3")
		font2 = wx.Font(16, wx.NORMAL, wx.NORMAL, wx.NORMAL)
		font3 = wx.Font(12, wx.NORMAL, wx.NORMAL, wx.NORMAL)
		text2.SetFont(font2)
		text3.SetFont(font3)
		url = wx.HyperlinkCtrl(self, -1, "github.com/AustP/Gitso", "https://github.com/AustP/Gitso")
		
		data = open(os.path.join(paths['main'], 'icon.png'), "rb").read()
		stream = cStringIO.StringIO(data)
		img = wx.ImageFromStream(stream)
		img.Rescale(150, 150)
		bmp = wx.BitmapFromImage(img)
		image1 = wx.StaticBitmap(self, -1, bmp)
		
		## Buttons ##
		ok = wx.Button(self, wx.ID_OK, "OK")
		self.SetDefaultItem(ok)
		ok.SetFocus()
		wx.EVT_BUTTON(self, wx.ID_OK, self.CloseAbout)
		
		## Sizers ##
		topsizer = wx.BoxSizer(wx.VERTICAL);

		info_sizer = wx.BoxSizer(wx.VERTICAL);
		info_sizer.Add(text1, 0, wx.ALIGN_CENTER | wx.ALL, 7);
		info_sizer.Add(text2, 0, wx.ALIGN_CENTER | wx.ALL, 3);
		info_sizer.Add(text3, 0, wx.ALIGN_CENTER | wx.ALL, 3);
		info_sizer.Add(url, 0, wx.ALIGN_CENTER | wx.ALL, 3);

		heading_sizer = wx.BoxSizer(wx.HORIZONTAL);
		heading_sizer.Add(image1, 0, wx.ALIGN_LEFT | wx.ALL, 10 );
		heading_sizer.Add(info_sizer, 0, wx.ALL, 10 );

		topsizer.Add(heading_sizer, 0, wx.ALIGN_CENTER);

		## Tabs ##
		nb = wx.Notebook(self, size=wx.Size(525,220))
		
		license_page = LicensePage(nb, paths)
		info_page = InfoPage(nb)
		
		nb.AddPage(info_page, "Authors")
		nb.AddPage(license_page, "License")
		
		tab_sizer = wx.BoxSizer(wx.HORIZONTAL);
		tab_sizer.Add(nb, 1, wx.EXPAND | wx.ALL, 10 );
		topsizer.Add(tab_sizer, 1, wx.ALIGN_RIGHT );

		## Buttons ##
		button_sizer = wx.BoxSizer(wx.HORIZONTAL);
		button_sizer.Add(ok, 0, wx.ALL, 10 );
		topsizer.Add(button_sizer, 0, wx.ALIGN_RIGHT );

		## Final settings ##
		self.SetSizer(topsizer);
		topsizer.SetSizeHints(self);

		self.SetThemeEnabled(True)
		self.Centre()
		self.Show()
		
	
	def CloseAbout(self, event):
		self.Close()

