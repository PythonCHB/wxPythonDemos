#!/usr/bin/python2.3

"""
A small program to produce a "magnifying glass" effect over an image.

Adapted from code posted to wxPython-users by Peter Damoc


"""
try:
    import fixdc
except ImportError:
    pass # If you get an error like: DC_DrawBitmap() takes at most 4 arguments (5 given)
         # you need the fixdc module, and don't have it
import wx

class MyCanvas(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.bmp = wx.Bitmap('splash.gif')
        self.mpos = (0,0)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        #self.SetSizeHints(*self.bmp.GetSize())
        self.SetSizeHints( self.bmp.GetWidth(), self.bmp.GetHeight() )
        self.lentSize = 80
        self.Zoom = 2.
        self.usePIL = False
    def OnMouseMove(self, evt):
        self.mpos = evt.GetPosition()
        self.Refresh(False)
        evt.Skip()
    def SetMask(self, bmp):
        #size = bmp.GetSize()
        size = ( self.bmp.GetWidth(), self.bmp.GetHeight() )
        mask = wx.EmptyBitmap(*size)
        mdc = wx.MemoryDC()
        mdc.SelectObject(mask)
        mdc.SetBrush(wx.BLACK_BRUSH)
        mdc.DrawRectangle(0,0, size[0], size[1])
        mdc.SetBrush(wx.WHITE_BRUSH)
        mdc.DrawEllipse(0,0, size[0], size[1])
        mdc.SelectObject(wx.NullBitmap)
        m = wx.Mask(mask)
        bmp.SetMask(m)
    def getAALoupe(self):
        sample = self.lentSize/self.Zoom        
        x = self.mpos[0]-sample/2
        y = self.mpos[1]-sample/2
        import Image
        loupe = wx.EmptyBitmap(sample, sample)
        mdc = wx.MemoryDC()
        mdc.SelectObject(loupe)
        mdc.Blit(0, 0, sample, sample, self.offDC, x, y)
        mdc.SelectObject(wx.NullBitmap)
        image = wx.ImageFromBitmap(loupe)
        pil = Image.new('RGB', (image.GetWidth(), image.GetHeight()))
        pil.fromstring(image.GetData())
        pil = pil.resize((self.lentSize, self.lentSize), Image.ANTIALIAS)
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        image.SetData(pil.convert('RGB').tostring())
        loupe = image.ConvertToBitmap()
        self.SetMask(loupe)
        return loupe
        
    def getLoupe(self):
        sample = self.lentSize/self.Zoom        
        x = self.mpos[0]-sample/2
        y = self.mpos[1]-sample/2
        loupe = wx.EmptyBitmap(self.lentSize, self.lentSize)
        mdc = wx.MemoryDC()
        mdc.SelectObject(loupe)
        mdc.SetUserScale(self.Zoom, self.Zoom)
        mdc.Blit(0, 0, sample, sample, self.offDC, x, y)
        mdc.SelectObject(wx.NullBitmap)
        self.SetMask(loupe)
        return loupe
        
    def OnPaint(self, evt):
        #self.size = self.bmp.GetSize()
        self.size = ( self.bmp.GetWidth(), self.bmp.GetHeight() )
        offscreenBMP = wx.EmptyBitmap(*self.size)
        self.offDC = wx.MemoryDC()
        self.offDC.SelectObject(offscreenBMP)
        self.offDC.Clear()
        self.offDC.BeginDrawing()
        self.offDC.DrawBitmap(self.bmp, 0, 0, True)
        
        if self.usePIL:
            try:
                loupe = self.getAALoupe()
            except:
                loupe = self.getLoupe()
        else:
            loupe = self.getLoupe()
        x = self.mpos[0]-self.lentSize/2
        y = self.mpos[1]-self.lentSize/2
        if self.mpos[0]>0 and self.mpos[1]>0 and \
                self.mpos[0]<self.size[0]-1 and self.mpos[1]<self.size[1]-1:
            self.offDC.DrawBitmap(loupe, x, y, True)

        self.offDC.EndDrawing()
        self.dc = wx.PaintDC(self)
        self.dc.Blit(0, 0, self.size[0], self.size[1], self.offDC, 0, 0)
        evt.Skip()
        
class Controller(wx.Panel):
    zooms = ['x2', 'x4', 'x8', 'x16']
    lents = ['80', '120', '160']
    def __init__(self, parent):
        self.canvas = parent.canvas
        wx.Panel.__init__(self, parent, -1)
        self.pil = wx.CheckBox(self, -1, "Use AA Resize", style=wx.ALIGN_RIGHT)
        self.rb = wx.RadioBox(
                self, -1, "Zoom:", wx.DefaultPosition, wx.DefaultSize,
                self.zooms, 1, wx.RA_SPECIFY_ROWS)
        self.loupe = wx.RadioBox(
                self, -1, "Lent Size:", wx.DefaultPosition, wx.DefaultSize,
                self.lents, 1, wx.RA_SPECIFY_ROWS)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.pil, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add((-1,-1), 1)
        sizer.Add(self.loupe, 0, wx.ALL, 5)
        sizer.Add((-1,-1), 1)
        sizer.Add(self.rb, 0, wx.ALL, 5)
        self.SetSizer(sizer)
        self.pil.Bind(wx.EVT_CHECKBOX, self.OnPIL)
        self.rb.Bind(wx.EVT_RADIOBOX, self.OnZoom)
        self.loupe.Bind(wx.EVT_RADIOBOX, self.OnLoupe)
        
    def OnLoupe(self, evt):
        self.canvas.lentSize = int(self.loupe.GetStringSelection())
    def OnZoom(self, evt):
        self.canvas.Zoom = float(self.rb.GetStringSelection()[1:])
    def OnPIL(self, evt):
        self.canvas.usePIL = self.pil.IsChecked()

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Lupa")
        self.canvas = MyCanvas(self)
        self.controller = Controller(self)
        sizer  = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas)
        sizer.Add(self.controller, 0, wx.EXPAND)
        #self.SetSizerAndFit(sizer)
        sizer.Layout()
        self.SetSizer(sizer)
        self.Fit()
        self.Show()

app = wx.PySimpleApp(0)
Frame()
app.MainLoop()


