#!/usr/bin/env python

"""
simple example of runnig wxPython in a secondary thread

As of now -- all I get is a crash!

"""

import threading

import wx
import time

import DoubleBufferDemo

class MicroFrame(wx.Frame):
    pass

class MicroApp(wx.App):
    def OnInit(self):
        f = MicroFrame(None, title="threading demo")
        f.Show()
        
        self.startup_event
        return True
        
       
class wxThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
            
        self.startup_event = startup_event = threading.Event()
        
    def run(self):
        print "starting up the wx app"
        self.app = DoubleBufferDemo.DemoApp(False)
        print "app started --- starting the mainloop"
        self.startup_event.set()
        self.app.MainLoop()

if __name__ == "__main__":

    wxt = wxThread()
    startup_event = wxt.startup_event
    wxt.start()
    print "thread started..."

    # wait for the wx.Frame to be created
    startup_event.wait()
    frame = wxt.app.frame
    # run an endless loop to do re-draw...
    while True:
        time.sleep(0.5)
        print "another moment passed..."
        frame.NewDrawing()

