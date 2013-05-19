#!/usr/bin/env python2.5


import wx

class Panel1(wx.Panel):
	def __init__(self, parent, id):
		print "Panel1 being initialized"
		
		wx.Panel.__init__(self, parent, id)

		topSizer = wx.BoxSizer(wx.VERTICAL)

		header = wx.StaticText(self, -1, 'First Panel')
		topSizer.Add(header, 0, wx.ALIGN_CENTER|wx.ALL, 3)

		button = wx.Button(self, -1, ' Next Panel ', wx.DefaultPosition, wx.Size(-1, 32))
		self.Bind(wx.EVT_BUTTON, self.Click, button)

		topSizer.Add((1, 13), 0, wx.ALIGN_CENTER)
		topSizer.Add(button, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.LEFT, 60)
		topSizer.Add((1, 13), 0, wx.ALIGN_CENTER)

		footer = wx.StaticText(self, -1, 'First Panel')
		topSizer.Add(footer, 0, wx.ALIGN_CENTER|wx.ALL, 3)

		self.SetSizer(topSizer)
		self.Fit()

	def Click(self, event):
		self.GetParent().ChangePanel()

class Panel2(wx.Panel):
	def __init__(self, parent, id):
		print "Panel2 being initialized"
		wx.Panel.__init__(self, parent, id)

		topSizer = wx.BoxSizer(wx.HORIZONTAL)
		topSizer.Add((20, 20), 0, wx.ALIGN_CENTER|wx.ALL, 3)

		leftText = wx.StaticText(self, -1, 'Second\n  Panel')
		topSizer.Add(leftText, 0, wx.ALIGN_CENTER|wx.ALL, 3)

		button = wx.Button(self, -1, ' Next Panel ', wx.DefaultPosition, wx.Size(-1, 32))
		self.Bind(wx.EVT_BUTTON, self.Click, button)

		topSizer.Add((20, 20), 0, wx.ALIGN_CENTER|wx.ALL, 3)
		topSizer.Add(button, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 33)
		topSizer.Add((20, 20), 0, wx.ALIGN_CENTER|wx.ALL, 3)
		
		rightText = wx.StaticText(self, -1, 'Second\n  Panel')
		topSizer.Add(rightText, 0, wx.ALIGN_CENTER|wx.ALL, 3)

		topSizer.Add((20, 20), 0, wx.ALIGN_CENTER|wx.ALL, 3)

		self.SetSizer(topSizer)
		self.Fit()

	def Click(self, event):
		self.GetParent().ChangePanel()

class MyFrame(wx.Frame):
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, 'My App')

		self.panel1 = Panel1(self, -1)
		self.panel2 = Panel2(self, -1)
		self.currentPanel = 2

		self.ChangePanel()

		self.Fit()
		self.Show(True)

	def ChangePanel(self):
		if self.currentPanel == 1:
			self.currentPanel = 2
			self.panel1.Hide()
			self.panel2.Show()
		else:
			self.currentPanel = 1
			self.panel2.Hide()
			self.panel1.Show()
		self.Fit()

class MyApp(wx.App):
	def OnInit(self):
		self.frame = MyFrame(None, -1)
		self.SetTopWindow(self.frame)
		return True

def main():
	app = MyApp(0)
	app.MainLoop()

if __name__ == '__main__':
	main()

