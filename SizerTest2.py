#!/usr/bin/env python2.3

import wx

class MyFrame(wx.Frame):
	def __init__(self, parent, id, name):
		wx.Frame.__init__ (self,
				   parent,
				   id,
				   name,
				   size = wx.DefaultSize,
				   style = (wx.DEFAULT_DIALOG_STYLE |
					    wx.MAXIMIZE_BOX |
					    wx.THICK_FRAME |
					    wx.RESIZE_BORDER)
				   )
		self.status = self.CreateStatusBar()
		
		btn1above = wx.Button(self, -1,  "Create")
		btn2above = wx.Button(self, -1,  "Ok")
		btn1right = wx.Button(self, -1,  "Cancel")
		btnbrowser = wx.Button(self, -1,  "Browse")
		btnmenu = wx.Button(self, -1,  "Menu")
		lst = wx.ListCtrl(self, -1)
		self.chkMatchCase = wx.CheckBox(self, -1, "Match Case")
		self.chkRegularExpression = wx.CheckBox(self, -1,"RegularExpression")
		self.chkSubDirectories = wx.CheckBox(self, -1, "Subdirectories")

#		status = wx.StatusBar(self, -1)		
		
		helpsizer = wx.BoxSizer(wx.VERTICAL)
		helpsizer.Add((0, 5), 0, wx.ALL, 0)
		helpsizer.Add(btnbrowser, 0, wx.ALL, 0)
		helpsizer.Add((0, 30), 0, wx.ALL, 0)
		helpsizer.Add(btnmenu, 0, wx.ALL, 0)
		helpsizer.Add((0, 40), 0, wx.ALL, 0)
		helpsizer.Add(btn1above, 0, wx.ALL, 0)
		helpsizer.Add((0, 5), 0, wx.ALL, 0)
		helpsizer.Add(self.chkRegularExpression, 0, wx.ALL, 0)
		helpsizer.Add((0, 25), 0, wx.ALL, 0)
		helpsizer.Add(self.chkMatchCase, 0, wx.ALL, 0)
		helpsizer.Add((0, 5), 0, wx.ALL, 0)
		helpsizer.Add(self.chkSubDirectories, 0, wx.ALL, 0)
		helpsizer.Add((0, 30), 0, wx.ALL, 0)
		helpsizer.Add(btn2above, 0, wx.ALL, 0)
		helpsizer.Add((0, 10), 0, wx.ALL, 0)
		helpsizer.Add(btn1right, 0, wx.ALL, 0)

		stat1 = wx.StaticText(self, -1, "Directory:")
		stat2 = wx.StaticText(self, -1, "File Pattern:")
		stat3 = wx.StaticText(self, -1, "Search For:")
		text1 = wx.ComboBox(self, -1, "", wx.DefaultPosition, (300,-1))
		text2 = wx.ComboBox(self, -1, "")
		text3 = wx.ComboBox(self, -1, "")

		topsizer = wx.FlexGridSizer(2,2,5,5)
		topsizer.AddGrowableCol(1)
		topsizer.Add(stat1,0)
		topsizer.Add(text1,1,wx.GROW)
		topsizer.Add(stat2,0)
		topsizer.Add(text2,1,wx.GROW)
		topsizer.Add(stat3,0)
		topsizer.Add(text3,1,wx.GROW)

		leftSizer = wx.BoxSizer(wx.VERTICAL)
		leftSizer.Add(topsizer,0, wx.EXPAND | wx.ALL, 5)
		leftSizer.Add(lst,1, wx.EXPAND | wx.ALL, 5)
		
		newSizer = wx.BoxSizer(wx.HORIZONTAL)
		newSizer.Add(leftSizer,1, wx.EXPAND | wx.ALL, 10)
		newSizer.Add(helpsizer,0, wx.ALIGN_TOP | wx.ALL, 10)
		lastSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(newSizer)

		self.Fit()
		self.Show()
		
app = wx.PySimpleApp()
Panel = MyFrame(None, -1, "Find Files")

app.MainLoop()

