#!/usr/bin/env python2.4

"""

This is a module that provides a PyBoxSizer class, that is more
pythonic than the raw wxWidgets interface.

"""

import wx

class PyBoxSizer(wx.BoxSizer):
    """
    PyBoxSizer class, that is more pythonic than the raw wxWidgets
    interface.

    The Add() method takes these parameters:

    Widget:  could be a wxWindow, wxSizer, or (x,y) spacer tuple
    AlignmentVertical = wx.CENTER:  could be wxCENTER, wxTOP, wxBOTTOM
    AlignmentHorizontal = wx.CENTER:  could be:wxCENTER, wxRIGHT, wxLEFT
    StretchFactorVertical = 0:  any integer >=0
    StretchFactorHorizontal = 0:  any integer >=0
    Borders = wx.ALL,# could be wxTOP, wxBOTTOM, wxLEFT, wxRIGHT or wxALL
    BorderSize = 0:  any integer >= 0
    ExtraFlags = wx.ADJUST_MINSIZE): # other flags, such as wxADJUST_MINSIZE


    """
    def __init__(self, orient):
         wx.BoxSizer.__init__(self, orient)

         self.orient = orient
         self.OldAdd = self.Add
         self.Add = self.PyAdd

    def PyAdd(self,
            Widget, # could be a wxWindow, wxSizer, or (x,y) spacer tuple
            AlignmentVertical = wx.CENTER, # could be wxCENTER, wxTOP, wxBOTTOM
            AlignmentHorizontal = wx.CENTER, # could be:wxCENTER, wxRIGHT, wxLEFT
            StretchFactorVertical = 0, # any integer >=0
            StretchFactorHorizontal = 0, # any integer >=0
            Borders = wx.ALL,# could be wxTOP, wxBOTTOM, wxLEFT, wxRIGHT or wxALL
            BorderSize = 0, # any integer >= 0
            ExtraFlags = wx.ADJUST_MINSIZE): # other flags, such as wxADJUST_MINSIZE

        flags = 0

        if self.orient == wx.VERTICAL:
            proportion = StretchFactorVertical
            if StretchFactorHorizontal > 0:
                flags = flags | wx.GROW
        elif self.orient == wx.HORIZONTAL:
            proportion = StretchFactorHorizontal
            if StretchFactorVertical > 0:
                flags = flags | wx.GROW

        if AlignmentVertical == wx.CENTER:
            flags |= wx.ALIGN_CENTER_VERTICAL
        elif AlignmentVertical == wx.TOP:
            flags |= wx.ALIGN_TOP
        elif AlignmentVertical == wx.BOTTOM:
            flags |= wx.ALIGN_BOTTOM

        if AlignmentHorizontal == wx.CENTER:
            flags |= wx.ALIGN_CENTER_HORIZONTAL
        elif AlignmentHorizontal == wx.LEFT:
            flags |= wx.ALIGN_LEFT
        elif AlignmentHorizontal == wx.RIGHT:
            flags |= wx.ALIGN_RIGHT

        flags |= Borders
        flags |= ExtraFlags  

        print "Calling old Add:", (proportion, flags, BorderSize)
        self.OldAdd(Widget, proportion, flags, BorderSize)
     
class MyDialog(wx.Dialog):

    """
    A simple app to test the new sizer API
	
    """
    
    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
	
        # Create a vertical BoxSizer for the Main Sizer
        topsizer = PyBoxSizer( wx.VERTICAL )

        # Create text ctrl with minimum size 100x60
        textBox = wx.TextCtrl(self,
                             value="My text.",
                             size=(300,100),
                             style=wx.TE_MULTILINE)

        # Add the text control
        topsizer.Add(textBox,
                     AlignmentVertical = wx.CENTER,
                     AlignmentHorizontal = wx.CENTER,
                     StretchFactorVertical = 1,
                     StretchFactorHorizontal = 1,
                     Borders = wx.ALL,
                     BorderSize = 10,
                     ExtraFlags = wx.ADJUST_MINSIZE)
        
        # Create a Horizontal Sizer for the Buttons
        button_sizer = PyBoxSizer(wx.HORIZONTAL)
        button_sizer.Add(wx.Button(self, wx.ID_OK),
                         Borders=wx.ALL,
                         BorderSize=10 )
        button_sizer.Add(wx.Button(self, wx.ID_CANCEL),
                         Borders=wx.ALL,
                         BorderSize=10 )
        
        topsizer.Add(button_sizer, AlignmentHorizontal = wx.RIGHT)
        
        self.SetSizerAndFit(topsizer)

if __name__=='__main__':
    App = wx.App()
    #AppFrame().Show()
    dlg = MyDialog(None, title="Test Dialog", style=wx.RESIZE_BORDER )
    dlg.ShowModal()
    dlg.Destroy()
    App.MainLoop()

