#!/usr/bin/env python2.4

import wx

StockCursors = [("ARROW",wx.CURSOR_ARROW),
                ("RIGHT_ARROW",wx.CURSOR_RIGHT_ARROW),
                ("BLANK",wx.CURSOR_BLANK),
                ("BULLSEYE",wx.CURSOR_BULLSEYE),
                ("CHAR",wx.CURSOR_CHAR),
                ("CROSS",wx.CURSOR_CROSS),
                ("HAND",wx.CURSOR_HAND),
                ("IBEAM",wx.CURSOR_IBEAM),
                ("LEFT_BUTTON",wx.CURSOR_LEFT_BUTTON),
                ("MAGNIFIER",wx.CURSOR_MAGNIFIER),
                ("MIDDLE_BUTTON",wx.CURSOR_MIDDLE_BUTTON),
                ("NO_ENTRY",wx.CURSOR_NO_ENTRY),
                ("PAINT_BRUSH",wx.CURSOR_PAINT_BRUSH),
                ("PENCIL",wx.CURSOR_PENCIL),
                ("POINT_LEFT",wx.CURSOR_POINT_LEFT),
                ("POINT_RIGHT",wx.CURSOR_POINT_RIGHT),
                ("QUESTION_ARROW",wx.CURSOR_QUESTION_ARROW),
                ("RIGHT_BUTTON",wx.CURSOR_RIGHT_BUTTON),
                ("SIZENESW",wx.CURSOR_SIZENESW),
                ("SIZENS",wx.CURSOR_SIZENS),
                ("SIZENWSE",wx.CURSOR_SIZENWSE),
                ("SIZEWE",wx.CURSOR_SIZEWE),
                ("SIZING",wx.CURSOR_SIZING),
                ("SPRAYCAN",wx.CURSOR_SPRAYCAN),
                ("WAIT",wx.CURSOR_WAIT),
                ("WATCH",wx.CURSOR_WATCH),
                ("ARROWWAIT",wx.CURSOR_ARROWWAIT),
                ]

MyCursors = [("My ZoomIn", "MagPlus.png"),
             ("My Move", "MoveButton.png")
             ]

class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self,title = "Cursor Test"):
        wx.Frame.__init__(self,None ,-1,title)#,size = (800,600),style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        self.TestPanel = wx.Panel(self, -1, size = (400,400))
        self.TestPanel.SetBackgroundColour("Blue")
        self.ButtonPanel = ButtonPanel(self)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(self.TestPanel, 1, wx.GROW)
        Sizer.Add(self.ButtonPanel, 1, wx.GROW)
        self.SetSizerAndFit(Sizer)
        self.Fit()

    def OnSetCursor(self, Cursor):
        self.TestPanel.SetCursor(Cursor)
      
        
    def OnQuit(self,Event):
        self.Destroy()

class ButtonPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        #NumButtons = Len(CursorList)
        NumColumns = 5.0
        #NumRows = math.ceil(NumButtons/NumColumns)
        Sizer = wx.GridSizer(0, NumColumns)
        self.Cursors = {}
        for name, Cursor in StockCursors:
            print Cursor
            try:
                self.Cursors[name] = wx.StockCursor(Cursor)
                B = wx.Button(self, -1, name)
                B.Bind(wx.EVT_BUTTON, self.OnButton)
                Sizer.Add(B, 1, wx.GROW | wx.ALL, 2 )
            except:
                print "Cursor:", name,"Doesn't exist."
        for name, filename in MyCursors:
            self.Cursors[name] = wx.CursorFromImage(wx.Image(filename))
            B = wx.Button(self, -1, name)
            B.Bind(wx.EVT_BUTTON, self.OnButton)
            Sizer.Add(B, 1, wx.GROW | wx.ALL, 2 )
            
        self.SetSizerAndFit(Sizer)

        self.ParentFrame = parent

    def OnButton(self, event):
        name =  event.GetEventObject().GetLabel()
        print name
        self.ParentFrame.OnSetCursor(self.Cursors[name])
        

app = wx.PySimpleApp(0)
frame = DemoFrame()
frame.Show()
app.MainLoop()





