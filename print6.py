#! /usr/bin/env python

import wx
print(wx.version())
import sys

#---------------------------------------------------------------------------


def RunTest(panel,frame):
    pd = wx.PrintData()
    pdd = wx.PrintDialogData()
    pdd.SetPrintData(pd)
    printer = wx.Printer(pdd)
    printout = MyPrintout()
    printout2 = MyPrintout()

    preview = wx.PrintPreview(printout, printout2)
    preview.SetZoom(90)
    if not preview.Ok():
        print('preview error')
        return
    frame2 = wx.PreviewFrame(preview, frame, "This is a print preview")
    frame2.Initialize()
    frame2.SetPosition(frame.GetPosition())
    frame2.SetSize(frame.GetSize())
    wx.CallAfter(frame2.Show, True)

#----------------------------------------------------------------------


class MyPrintout(wx.Printout):
    def __init__(self, canvas=None):
        wx.Printout.__init__(self)
        self.end_pg = 1

    def OnBeginDocument(self, start, end):
        return wx.Printout.OnBeginDocument(self, start, end)

    def OnEndDocument(self):
        wx.Printout.OnEndDocument(self)

    def HasPage(self, page):
        return (page <= self.end_pg)

    def GetPageInfo(self):
        return (1, 1, 1, 1)

    def OnPreparePrinting(self):
        wx.Printout.OnPreparePrinting(self)

    def OnBeginPrinting(self):
        wx.Printout.OnBeginPrinting(self)

    def OnPrintPage(self, page):
        dc = self.GetDC()
        if self.IsPreview():
            print("in previewmode")
        else:
            print("in printing mode")
        PPI = dc.GetPPI()
        print("PPI=", PPI)
        print(repr(PPI))

        ## fixme: this shouldn't be hardcoded here
        topmargin, leftmargin = 1, 1 # inches
        topmargin, leftmargin = topmargin*PPI[1], leftmargin*PPI[1] #(convert to pixels)
        ##if self.IsPreview():
##            font = dc.GetFont()
##            print "In preview: fontsize:",font.GetPointSize()  # linux=10, MSW crashes, but I think it is 16
##        else:
##            font = dc.GetFont()
##            print "In print: fontsize:",font.GetPointSize()  # linux=10, MSW crashes, but I think it is 16
##            if sys.platform == 'win32':
##                point = 32  # trial and error !!!
##            else:
##                point = 12  #      ditto
        point = 12
        font = wx.Font(point, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        height = dc.GetTextExtent('X')[1]
        print("TextExtent", dc.GetTextExtent('X'))

        lineskip = 1.2 * height
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        height = dc.GetTextExtent('X')[1]
        line = 0
        dc.DrawText('This is a heading '+sys.platform,leftmargin,topmargin+int(line*lineskip))
        font.SetWeight(wx.FONTWEIGHT_LIGHT)
        dc.SetFont(font)
        line = 2
        dc.DrawText('This is a detail line wxMODERN',leftmargin,topmargin+int(line*lineskip))
        line = 3
        dc.DrawText('This is another detail line',leftmargin,topmargin+int(line*lineskip))
        font.SetUnderlined(True)  # only works with MSW and PS!
        dc.SetFont(font)
        line = 5
        dc.DrawText('This is a total line',leftmargin,topmargin+int(line*lineskip))

        return True

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, frame):
        wx.Panel.__init__(self, frame, -1)
        RunTest(self, frame)

#----------------------------------------------------------------------

class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, -1, "Printing test", size=(530, 400),
                        style=wx.NO_FULL_REPAINT_ON_RESIZE | wx.DEFAULT_FRAME_STYLE)
        self.frame = frame
        frame.CreateStatusBar()
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(101, "E&xit\tAlt-X", "Exit demo")
        self.Bind(wx.EVT_MENU, self.OnButton, id=101)
        menuBar.Append(menu, "&File")
        frame.SetMenuBar(menuBar)
        win = TestPanel(frame)
        frame.CentreOnScreen()
        frame.Show(True)
        self.SetTopWindow(frame)

        return True

    def OnButton(self, evt):
        self.frame.Close(True)


if __name__ == '__main__':
    app = App(0)
    app.MainLoop()
