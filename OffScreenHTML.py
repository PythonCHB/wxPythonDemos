#!/usr/bin/env python

"""
test of rendering HTML to an off-screen bitmap
"""

import wx
import wx.html

class OffScreenHTML:
    def __init__(self, width, height):
        
        self.width = width
        self.height = height
        self.Buffer = wx.EmptyBitmap(width, height)
        
        self.HR = wx.html.HtmlDCRenderer()
        
        # a bunch of defaults...
        self.BackgroundColor = "White"
        self.Padding = 10
        
       
    def Render(self, source):
        """
        Render the html source to the bitmap
        """
        DC = wx.MemoryDC()
        DC.SelectObject(self.Buffer)
        DC.SetBackground(wx.Brush(self.BackgroundColor))
        DC.Clear()
        
        self.HR.SetDC(DC, 1.0)
        self.HR.SetSize(self.width-2*self.Padding, self.height)
        
        self.HR.SetHtmlText(source)
        self.HR.Render(self.Padding, self.Padding, [])
        self.RenderedSize = (self.width, self.HR.GetTotalHeight()+2*self.Padding)

    def SaveAsPNG(self, filename):
        sub = self.Buffer.GetSubBitmap(wx.Rect(0, 0, *self.RenderedSize) )
        sub.SaveFile(filename, wx.BITMAP_TYPE_PNG)

class Text2html:
    """
    A simple class for converting plain text to basic HTML
    
    This is an alternative to using <pre> -- I want it to wrap, but otherwise preserve newlines, etc.

    """
    def __init__(self):
        pass
    
    def Convert(self, text):
        """
        Takes raw text, and returns html with newlines converted, etc.
        """
        print "raw text:", text
        # double returns are a new paragraph
        text = text.split("\n\n")
        print "split by paragraphs:", text
        text = [p.strip().replace("\n","<br>") for p in text]
        print text
        text = "<p>\n" + "\n</p>\n<p>\n".join(text) + "\n</p>"
        
        return text




if __name__ == "__main__":
    HTML = """ <h1> A Title </h1>
    
    <p>This is a simple test of rendering a little text with an html renderer</p>
    
    <p>
    Now another paragraph, with a bunch more text in it. This is a test
    that will show if it can take care of the basic rendering for us, and
    auto-wrap, and all sorts of nifty stuff like that
    </p>
    
    <p> It does seem to work OK </p> 
    """
    
    App = wx.App(False)
    OSR = OffScreenHTML(500, 500)
    OSR.width = 200 
    OSR.Render(HTML)
    OSR.SaveAsPNG('junk.png')
    OSR.width = 300 
    OSR.Render(HTML)
    OSR.SaveAsPNG('junk2.png')
    


