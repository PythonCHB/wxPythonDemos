#!/usr/bin/env python2.5

"""
A demo and test of how to make a poopup menu that is customized to when
it is called

"""
 
import wx


class MyPopupMenu(wx.Menu):
    def __init__(self, WinName):
        wx.Menu.__init__(self)

        self.WinName = WinName
    
        # Binding the conventional way:
        item = wx.MenuItem(self, wx.NewId(),"Item One")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnItem1, item)

        item = wx.MenuItem(self, wx.NewId(),"Item Two")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnItem2, item)

        #Generate a bunch of menu items programatically with the "lambda+keyword trick"
        for name in ["Item Three", "Item Four"]:
            item = wx.MenuItem(self, wx.NewId(), name)
            self.AppendItem(item)
            self.Bind(wx.EVT_MENU, lambda event, name=name: self.OnItems(event, name), item)

    def OnItem1(self, event):
        print "Item One selected in the %s window"%self.WinName

    def OnItem2(self, event):
        print "Item Two selected in the %s window"%self.WinName

    def OnItems(self, event, name):
        print "%s selected in the %s window"%(name, self.WinName)


class MyWindow(wx.Window):
    def __init__(self, parent, color):
        wx.Window.__init__(self, parent, -1)


        self.color = color

        self.SetBackgroundColour(color)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        
    def OnRightDown(self,event):
        menu = MyPopupMenu(self.color)
        self.PopupMenu(menu, event.GetPosition())
        # the menu needs to be destroyed when you're done with it, or it will
        # hang around forever, and you'll create a new one each time this is called!
        menu.Destroy()

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None, -1, "Test", size=(300, 200))

        sizer = wx.GridSizer(2,2,5,5)

        sizer.Add(MyWindow(self,"blue"),1,wx.GROW)
        sizer.Add(MyWindow(self,"yellow"),1,wx.GROW)
        sizer.Add(MyWindow(self,"red"),1,wx.GROW)
        sizer.Add(MyWindow(self,"green"),1,wx.GROW)

        self.SetSizer(sizer)

        self.Show()


app = wx.App(False)
frame = MyFrame()
app.SetTopWindow(frame)
app.MainLoop()

