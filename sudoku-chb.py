#!/usr/bin/env python
"""
Yet another Sudoku Puzzle program.

This one does not solve puzzles.

However, it does display them, and will highlight the appropriate row, column,
or box if there is an error in the puzzle at any time, as you add numbers, etc.

One thing unique about this one is the use of numpy arrays. Numpy arrays have two
properties that make them handy for this problem:

1) n-d arrays (in this case 2-d)
2) slices as views on the data

The whole puzzle is a 9X 9 array
  each box is a 3X3 sub-array
  each row is a length 9 array
  each column is a length 9 array

these are share the same memory

This one also is a nice demo of a self-drawn semi-complex widget with wx.

This code is in the public domain
  -Chris.Barker@noaa.gov

"""


import wx
import numpy as N


# Old classic fixes.
if wx.VERSION < (2, 9):
    wx.BRUSHSTYLE_SOLID = wx.SOLID
    wx.PENSTYLE_SOLID = wx.SOLID

if 'phoenix' in wx.version():
    wx.EmptyBitmap = wx.Bitmap
    

class PuzzleGrid:
    def __init__(self):
        self.Grid = N.zeros((9,9), N.int8)
        Boxes = []
        for i in range(3):
            for j in range(3):
              Boxes.append(self.Grid[3*i:3*i+3, 3*j:3*j+3])

        self.Boxes = Boxes

    def SetValue(self, (r,c), v):
        self.Grid[r,c] = v

    def GetValue(self, (r, c)):
        return self.Grid[r,c]

    def Solved(self):
        """
        returns True is the puzzle is solved, False otherwise
        """
        raise NotImplementedError

    def CheckRows(self):
        """
        returns a values for each row:
        0 -- repeated values
        1 -- valid, but not solved
        2 -- solved

        """
        results = N.zeros((9,), N.int8 )
        for i in range(9):
            results[i] = self.CheckValid(self.Grid[i,:])
        return results

    def CheckColumns(self):
        """
        returns a values for each row:
        0 -- repeated values
        1 -- valid, but not solved
        2 -- solved

        """
        results = N.zeros((9,), N.int8 )
        for i in range(9):
            results[i] = self.CheckValid(self.Grid[:,i])
        return results

    def CheckBoxes(self):
        """
        returns a values for each row:
        0 -- repeated values
        1 -- valid, but not solved
        2 -- solved

        """
        results = N.zeros((9,), N.int8 )
        for i in range(9):
            results[i] = self.CheckValid(self.Boxes[i])
        return results


    def CheckValid(self, A):
        """
        CheckValid(A) -- checks if A has any digits repeated.

        returns 0 is there are any digits repeated (invalid)
        returns 1 if none are repeated, but there are zeros (valid, but not solved)
        returns 2 if all digits, 1-9 are there (solved)

        A should be a numpy array that has 9 elements
        """

        there = []
        for i in A.flat:
            if i>0 and i in there:
                return 0
            else:
                there.append(i)
        if 0 in there:
            return 1
        return 2


    def __str__(self):
        msg = []
        for i in range(9):
            if not i%3:
                msg.append("|-----------------------|\n")
            msg.append("| %i %i %i | %i %i %i | %i %i %i |\n"%tuple(self.Grid[i]))
        msg.append("|-----------------------|\n")
        return "".join(msg)


def test_PuzzleGrid():
    P = PuzzleGrid()
    print P
    print "These should all be true:"
    # all valid, butnot solved
    print P.CheckValid(N.array( (1,2,0,4,0,6,0,8,9), dtype=N.int8 ) ) == 1
    print P.CheckValid(N.array( (0,0,0,0,0,0,0,0,0), dtype=N.int8 ) ) == 1
    print P.CheckValid(N.array( (1,2,0,4,5,6,7,8,9), dtype=N.int8) ) == 1

    # solved
    print P.CheckValid(N.array( (1,2,3,4,5,6,7,8,9), dtype=N.int8) ) == 2
    print P.CheckValid(N.array( (1,2,9,4,5,6,7,8,3), dtype=N.int8) ) == 2
    print P.CheckValid(N.array( (9,8,7,6,5,4,3,2,1), dtype=N.int8) ) == 2

    # all not valid
    print P.CheckValid(N.array( (1,1,0,4,0,6,0,8,9), dtype=N.int8 ) ) == 0
    print P.CheckValid(N.array( (1,0,0,4,0,6,0,9,9), dtype=N.int8 ) ) == 0
    print P.CheckValid(N.array( (1,1,1,4,4,6,0,1,1), dtype=N.int8 ) ) == 0

class Grid:
    def __init__(self, w, h):
        size = min(w,h)
        self.d = d = max( 2, (size - 20) / 9 )# make  sure we don't get zero...
        self.x0 = (w - (self.d * 9)) / 2
        self.y0 = (h - (self.d * 9)) / 2
        self.font_size = int(11 * d/16.0)
        ##figure out the text offset
        dc = wx.ScreenDC()
        dc.SetFont(wx.Font(self.font_size,
                    wx.FONTFAMILY_SWISS,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD,
                                        )
                   )
        w,h = dc.GetTextExtent("5")
        self.text_off_x = ( d - w )/2+2 # I don't know why I need to azdd the 2!
        self.text_off_y = ( d - h )/2+2

class GridWindow(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.SetBackgroundColour("White")

        self.Puzzle = PuzzleGrid()

        self.InvalidRows = []
        self.InvalidColumns = []
        self.InvalidBoxes = []

        ## a few initalzers
        self.Selected = (5,7)
        self.Puzzle.Grid[3,4] = 3
        self.Puzzle.Grid[8,7] = 5

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.OnSize()

    def InitBuffer(self):
        w, h = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(w, h)
        self.DrawNow()

    def OnSize(self, event=None):
        size = self.GetClientSize()
        if size[0] > 0 and size[1] > 1:
            self.Grid = Grid(*size)
            self.InitBuffer()

    def DrawNow(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.Draw(dc)

    def Draw(self, dc):
        # Make grid info local:
        d = self.Grid.d
        x0 = self.Grid.x0
        y0 = self.Grid.y0
        font_size = self.Grid.font_size
        text_off_x = self.Grid.text_off_x
        text_off_y = self.Grid.text_off_y

        # draw the background:
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetBrush(wx.Brush(wx.Colour(128,128,255)))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(x0, y0, d*9, d*9 )

        #draw The invalid rows
        for i in self.InvalidRows:
            dc.SetBrush(wx.Brush("Purple", wx.BRUSHSTYLE_SOLID))
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.DrawRectangle(x0, y0 + i*d, 9*d, d )

        #draw The invalid columns
        for i in self.InvalidColumns:
            dc.SetBrush(wx.Brush("Purple", wx.BRUSHSTYLE_SOLID))
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.DrawRectangle(x0 + i*d, y0, d, 9*d )

        #draw The invalid boxes
        for i in self.InvalidBoxes:
            dc.SetBrush(wx.Brush("Purple", wx.BRUSHSTYLE_SOLID))
            dc.SetPen(wx.TRANSPARENT_PEN)
            r = i//3
            c = i%3
            dc.DrawRectangle(x0 + c*3*d, y0 + r*3*d, 3*d, 3*d )

        # draw the selected cell:
        dc.SetBrush(wx.Brush("Red", wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(x0 + d*self.Selected[1], y0 + d*self.Selected[0], d, d)

        # draw the white lines:
        dc.SetPen(wx.Pen("White", 2, wx.PENSTYLE_SOLID) )
        for i in range(10):
            dc.DrawLine(x0, y0 + d*i, x0 + d*9, y0 + d*i)
            dc.DrawLine(x0 + d*i, y0, x0 + d*i, y0 + d*9)

        # draw the numbers:
        dc.SetFont(wx.Font(font_size,
                           wx.FONTFAMILY_SWISS,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_BOLD))
        for i in range(9):
            for j in range(9):
                val = self.Puzzle.Grid[i,j]
                if val > 0:
                    dc.DrawText('%i'%val, x0 + d*j + text_off_x, y0 + d*i + text_off_y)

        # Draw the Big Grid
        dc.SetPen(wx.Pen("Black", 3, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        d*=3
        for i in range(4):
            dc.DrawLine(x0, y0 + d*i, x0 + d*3, y0 + d*i)
            dc.DrawLine(x0 + d*i, y0, x0 + d*i, y0 + d*3)


    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)

    def CheckValid(self):
        self.InvalidRows    = N.nonzero(self.Puzzle.CheckRows() == 0)[0]
        self.InvalidColumns = N.nonzero(self.Puzzle.CheckColumns() == 0)[0]
        self.InvalidBoxes   = N.nonzero(self.Puzzle.CheckBoxes() == 0)[0]

    def OnLeftDown(self, e):
        """called when the left mouse button is pressed"""
        if 'phoenix' in wx.version():
            x, y = e.GetPosition()
        else:
            x, y = e.GetPositionTuple()
        i = (y - self.Grid.y0) / self.Grid.d
        j = (x - self.Grid.x0) / self.Grid.d
        if i >= 0 and i < 9 and j >= 0 and j < 9:
            self.Selected = (i,j)
            self.DrawNow()

    def OnKeyDown(self, e):
        keycode = e.GetKeyCode()
        i, j = self.Selected
        if (keycode == wx.WXK_TAB or
            keycode == wx.WXK_RIGHT or
            keycode == wx.WXK_RETURN or
            keycode == wx.WXK_SPACE):
            j += 1
        elif keycode == wx.WXK_UP:
            i -= 1
        elif keycode == wx.WXK_DOWN:
            i += 1
        elif keycode == wx.WXK_LEFT:
            j -= 1
        elif keycode == wx.WXK_DELETE:
            self.Puzzle.Grid[self.Selected] = 0
            self.CheckValid()
        elif keycode >= ord("0") and keycode <= ord("9"):
            self.Puzzle.Grid[self.Selected] = (keycode - ord("0"))
            self.CheckValid()
            j += 1
        if j > 8:
            j = 0
            i += 1
        if j < 0:
            j = 8
            i -= 1
        if i > 8:
            i = 0
        if i < 0:
            i = 8

        self.Selected = (i,j)
        self.DrawNow()

    def SetValue(self, value):
        self.Puzzle.Grid[self.Selected] = value

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Sudoku Machine", size=(500, 500))
        self.grid = GridWindow(self, -1)
        #self.ToolBar()

#    def ToolBar(self):
#        statusBar = self.CreateStatusBar()
#        menuBar = wx.MenuBar()
#        menu1 = wx.Menu()
#        menuBar.Append(menu1, "&File")
#        menu2 = wx.Menu()
#        menu2.Append(wx.NewId(), "&Copy", "Copy in status bar")
#        menu2.Append(wx.NewId(), "&Cut", "")
#        menu2.Append(wx.NewId(), "Paste", "")
#        menu2.AppendSeparator()
#        menu2.Append(wx.NewId(), "&Options...", "Display options")
#        menuBar.Append(menu2, "&Edit")
#        self.SetMenuBar(menuBar)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'test':
        test_PuzzleGrid()
    else:
        app = wx.App(0)
        frame = MainFrame(None)
        frame.Show(True)
        app.MainLoop()

