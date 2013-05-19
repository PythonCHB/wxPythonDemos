#!/usr/bin/env python

'''
"lambda trick" test

A demo of a way to pass extra args in to callback
good for generating multiple gui items o code.

Use the menu to test it out!

'''

import wx

class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)


        MenuBar = wx.MenuBar()
        TestMenu = wx.Menu()
        
        # build menu from data:
        menu_names = ['item 1', 'item 2', 'item 3']
        
        for name in menu_names:
            item = TestMenu.Append(wx.ID_ANY, text = name)
            self.Bind(wx.EVT_MENU,
                      (lambda evt, name = name: 
                       self.onMenuSelect(evt, name) ),
                       item)
        MenuBar.Append(TestMenu , "&Test")

        self.SetMenuBar(MenuBar)

    def onMenuSelect(self, evt, menu_name):
        print "Menu: %s was selected"%menu_name

A = wx.App(False)
F = TestFrame(None)
F.Show()
A.MainLoop()



