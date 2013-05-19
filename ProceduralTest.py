#!/usr/bin/env python

"""

This is a little script that tried to demonstrate a simple "procedural"
program using wxPython. The goal is to have a script that runs through a
few questions for the user, popping up dialogs as it goes, but without a
main frame, and all the baggage that usually comes with writing a full,
event drive app.

"""

import wx

from sys import exit

## Here's an example of a custom dialog with no parent
class MyCheckDialog(wx.Dialog):
    def __init__(self, Choices):
        wx.Dialog.__init__(self, None, -1, 'wxDialog')
        self.Choices = Choices 

        self.clb = wx.CheckListBox(self, -1, wx.DefaultPosition, wx.DefaultSize, self.Choices)

        ok = wx.Button(self, wx.ID_OK, 'Ok')
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.clb, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(ok, 0, wx.ALIGN_RIGHT|wx.ALL^wx.TOP, 5)
        self.SetSizer(sizer)
        
        self.Center() # make it come up on the center of the screen

    def GetChecked(self):
        Checked = []
        for (index, item) in enumerate(self.Choices):
            if self.clb.IsChecked(index):
                Checked.append(item)
        return Checked

# You could put some code here, to run before initializing wx.

# you need to start by initializing a wxApp
app = wx.App(False)


## now you can run your script, bringing  up various dialogs.

fd = wx.FileDialog(None,"Pick a File")
if fd.ShowModal() != wx.ID_OK:
    exit(1)
else:
    print "You choose the file: ", fd.GetFilename()

md = wx.MessageDialog(None, 'Continue?')
if md.ShowModal() != wx.ID_OK:
    exit(1)
else:
    print "You chose to continue"

scd = wx.SingleChoiceDialog(None, 'Pick One',
                            'A Single Choice Dialog',
                            ['single', 'choice', 'dialog','with','some','choices'])
if scd.ShowModal() != wx.ID_OK:
    exit(1)
else:
    print "You chose:", scd.GetStringSelection()

# now lets get some input on the command line:
I = raw_input("type something here >>")
print "You typed:", I


myd = MyCheckDialog(['check', 'list', 'box', 'another'])
if myd.ShowModal() != wx.ID_OK:
    exit(1)
else:
    print "You checked:", myd.GetChecked()

