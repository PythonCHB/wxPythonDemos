#!/usr/bin/env python

"""
TA simple test app for wxHTML

It provides and easy way to test HTML, and how it is rendered by wxHtml

The wxHtml window automatically updates as you type in the text window.

Also tests printing.

"""

## some sample html to start with
body = ["<font size=%i> <p> text in size %i </p> </font>"%(i,i) for i in [10, 14, 16]]

HTML = """<html><body>

<h1> Header1: Very basic Sample HTML </h1>

<h2> Header 2: a test of fonts...</h2>

<tt>
<p> text default size</p>
<font size=10> <p> text in size 10 </p> </font>
<font size=16> <p> text in size 16 </p> </font>
</tt>

<h3> Header 3: a test of subscripts</h3>

H<sub>2</sub>O

<h4>Header 4:</h4>
<h5>Header 5:</h5>
<h6>Header 6:</h6>

</body></html>

"""

import wx
import wx.html

#-------------------------------------------------------------------


class MyHTMLWindow(wx.html.HtmlWindow):
    """
    Not much need for a class here -- but maybe they'll be moreto add later
    """
    def __init__(self, parent):
        wx.html.HtmlWindow.__init__(self, parent,
                                    style=wx.VSCROLL|wx.ALWAYS_SHOW_SB)

        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()
        self.Show()


class MyFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        title = 'wxHtml Tester'
        wx.Frame.__init__(self, *args, **kwargs)
        self.htwindow = MyHTMLWindow(self)

        self.InputWindow = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.InputWindow.SetFont(wx.Font(12,
                                         wx.FONTFAMILY_TELETYPE,
                                         wx.FONTSTYLE_NORMAL,
                                         wx.FONTWEIGHT_NORMAL))
        self.InputWindow.Value = HTML
        self.InputWindow.Bind(wx.EVT_TEXT, self.OnTextChanged)

        # lay out the frame
        S = wx.BoxSizer(wx.HORIZONTAL)
        S.Add(self.InputWindow, 3, wx.EXPAND)
        S.Add(self.htwindow, 4, wx.EXPAND)

        self.Printer = wx.html.HtmlEasyPrinting()

        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        item = FileMenu.Append(wx.ID_EXIT, text = "&Exit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        item = FileMenu.Append(wx.ID_PRINT, text = "&Print")
        self.Bind(wx.EVT_MENU, self.OnPrint, item)
        item = FileMenu.Append(wx.ID_PRINT, text = "Print P&review")
        self.Bind(wx.EVT_MENU, self.OnPreview, item)
        MenuBar.Append(FileMenu, "&File")

        self.SetMenuBar(MenuBar)

        self.SetSizerAndFit(S)
        wx.CallAfter(self.OnTextChanged)

    def OnTextChanged(self, evt=None):
        """
        Updates the HTML: called whenever there is a change in the input
            text field.

        Keeps the HtmlWindow scrolled to the same position as it was
        """
        pos = self.htwindow.GetViewStart()
        self.htwindow.Freeze()
        self.htwindow.SetPage(self.InputWindow.Value)
        self.htwindow.Scroll(*pos)
        self.htwindow.Thaw()

    def OnPrint(self, evt=None):
        self.Printer.PrintText(self.InputWindow.Value, "HTML tester")

    def OnPreview(self, evt=None):
        self.Printer.PreviewText(self.InputWindow.Value)

    def OnQuit(self,Event):
        self.Destroy()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title="HTML Tester Window", size=(600, 500))
        self.SetTopWindow(frame)
        frame.Size = (900, 500)
        frame.Centre()
        frame.Show(True)
        return True


if __name__ == "__main__" :
    app = MyApp(0)
    app.MainLoop()
