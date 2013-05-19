#!/usr/bin/env python

import wx, random

class MainWindow(wx.Frame):
    """ This window displays a button """
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self, None, -1, "Blit Test",
                         wx.DefaultPosition,
                         size=(500,500),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        wx.EVT_CLOSE(self,self.OnQuit)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_SIZE, self.BuildImage)

        self.Numtimer = 0
        self.NumLines = 100

        self.t=wx.Timer(self)
        self.BuildImage()
        self.t.Start(100)
        
    def OnQuit(self,Event):
        self.Destroy()

    def BuildImage(self, event = None):
        Size  = self.GetClientSizeTuple()

        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        print "making new buffer:",Size
        self._Buffer = wx.EmptyBitmap(Size[0],Size[1])

        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)


        self.Lines = []
        for i in range(self.NumLines):
            x1,y1,x2,y2 = (random.randint(1,max(Size)),
                           random.randint(1,max(Size)),
                           random.randint(1,max(Size)),
                           random.randint(1,max(Size)))
            
            color = self.random_color()
            self.Lines.append( [color, (x1,y1,x2,y2)] )
        
        dc.BeginDrawing()
        dc.Clear()
        for line in self.Lines:
            dc.SetPen(wx.Pen(line[0], 2))
            dc.DrawLine(*line[1])
        dc.EndDrawing()

    def OnTimer(self,event):
        self.Numtimer += 1
        print "Timer fired: %i times"%self.Numtimer

        # change one color:
        self.Lines[random.randrange(self.NumLines)][0] = self.random_color()
        # update the screen
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        dc.BeginDrawing()
        dc.Clear()
        for line in self.Lines:
            dc.SetPen(wx.Pen(line[0], 2))
            dc.DrawLine(*line[1])
        dc.EndDrawing()
        del dc
        wx.ClientDC(self).DrawBitmap(self._Buffer,0,0)
        
    def random_color(self):
        return apply(wx.Colour,(random.randrange(255),random.randrange(255),random.randrange(255)))


class MyApp(wx.App):
    def OnInit(self):

        frame = MainWindow(None, -1, "BlitTest")
        self.SetTopWindow(frame)
        frame.Show()
        
        return True
        

app = MyApp(0)
app.MainLoop()





