#!/usr/bin/env python

import wx
from wx.html import HtmlEasyPrinting
#import  wx.lib.wxpTag

#-------------------------------------------------------------------


class ExpandButton(wx.BitmapButton):
    """

    This was the first attempt at a button that could be put
    on an html page -- it worked but got ugly
    """
    #DownBmp = wx.Bitmap("Images/ArrowDown.png")
    #RightBmp = wx.Bitmap("Images/ArrowRight.png")

    def __init__(self, *args, **kwargs):

        self.__class__.DownBmp= wx.Bitmap("Images/ArrowDown.png")
        self.__class__.RightBmp = wx.Bitmap("Images/ArrowRight.png")

        self.Section = Sections[kwargs.pop("section")]

        print("Section is:", self.Section)
        kwargs["bitmap"] = self.RightBmp
        wx.BitmapButton.__init__(self, *args, **kwargs)

        self.Section.Expanded = False
        self.Bind(wx.EVT_BUTTON, self.Clicked)

    def Clicked(self, event):
        print("ExpandButton was clicked!")
        if self.Section.Expanded:
            self.Section.Expanded = False
            self.SetBitmapLabel(self.RightBmp)
        else:
            self.Section.Expanded = True
            self.SetBitmapLabel(self.DownBmp)


class HTMLSection:
    def __init__(self, header="", text=""):
        self.header = header
        self.text = text
        self.Expanded = False
        ## fixme - this could be auto-incremented
        self.SectionNum=None

    def OnClick(self):
        if self.Expanded:
            self.Expanded = False
        else:
            self.Expanded = True

    def GetHtml(self):

        html = []
        html.append('\n<A HREF="Section%i"><IMG SRC= '%self.SectionNum )
        if self.Expanded:
            #html.append('"Images/ArrowRight.png"')
            html.append('"Images/Minus.png"')
        else:
            #html.append('"Images/ArrowDown.png"')
            html.append('"Images/Plus.png"')
        html.append(' ALIGN=TEXTTOP> </A>')
        html.append('<font size=+3><b>%s<b></font><br>'%self.header)
        if self.Expanded:
            html.append("\n<P> %s <P>"%self.text)
        return "".join(html)

## Create some fake sections

Sections = []
Sections = [HTMLSection("A Simple Test", """

            This is a test of how to do the expand-contract thing with a
            wx.HtmlWindow

            """),

            HTMLSection("The First approach", """

            I started this out by putting a wx.BitmapButton with the
            arrow on it on the page, and then having it catch the button
            event when it was clicked, and change the arrow, etc.

            <p> Changing the arrow worked well, but:
            having the button know which Section it corresponded
            too, and also having it have a reference to the htmlWindow
            got kind of messy. Also, the button looked kind of out of place on the html
            page, and it didn't print at all.

            <p> Given all that, I tried another approach.

            """),

            HTMLSection("How This Works", """

            This whole system works by putting a small bitmap link in
            the html with the little arrow on it. The href for that link
            is an ID of the section. All clicks on links are
            intercepted, so they can be check to see what section has
            been clicked on. The one that is clicked on then has its
            Expanded flag toggled, and the html for the whole page is
            re-generated.

            <p> When the the html fo rthe whole page is generated, each
            section object is asked for its html. If its Expanded flag
            is set, then it it shows the html for the whole thing. If
            not, then it only shows the littel arrrow and the header
            text.

            """),

            HTMLSection("Still To Do:", """

            This was really just a simple test. I think it shows how it
            can work, but really needs some cleanign up:

            <UL>

            <LI> The HTML is pretty mixed in the with code: maybe useing
            a template system would be better?

            <LI>We could use a better bitmap for the little arrow. It
            should probalby be alligned better. It's now using the
            <pre>ALIGN=TEXTTOP</pre> flag, but that may not be the best
            choice.

            <LI> I'm not sure the best way to get the bitmap loaded,
            either. Right now it points to a file, but that could get
            tricky if we bundle the whole thing up in to a single .exe
            file. Maybe you can load a binary bitmap straight into the
            wx.HtmlWindow, but I don't know how.

            <LI> The code could be cleaned up in other ways too -- like
            how each section gets generated and added.

            </UL>

            """),

            ]
for i, sec in enumerate(Sections):
    sec.SectionNum = i


class Printer(HtmlEasyPrinting):
    def __init__(self):
        HtmlEasyPrinting.__init__(self)


class MyHTMLWindow(wx.html.HtmlWindow):

    def __init__(self, *args, **kwargs):
        wx.html.HtmlWindow.__init__(self, *args, **kwargs)

        self.Printer = HtmlEasyPrinting()
        self.Sections = Sections
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

        self.Header = (
"""
<HTML>
<BODY>
<H1>A very simple HTML page</H1>
<H2>A subheading</H2>
<P>Just a tiny bit of text here</P>
<P><BR>
</P>
<P>now a link: <A HREF="http://Any.link.will.do.com/">http://Any.link.will.do.com</A></P>
<P>And a tiny bit more text.</P>
<P>

""")

        self.Footer ="\n</BODY>\n</HTML>"

        self.Reload()

    def OnLinkClicked(self, linkinfo):
        ##This captures a click on any link:
        linktext = linkinfo.GetHref()

        ## See if it's one of the section expanders
        if linktext.startswith("Section"):
            SecNum = int(linktext[7:])
            self.Sections[SecNum].OnClick()
            self.Reload()

        ## Virtuals in the base class have been renamed with base_ on the front.
        # Use this if you want he usual action
        # self.base_OnLinkClicked(linkinfo)

    def Reload(self):
        HTML = [self.Header]
        for s in self.Sections:
            HTML.append(s.GetHtml())
        HTML.append(self.Footer)
        self.HTML_Code = "\n".join(HTML)
        self.SetPage( self.HTML_Code )

    def Print(self):
        self.Printer.PrintText(self.HTML_Code,"TestHTML")

    def PS_Print(self):
        print("Using PostScriptDC")
        PData = wx.PrintData()
        PData.SetFilename("TestPS.ps")
        DC = wx.PostScriptDC(PData)
        print("PPI", DC.GetPPI())
        ## What to do now?


class MyPanel(wx.Panel):

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        PrintButton = wx.Button(self, label="Print")
        PrintButton.Bind(wx.EVT_BUTTON, self.Print)

        PSPrintButton = wx.Button(self, label="PS-Print")
        PSPrintButton.Bind(wx.EVT_BUTTON, self.PS_Print)


        TopSizer = wx.BoxSizer(wx.HORIZONTAL)
        TopSizer.Add((1,1), 1, wx.GROW)
        TopSizer.Add(PrintButton, 0)
        TopSizer.Add((10,1), 0)
        TopSizer.Add(PSPrintButton, 0)
        TopSizer.Add((1,1), 1, wx.GROW)

        self.Html = MyHTMLWindow(self, size = (400,400), style=wx.VSCROLL|wx.ALWAYS_SHOW_SB)

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        MainSizer.Add(TopSizer, 0, wx.GROW)
        MainSizer.Add(self.Html, 1, wx.GROW)

        self.SetSizerAndFit(MainSizer)

        self.Reload(None)

    def Reload(self,event):
        self.Html.Reload()

    def Print(self,Event):
        self.Html.Print()

    def PS_Print(self,Event):
        self.Html.PS_Print()

#-------------------------------------------------------------------

class MyFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        title = 'wxHtml Tester'
        wx.Frame.__init__(self, *args, **kwargs)
        self.panel = MyPanel(self, -1)
#-------------------------------------------------------------------


class MyApp(wx.App):

    def OnInit(self):
        frame = wx.Frame(None, title="HTML Tester Window")
        panel = MyPanel(frame)
        self.SetTopWindow(frame)
        frame.Fit()
        frame.Show(True)
        return True


if __name__ == "__main__" :
    app = MyApp(0)
    app.MainLoop()
