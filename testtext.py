#!/usr/bin/env python2.3

from wxPython.wx import *
from   wxPython.html       import *

#-------------------------------------------------------------------

class MyPanel(wxPanel):   

    def __init__(self, parent, id):
        wxPanel.__init__(self, parent, id, wxDefaultPosition, wxDefaultSize)

        sty = wxTE_MULTILINE | wxTE_RICH2 | wxTE_DONTWRAP | wxHSCROLL
        self.tc = wxTextCtrl(self, -1, '', (8, 8), wxSize(300, 200), sty)
        attrib1 = wxTextAttr('RED', 'WHITE', wxFont(12, wxMODERN, wxNORMAL, wxNORMAL))
        attrib2 = wxTextAttr('BLACK', 'WHITE', wxFont(12, wxROMAN, wxNORMAL, wxNORMAL))
        attrib3 = wxTextAttr('BLACK', 'WHITE', wxFont(12, wxSWISS, wxNORMAL, wxBOLD))
        self.tc.SetDefaultStyle(attrib1)
        self.tc.AppendText("This is a line of text\n")
        self.tc.AppendText("This is another line of text\n")
        self.tc.SetDefaultStyle(attrib2)
        self.tc.AppendText("This is a third line of text\n")
        self.tc.SetDefaultStyle(attrib3)
        self.tc.AppendText("This is a fourth line of text\n")

        self.Html = wxHtmlWindow(self, -1 , (8, 220), wxSize(300, 200),wxNO_FULL_REPAINT_ON_RESIZE )
        text = """
        <html><body><tt>
        <pre>
This is a line of text<br>
This is another line of text<br>
This is a third line of text<br>
This is a fourth line of text<br>
123  456  56  3432<br>
 34   32 123    34<br>
         </pre>
        </tt>
        </body></html>"""
        self.Html.SetPage(text)
        
#-------------------------------------------------------------------

class MyFrame(wxFrame):

    def __init__(self, parent, id):
        title = 'atextctrl'
        style = wxSYSTEM_MENU | wxCAPTION | wxMINIMIZE_BOX
        wxFrame.__init__(self, parent, id, title, wxPoint(0, 0),
                            wxSize(350, 500), style)
        self.panel = MyPanel(self, -1)

#-------------------------------------------------------------------

class MyApp(wxApp):

    def OnInit(self):
        frame = MyFrame(None, -1)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

#-------------------------------------------------------------------

def main():
    app = MyApp(0)
    app.MainLoop()

#-------------------------------------------------------------------

if __name__ == "__main__" :
    main()

#eof-------------------------------------------------------------------
