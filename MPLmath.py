#!/usr/bin/env python

"""
test of embedding matplotlib, and using it to render math

Written by Chris Barker
"""

import matplotlib
matplotlib.use( 'WXAgg' )
import matplotlib.figure
import matplotlib.backends.backend_wxagg

import wx

class MathPanel (wx.Panel):
    """
    The MathPanel is a very simple panel with just and MPL figure on it,
    it will automatically render text in the middle of the figure
    """
    def __init__( self, *args, **kwargs ):
        kwargs['style'] = wx.NO_FULL_REPAINT_ON_RESIZE
        wx.Panel.__init__( self, *args, **kwargs )

        # initialize matplotlib stuff
        self.figure = matplotlib.figure.Figure( None )
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg( self, -1, self.figure )

        self._SetSize()

        self.Bind(wx.EVT_SIZE, self._SetSize)
        
        self.TeX = ""
        self.font_size = 32

        self.draw()

    def SetTeX(self, str):
        self.TeX = "$%s$"%str
        self.draw()

    def draw(self):
        try:
            self.figure.clear()
            self.figure.text(0.05, 0.5, self.TeX, size=self.font_size)
            self.canvas.draw()
        except matplotlib.pyparsing.ParseFatalException:
            self.figure.clear()
            self.figure.text(0.05, 0.5, "Parsing Error in MathTeX", size=self.font_size)
            self.canvas.draw()
            
    def _SetSize( self, evt=None ):
        pixels = self.GetSize()
        self.SetSize( pixels )
        self.canvas.SetSize( pixels )
        self.figure.set_size_inches( float( pixels[0] )/self.figure.get_dpi(),
                                     float( pixels[1] )/self.figure.get_dpi() )


class MathFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        
        self.input_box = wx.TextCtrl(self, size=(500,80), )
        self.input_box.Font = wx.Font(16,
                                      wx.FONTFAMILY_TELETYPE,
                                      wx.FONTSTYLE_NORMAL,
                                      wx.FONTWEIGHT_NORMAL)
        self.Bind(wx.EVT_TEXT, self.OnText)
        self.math_panel = MathPanel(self, size = (500, 200))
        
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(wx.StaticText(self, label="Type some TeX here:"), 0, wx.TOP|wx.LEFT, 5)
        S.Add(self.input_box, 0, wx.GROW|wx.ALL, 5)
        S.Add(self.math_panel, 1, wx.GROW)
        self.SetSizerAndFit(S)
        
        self.Show()
        self.input_box.Value = r'\frac{(a+fffb)}{(c-d)}'
    
    def OnText(self, evt):
        self.math_panel.SetTeX(self.input_box.Value)
                                       
if __name__ == '__main__':

    app = wx.App( False )
    frame = MathFrame( None, title='Test Matplotlib Math Renderer')
    app.MainLoop()
