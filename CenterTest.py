#!/usr/bin/env python

import wx

class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Hello")
        b.Bind(wx.EVT_BUTTON, self.OnClick)
        # the Bind() method removes the need to keep track of IDs

        Sizer = wx.BoxSizer(wx.VERTICAL)
        ## by adding a stretchable spacer above and below, you get the
        ## button centered.
        Sizer.Add((1,1), 1) ## this adds a 1X1 pixel spacer
                            ## but the "1" means that it has a stretch factor of 1
        Sizer.Add(b, 0, wx.ALIGN_CENTER) # the "0" means it won't stretch
        Sizer.Add((1,1), 2) # same as above
        # try changing the stretch factors, and see what you get.

        self.SetSizer(Sizer)

    def OnClick(self, event):
        msgdialog = wx.MessageDialog(self,"HELLO WHIRLED",style=wx.OK)
        msgdialog.ShowModal()

class MyFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='Wombat',
                 pos=wx.DefaultPosition, size=(200, 200)):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        panel = MyPanel(self)

class App(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Center()
        frame.Show()
        self.SetTopWindow(frame)
        return True

def main():
    app = App()
    app.MainLoop()

if __name__ == '__main__':
    main()
