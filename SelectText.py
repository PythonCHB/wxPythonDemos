#!/usr/bin/env python

import  wx

BUFFERED = 1


class Shape:
    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.Size[0], self.Size[1])

class DragShape(Shape):
    def __init__(self, bmp):
        self.bmp = bmp
        self.pos = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = False
        self.IsDrag = True
        self.Size = (self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False


class TextShape(Shape):
    def __init__(self, string):
        self.string = string
        self.pos = (0,0)
        self.shown = True
        self.fullscreen = False
        self.Size = None
        self.IsDrag = False

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)


    def Draw(self, dc, op=wx.COPY):
        font = wx.Font(36, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial")
        #text1 = "Hi there, this is some text"
        #textExtent = self.GetFullTextExtent(text1, font)
        dc.SetTextForeground(wx.BLACK)
        dc.SetFont(font)
        if self.Size is None:
            self.Size = dc.GetTextExtent(self.string)
        dc.DrawText(self.string, self.pos[0], self.pos[1])


#----------------------------------------------------------------------
class MyCanvas(wx.ScrolledWindow):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER | wx.NO_FULL_REPAINT_ON_RESIZE)

        self.shapes = []
        self.shape1 = []
        self.shape2 = []

        self.dragImage = None
        self.dragShape = None
        self.hiliteShape = None

        self.lines = []
        self.maxWidth  = 1000
        self.maxHeight = 1000
        self.x = self.y = 0
        self.curLine = []
        self.drawing = False

        self.bg_bmp = wx.Bitmap("Images/BG.jpg", wx.BITMAP_TYPE_ANY)
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

        self.SetScrollbars(80, 25, self.maxWidth / 20, self.maxHeight / 20)

#-----------------------------------------------------------------------------------

        if BUFFERED:
            # Initialize the buffer bitmap.  No real DC is needed at this point.
            self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
            dc = wx.BufferedDC(None, self.buffer)
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()
            self.DoDrawing(dc)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def getWidth(self):
        return self.maxWidth

    def getHeight(self):
        return self.maxHeight

    def OnPaint(self, event):
        if BUFFERED:
            dc = wx.BufferedPaintDC(self, self.buffer)
        else:
            dc = wx.PaintDC(self)
            self.PrepareDC(dc)
            self.DoDrawing(dc)

    def DoDrawing(self, dc, printing=False):
        dc.BeginDrawing()

        # Add a text object:
        text1 = TextShape("Hi there, this is some text")
        text1.pos = (25, 25)
        self.shapes.append(text1)

        bmp = wx.EmptyBitmap(845, 1079)
        shape1 = DragShape(bmp)
        shape1.pos = (125, 55)
        shape1.fullscreen = False
        self.shapes.append(shape1)

        dc = wx.MemoryDC()
        dc.SelectObject(bmp)

        bmp2 = wx.Bitmap("Paper.jpg", wx.BITMAP_TYPE_ANY)
        dc.DrawBitmap(bmp2, -14, -15)

        dc.EndDrawing()

    def SetXY(self, event):
        self.x, self.y = self.ConvertEventCoords(event)

    def ConvertEventCoords(self, event):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        return (event.GetX() + (xView * xDelta),
                event.GetY() + (yView * yDelta))

    # tile the background bitmap
    def TileBackground(self, dc):
        sz = self.GetClientSize()
        w = self.bg_bmp.GetWidth()
        h = self.bg_bmp.GetHeight()

        x = 0

        while x < sz.width:
            y = 0

            while y < sz.height:
                dc.DrawBitmap(self.bg_bmp, x, y)
                y = y + h

            x = x + w

    # Go through our list of shapes and draw them in whatever place they are.
    def DrawShapes(self, dc):
        for shape in self.shapes:
            if shape.shown:
                shape.Draw(dc)

    # This is actually a sophisticated 'hit test', but in this
    # case we're also determining which shape, if any, was 'hit'.
    def FindShape(self, pt):
        for shape in self.shapes:
            if shape.HitTest(pt):
                return shape
        return None

    # Remove a shape from the display
    def EraseShape(self, shape, dc):
        r = shape.GetRect()
        dc.SetClippingRect(r)
        self.TileBackground(dc)
        self.DrawShapes(dc)
        dc.DestroyClippingRegion()

    # Clears the background, then redraws it. If the DC is passed, then
    # we only do so in the area so designated. Otherwise, it's the whole thing.
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()

        if not dc:
            dc = wxClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        self.TileBackground(dc)

    # Fired whenever a paint event occurs
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        self.DrawShapes(dc)

    # Left mouse button is down.
    def OnLeftDown(self, evt):
        # Did the mouse go down on one of our shapes?
        shape = self.FindShape(evt.GetPosition())

        # If a shape was 'hit', then set that as the shape we're going to
        # drag around. Get our start position. Dragging has not yet started.
        # That will happen once the mouse moves, OR the mouse is released.
        if shape:
            if shape.IsDrag:
                self.dragShape = shape
                self.dragStartPos = evt.GetPosition()
            else:
                print "Text Object Hit: %s"%shape.string
    # Left mouse button up.
    def OnLeftUp(self, evt):
        if not self.dragImage or not self.dragShape:
            self.dragImage = None
            self.dragShape = None
            return

        # Hide the image, end dragging, and nuke out the drag image.
        self.dragImage.Hide()
        self.dragImage.EndDrag()
        self.dragImage = None

        dc = wx.ClientDC(self)

        if self.hiliteShape:
            self.hiliteShape.Draw(dc)
            self.hiliteShape = None



        self.dragShape.pos = (
            self.dragShape.pos[0] + evt.GetPosition()[0] - self.dragStartPos[0],
            self.dragShape.pos[1] + evt.GetPosition()[1] - self.dragStartPos[1]
            )

        self.dragShape.shown = True
        self.dragShape.Draw(dc)
        self.dragShape = None

    # The mouse is moving
    def OnMotion(self, evt):
        # Ignore mouse movement if we're not dragging.
        if not self.dragShape or not evt.Dragging() or not evt.LeftIsDown():
            return

        # if we have a shape, but haven't started dragging yet
        if self.dragShape and not self.dragImage:

            # only start the drag after having moved a couple pixels
            tolerance = 2
            pt = evt.GetPosition()
            dx = abs(pt.x - self.dragStartPos.x)
            dy = abs(pt.y - self.dragStartPos.y)
            if dx <= tolerance and dy <= tolerance:
                return

            # erase the shape since it will be drawn independently now
            dc = wx.ClientDC(self)
            self.dragShape.shown = False
            self.EraseShape(self.dragShape, dc)

            if self.dragShape.text:
                self.dragImage = wx.DragString(self.dragShape.text,
                                              wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.dragImage = wx.DragImage(self.dragShape.bmp,
                                             wx.StockCursor(wx.CURSOR_HAND))

            hotspot = self.dragStartPos - self.dragShape.pos
            self.dragImage.BeginDrag(hotspot, self, self.dragShape.fullscreen)

            self.dragImage.Move(pt)
            self.dragImage.Show()
        # if we have shape and image then move it, posibly highlighting another shape.
        elif self.dragShape and self.dragImage:
            onShape = self.FindShape(evt.GetPosition())
            unhiliteOld = False
            hiliteNew = False

            # figure out what to hilite and what to unhilite
            if self.hiliteShape:
                if onShape is None or self.hiliteShape is not onShape:
                    unhiliteOld = True

            if onShape and onShape is not self.hiliteShape and onShape.shown:
                hiliteNew = True

            # if needed, hide the drag image so we can update the window
            if unhiliteOld or hiliteNew:
                self.dragImage.Hide()

            if unhiliteOld:
                dc = wx.ClientDC(self)
                self.hiliteShape.Draw(dc)
                self.hiliteShape = None

            if hiliteNew:
                dc = wx.ClientDC(self)
                self.hiliteShape = onShape
                self.hiliteShape.Draw(dc, wx.INVERT)

            # now move it and show it again if needed
            self.dragImage.Move(evt.GetPosition())
            if unhiliteOld or hiliteNew:
                self.dragImage.Show()


if __name__ == '__main__':
    app = wx.App(0)
    frame = wx.Frame(None, -1, "A Test Frame")
    win = MyCanvas(frame)
    frame.Show()
    app.MainLoop()
