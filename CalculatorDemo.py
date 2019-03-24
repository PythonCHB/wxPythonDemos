#!/usr/bin/env python
"""
wxPython Calculator Demo in 50 lines of code

This demo was pulled from the wxPython Wiki:

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

from __future__ import (division, unicode_literals, print_function)
import wx
from math import *  # So we can evaluate "sqrt(8)" and others


class Calculator(wx.Panel):
    '''Main calculator dialog'''

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)  # Main vertical sizer

        self.display = wx.ComboBox(self)  # Current calculation
        sizer.Add(self.display, 0, wx.EXPAND | wx.BOTTOM,
                  8)  # Add to main sizer

        # [7][8][9][/]
        # [4][5][6][*]
        # [1][2][3][-]
        # [0][.][C][+]
        gsizer = wx.GridSizer(4, 4, 8, 8)
        for row in (("7", "8", "9", "/"), ("4", "5", "6", "*"),
                    ("1", "2", "3", "-"), ("0", ".", "C", "+")):
            for label in row:
                b = wx.Button(self, label=label, size=(40, -1))
                gsizer.Add(b)
                b.Bind(wx.EVT_BUTTON, self.OnButton)
        sizer.Add(gsizer, 1, wx.EXPAND)

        # [    =     ]
        b = wx.Button(self, label="=")
        b.Bind(wx.EVT_BUTTON, self.OnButton)
        sizer.Add(b, 0, wx.EXPAND | wx.ALL, 8)
        self.equal = b

        # Set sizer and center
        self.SetSizerAndFit(sizer)

    def OnButton(self, evt):
        '''Handle button click event'''

        # Get title of clicked button
        label = evt.GetEventObject().GetLabel()

        if label == "=":  # Calculate
            self.Calculate()
        elif label == "C":  # Clear
            self.display.SetValue("")

        else:  # Just add button text to current calculation
            self.display.SetValue(self.display.GetValue() + label)
            self.display.SetInsertionPointEnd()
            self.equal.SetFocus()  # Set the [=] button in focus

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
        except Exception as e:
            wx.LogError(str(e))
            return

    def ComputeExpression(self, expression):
        """
        Compute the expression passed in.

        This can be called from another class, module, etc.
        """
        print("ComputeExpression called with:", expression)
        self.display.SetValue(expression)
        self.Calculate()


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('title', "Calculator")
        wx.Frame.__init__(self, *args, **kwargs)

        self.calcPanel = Calculator(self)

        # put the panel on -- in a sizer to give it some space
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(self.calcPanel, 1, wx.GROW | wx.ALL, 10)
        self.SetSizerAndFit(S)
        self.CenterOnScreen()


if __name__ == "__main__":
    # Run the application
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()
