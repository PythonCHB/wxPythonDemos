#! /usr/bin/env python2.4
import wxPython
from wxPython.wx import *
print wxPython.__version__
import sys

#---------------------------------------------------------------------------

def RunTest(panel,frame):
    pd = wxPrintData()
    pdd = wxPrintDialogData()
    pdd.SetPrintData(pd)
    printer = wxPrinter(pdd)
    printout = MyPrintout()
    printout2 = MyPrintout()

    preview = wxPrintPreview(printout, printout2)
    if not preview.Ok():
        print 'preview error'
        return
    frame2 = wxPreviewFrame(preview, frame, "This is a print preview")
    frame2.Initialize()
    frame2.SetPosition(frame.GetPosition())
    frame2.SetSize(frame.GetSize())
    wxCallAfter(frame2.Show,true)

#----------------------------------------------------------------------

class MyPrintout(wxPrintout):
    def __init__(self, canvas=None):
        wxPrintout.__init__(self)
        self.end_pg = 1

    def OnBeginDocument(self, start, end):
        return self.base_OnBeginDocument(start, end)

    def OnEndDocument(self):
        self.base_OnEndDocument()

    def HasPage(self, page):
        return (page <= self.end_pg)

    def GetPageInfo(self):
        return (1,1,1,1)

    def OnPreparePrinting(self):
        self.base_OnPreparePrinting()

    def OnBeginPrinting(self):
        self.base_OnBeginPrinting()

    def OnPrintPage(self, page):
        dc = self.GetDC()
        if self.IsPreview():
            print "in previewmode"
        else:
            print "in printing mode"
        PPI = dc.GetPPI()
        print "PPI=", PPI
        print repr(PPI)

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
        font = wxFont(point,wxMODERN,wxNORMAL,wxNORMAL)
        dc.SetFont(font)
        height = dc.GetTextExtent('X')[1]
        print "TextExtent", dc.GetTextExtent('X')

        lineskip = 1.2*height
        font.SetWeight(wxBOLD)
        dc.SetFont(font)
        height = dc.GetTextExtent('X')[1]
        line = 0
        dc.DrawText('This is a heading '+sys.platform,leftmargin,topmargin+int(line*lineskip))
        font.SetWeight(wxLIGHT)
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

class TestPanel(wxPanel):
    def __init__(self, frame):
        wxPanel.__init__(self, frame, -1)
        RunTest(self,frame)

#----------------------------------------------------------------------

class App(wxApp):
    def OnInit(self):
        wxInitAllImageHandlers()
        frame = wxFrame(None, -1, "Printing test", size=(530,400),
                        style=wxNO_FULL_REPAINT_ON_RESIZE|wxDEFAULT_FRAME_STYLE)
        self.frame = frame
        frame.CreateStatusBar()
        menuBar = wxMenuBar()
        menu = wxMenu()
        menu.Append(101, "E&xit\tAlt-X", "Exit demo")
        EVT_MENU(self, 101, self.OnButton)
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

