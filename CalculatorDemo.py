#!/usr/bin/env python

"""
wxPython Calculator Demo in 50 lines of code

This demo was pulled form teh wxPython Wiki:

http://wiki.wxpython.org/CalculatorDemo
by  Miki Tebeka

It has been altered to allow it to be "driven" by an external script,
plus a little layout improvement

See CalcualtorDemoDriver.py 

for an example
"""


# Calculator GUI:

# ___________v
# [7][8][9][/] 
# [4][5][6][*]
# [1][2][3][-]
# [0][.][C][+]
# [    =     ]

from __future__ import division # So that 8/3 will be 2.6666 and not 2
import wx
from math import * # So we can evaluate "sqrt(8)"

class Calculator(wx.Frame):
    '''Main calculator dialog'''
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, title="Calculator")
        sizer = wx.BoxSizer(wx.VERTICAL) # Main vertical sizer

        self.display = wx.ComboBox(self, -1) # Current calculation
        sizer.Add(self.display, 0, wx.EXPAND) # Add to main sizer

        # [7][8][9][/] 
        # [4][5][6][*]
        # [1][2][3][-]
        # [0][.][C][+]
        gsizer = wx.GridSizer(4, 4, 8, 8)
        for row in (("7", "8", "9", "/"),
                    ("4", "5", "6", "*"),
                    ("1", "2", "3", "-"),
                    ("0", ".", "C", "+")):
            for label in row:
                b = wx.Button(self, label=label, size=(40,-1))
                gsizer.Add(b)
                b.Bind(wx.EVT_BUTTON, self.OnButton)
        sizer.Add(gsizer, 1, wx.EXPAND)

        # [    =     ]
        b = wx.Button(self, label="=")
        b.Bind(wx.EVT_BUTTON, self.OnButton)
        sizer.Add(b, 0, wx.EXPAND|wx.ALL, 8)
        self.equal = b

        # Set sizer and center
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.CenterOnScreen()

    def OnButton(self, evt):
        '''Handle button click event'''
        
        # Get title of clicked button
        label = evt.GetEventObject().GetLabel()

        if label == "=": # Calculate
            self.Calculate()
        elif label == "C": # Clear
            self.display.SetValue("")

        else: # Just add button text to current calculation
            self.display.SetValue(self.display.GetValue() + label)
            self.equal.SetFocus() # Set the [=] button in focus

    def Calculate(self):
        """
        do the calculation itself
        
        in a separate method, so it can be called outside of a button event handler
        """
        try:
            compute = self.display.GetValue()
            # Ignore empty calculation
            if not compute.strip():
                return

            # Calculate result
            result = eval(compute)

            # Add to history
            self.display.Insert(compute, 0)

            # Show result
            self.display.SetValue(str(result))
        except Exception, e:
            wx.LogError(str(e))
            return

    def ComputeExpression(self, expression):
        """
        Compute the expression passed in.
        
        This can be called from another class, module, etc.
        """
        self.display.SetValue(expression)
        self.Calculate()

if __name__ == "__main__":
    # Run the application
    app = wx.App(False)
    frame = Calculator(None)
    frame.Show()
    app.MainLoop()