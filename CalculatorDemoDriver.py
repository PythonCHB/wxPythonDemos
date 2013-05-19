#!/usr/bin/env python
 
"""
demo of how to drive a wxPython app from another script:

one thread to do the driving, one thread to run the Calculator:

the primary thread runs the GUI - - it gets "locked up" with the mainloop.

the secondary thread i used to do things in a way outside the GUI. In this
case, a simple pause and sending commands now and then. The commands are put
on the event loop with a wx.CallAfter() call.

"""

import threading

import wx

import CalculatorDemo

class GUI_Thread(threading.Thread):
    """
    class to create a thread to run the GUI in 
    
    this should allow the command line to stay active in the main thread,
    while the mainloop is running in this thread.
    
    """
    def run(self):
        """
        run starts up mainloop of the wx.App
        """
        #Create the application
        self.app = wx.App(False)
        self.calculator = CalculatorDemo.Calculator()
        self.calculator.Show()
        self.app.MainLoop()
        

# create and start the thread for the GUI
gui_thread = GUI_Thread()
gui_thread.start()

# now we have control back -- start a loop for user input
print "enter expressions to calcualte: enter to evaluate"
print "hit ctrl+C to exit"
while True:
    expr = raw_input()
    # send the input to the calculator to calculate
    gui_thread.calculator.ComputeExpression(expr)
    

