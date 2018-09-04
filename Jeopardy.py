#!/usr/bin/env python
"""

A simple Jeopardy Game

Modeled after the Game show Jeopardy! (tm), this program
lets you run a simple game yourself, with questions and
answers provided by you.

NOTE: very much a work in progress!

This code is in the public domain

  -Chris.Barker@noaa.gov

"""

import wx


class Question(object):
    """
    A class to hold each question, and data about it.
    """
    def __init__(self, question, answer, value):
        self.question = question
        self.answer = answer
        self.value = value

        self.answered = False


class Game:
    def __init__(self, catagories, questions):
        self.catagories = catagories
        self.questions = questions
        self.num_cat = len(catagories)
        self.num_ques = len(questions[0])

    def all_answered(self):
        """
        returns True if all the questions are answered
        """
        solved = True
        for cat in self.questions:
            for q in cat:
                if q.answered:
                    solved = False
                    break
        return solved


class GridGeom:
    def __init__(self, w, h, num_catagories=6, num_questions=5):

        self.box_w = w / num_catagories
        self.box_h = h / (num_questions + 1)
        self.num_cat = num_catagories
        self.num_ques = num_questions

        self.font_size = min( int(self.box_w / 2), int(self.box_h / 2) )

        ##figure out the text offset
        dc = wx.ScreenDC()
        dc.SetFont(wx.FontFromPixelSize((self.font_size, self.font_size),
                   wx.FONTFAMILY_SWISS,
                   wx.FONTSTYLE_NORMAL,
                   wx.FONTWEIGHT_BOLD,
                                        ),
                   )
        w, h = dc.GetTextExtent("500")
        self.text_off_x = ( self.box_w - w ) / 2
        self.text_off_y = ( self.box_h - h ) / 2

class GridWindow(wx.Window):
    def __init__(self, parent, game):
        wx.Window.__init__(self, parent)
        self.SetBackgroundColour("White")

        self.game = game

        ## a few initalzers
        self.Selected = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)

        self.OnSize()

    def InitBuffer(self):
        w, h = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(w, h)
        self.DrawNow()

    def OnSize(self, event=None):
        size = self.GetClientSize()
        if size[0] > 0 and size[1] > 1:
            self.grid = GridGeom(*size)
            self.InitBuffer()

    def DrawNow(self):
        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        self.Draw(dc)
        self.Refresh()
        self.Update()
#        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
#        self.Draw(dc)

    def Draw(self, dc):
        # Make grid local:
        grid = self.grid
        w = grid.box_w
        h = grid.box_h
        # draw the background:
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetBrush(wx.Brush(wx.Colour(128,128,255)))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0, 0, w * grid.num_cat, h * grid.num_ques)

        # draw catagory headings
        dc.SetFont(wx.FontFromPixelSize((grid.font_size, grid.font_size),
                                        wx.FONTFAMILY_SWISS,
                                        wx.FONTSTYLE_NORMAL,
                                        wx.FONTWEIGHT_BOLD))

        for i, cat in enumerate(self.game.catagories):
            dc.SetBrush( wx.Brush("Blue", wx.SOLID) )
            dc.SetPen( wx.Pen("White", width=4) )
            dc.DrawRectangle(i*w + 3, h + 3, w - 6, h - 6 )
            dc.DrawText(cat, i*w + grid.text_off_x, h + grid.text_off_y)


        #draw cells
        dc.SetFont(wx.FontFromPixelSize((grid.font_size, grid.font_size),
                                        wx.FONTFAMILY_SWISS,
                                        wx.FONTSTYLE_NORMAL,
                                        wx.FONTWEIGHT_BOLD))
        for i, cat in enumerate(self.game.questions):
            for j, q in enumerate(cat):
                j+=1
                if q.answered:
                    dc.SetBrush( wx.Brush("Blue", wx.SOLID) )
                    dc.SetPen( wx.Pen("Black", width=4) )
                    dc.DrawRectangle(i*w + 3, j*h + 3, w - 6, h - 6 )
                else:
                    dc.SetBrush( wx.Brush("Blue", wx.SOLID) )
                    dc.SetPen( wx.Pen("White", width=4) )
                    dc.DrawRectangle(i*w + 3, j*h + 3, w - 6, h - 6 )
                    dc.DrawText('%i'%q.value, i*w + grid.text_off_x, j*h + grid.text_off_y)



        # # draw the selected cells:
        # dc.SetBrush(wx.Brush("Red", wx.SOLID))
        # dc.DrawRectangle(x0 + d*self.Selected[1], y0 + d*self.Selected[0], d, d)

        # # draw the white lines:
        # dc.SetPen(wx.Pen("White", 2, wx.SOLID) )
        # for i in range(10):
        #     dc.DrawLine(x0, y0 + d*i, x0 + d*9, y0 + d*i)
        #     dc.DrawLine(x0 + d*i, y0, x0 + d*i, y0 + d*9)

        # # draw the numbers:
        # dc.SetFont(wx.FontFromPixelSize((font_size,font_size),
        #                                 wx.FONTFAMILY_SWISS,
        #                                 wx.FONTSTYLE_NORMAL,
        #                                 wx.FONTWEIGHT_BOLD))
        # for i in range(5):
        #     for j in range(5):
        #         val = self.Puzzle.Grid[i,j]
        #         if val > 0:
        #             dc.DrawText('%i'%val, x0 + d*j + text_off_x, y0 + d*i + text_off_y)

        # # Draw the Big Grid
        # dc.SetPen(wx.Pen("Black", 3, wx.SOLID))
        # dc.SetBrush(wx.TRANSPARENT_BRUSH)

        # d*=3
        # for i in range(4):
        #     dc.DrawLine(x0, y0 + d*i, x0 + d*3, y0 + d*i)
        #     dc.DrawLine(x0 + d*i, y0, x0 + d*i, y0 + d*3)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)

    def OnLeftDown(self, e):
        """called when the left mouse button is pressed"""
        grid = self.grid
        x, y = e.GetPositionTuple()
        i = x / grid.box_w
        j = y / grid.box_h - 1  # compensate for header
        if i >= 0 and i < grid.num_cat and j >= 0 and j < grid.num_ques:
            self.game.questions[i][j].answered = not self.game.questions[i][j].answered
            self.DrawNow()

    def OnMotion(self, evt):
        pass
    # def OnKeyDown(self, e):
    #     keycode = e.GetKeyCode()
    #     i, j = self.Selected
    #     if (keycode == wx.WXK_TAB or
    #         keycode == wx.WXK_RIGHT or
    #         keycode == wx.WXK_RETURN or
    #         keycode == wx.WXK_SPACE):
    #         j += 1
    #     elif keycode == wx.WXK_UP:
    #         i -= 1
    #     elif keycode == wx.WXK_DOWN:
    #         i += 1
    #     elif keycode == wx.WXK_LEFT:
    #         j -= 1
    #     elif keycode == wx.WXK_DELETE:
    #         self.Puzzle.Grid[self.Selected] = 0
    #         self.CheckValid()
    #     elif keycode >= ord("0") and keycode <= ord("9"):
    #         self.Puzzle.Grid[self.Selected] = (keycode - ord("0"))
    #         self.CheckValid()
    #         j += 1
    #     if j > 8:
    #         j = 0
    #         i += 1
    #     if j < 0:
    #         j = 8
    #         i -= 1
    #     if i > 8:
    #         i = 0
    #     if i < 0:
    #         i = 8

    #     self.Selected = (i,j)
    #     self.DrawNow()

    # def SetValue(self, value):
    #     self.Puzzle.Grid[self.Selected] = value

class MainFrame(wx.Frame):
    def __init__(self, parent, game):
        wx.Frame.__init__(self, parent, title="Jeopardy", size=(600, 500))
        self.game = game
        self.grid = GridWindow(self, game)
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

class Header(object):
    """
    class to handle drawing of question header
    """
    # font info:
    Family = wx.MODERN,
    Style = wx.NORMAL,
    Weight = wx.NORMAL,
    Underlined = False,
    FaceName = ''

    def __init__(self, text):

        self.width = 100
        self.font_size = 12
        self.text = text

        self.wrap_to_width()
        self.PadSize = 2

    def wrap_to_width(self):
        dc = wx.MemoryDC()
        bitmap = wx.EmptyBitmap(1, 1)
        dc.SelectObject(bitmap) #wxMac needs a Bitmap selected for GetTextExtent to work.
#        Size = self.font_size
#        Width = (self.Width - 2*self.PadSize)
#        self.SetFont(DrawingSize, self.Family, self.Style, self.Weight, self.Underlined, self.FaceName)
#        dc.SetFont(self.Font)
#        NewStrings = []
#        for s in (self.question,):
#            text = s.split(" ")
#            text.reverse()
#            LineLength = 0
#            NewText = text[-1]
#            del text[-1]
#            while text:
#                w  = dc.GetTextExtent(' ' + text[-1])[0]
#                if LineLength + w <= Width:
#                    NewText += ' '
#                    NewText += text[-1]
#                    LineLength = dc.GetTextExtent(NewText)[0]
#                else:
#                    NewStrings.append(NewText)
#                    NewText = text[-1]
#                    LineLength = dc.GetTextExtent(text[-1])[0]
#                del text[-1]
#            NewStrings.append(NewText)
#        self.question_lines = NewStrings
#
#    def LayoutText(self):
#        """
#        Calculates the positions of the words of text.
#
#        This isn't exact, as fonts don't scale exactly.
#        To help this, the position of each individual word
#        is stored separately, so that the general layout stays
#        the same  as the fonts scale.
#        """
#        self.Strings = self.String.split("\n")
#        if self.Width:
#            self.WrapToWidth()
#
#        dc = wx.MemoryDC()
#        bitmap = wx.EmptyBitmap(1, 1)
#        dc.SelectObject(bitmap) #wxMac needs a Bitmap selected for GetTextExtent to work.
#
#        DrawingSize = self.LayoutFontSize # pts This effectively determines the resolution that the BB is computed to.
#        ScaleFactor = float(self.Size) / DrawingSize
#
#        self.SetFont(DrawingSize, self.Family, self.Style, self.Weight, self.Underlined, self.FaceName)
#        dc.SetFont(self.Font)
#        TextHeight = dc.GetTextExtent("X")[1]
#        SpaceWidth = dc.GetTextExtent(" ")[0]
#        LineHeight = TextHeight * self.LineSpacing
#
#        LineWidths = N.zeros((len(self.Strings),), N.float)
#        y = 0
#        Words = []
#        AllLinePoints = []
#
#        for i, s in enumerate(self.Strings):
#            LineWidths[i] = 0
#            LineWords = s.split(" ")
#            LinePoints = N.zeros((len(LineWords),2), N.float)
#            for j, word in enumerate(LineWords):
#                if j > 0:
#                    LineWidths[i] += SpaceWidth
#                Words.append(word)
#                LinePoints[j] = (LineWidths[i], y)
#                w = dc.GetTextExtent(word)[0]
#                LineWidths[i] += w
#            y -= LineHeight
#            AllLinePoints.append(LinePoints)
#        TextWidth = N.maximum.reduce(LineWidths)
#        self.Words = Words
#
#        if self.Width is None:
#            BoxWidth = TextWidth * ScaleFactor + 2*self.PadSize
#        else: # use the defined Width
#            BoxWidth = self.Width
#        Points = N.zeros((0,2), N.float)
#
#        for i, LinePoints in enumerate(AllLinePoints):
#            ## Scale to World Coords.
#            LinePoints *= (ScaleFactor, ScaleFactor)
#            if self.Alignment == 'left':
#                LinePoints[:,0] += self.PadSize
#            elif self.Alignment == 'center':
#                LinePoints[:,0] += (BoxWidth - LineWidths[i]*ScaleFactor)/2.0
#            elif self.Alignment == 'right':
#                LinePoints[:,0] += (BoxWidth - LineWidths[i]*ScaleFactor-self.PadSize)
#            Points = N.concatenate((Points, LinePoints))
#
#        BoxHeight = -(Points[-1,1] - (TextHeight * ScaleFactor)) + 2*self.PadSize
#        #(x,y) = self.ShiftFun(self.XY[0], self.XY[1], BoxWidth, BoxHeight, world=1)
#        Points += (0, -self.PadSize)
#        self.Points = Points
#        self.BoxWidth = BoxWidth
#        self.BoxHeight = BoxHeight
#        self.CalcBoundingBox()

    # def draw(self, DC):
    #     for word in question:
    #         pass


if __name__ == '__main__':

    catagories = [None for i in range(6)]
    questions = [[None for i in range(5)] for j in range(6)]

    # test data:

    catagories[0] = "Household Pets"
    questions[0][0] = Question("slobbery", "what is a dog?", 100)
    questions[0][1] = Question("cute and fuzzy", "what is a cat?", 200)
    questions[0][2] = Question("long and slithery", "what is a snake?", 300)
    questions[0][3] = Question("sometimes lives in a sewer", "what is a rat?", 400)
    questions[0][4] = Question("a reptile often mistaken for an amphibian",
                               "what is a turtle?", 500)

    catagories[1] = "Household Pets"
    questions[1][0] = Question("slobbery", "what is a dog?", 100)
    questions[1][1] = Question("cute an fuzzy", "what is a cat?", 200)
    questions[1][2] = Question("long and slithery", "what is a snake?", 300)
    questions[1][3] = Question("sometimes lives in a sewer", "what is a rat?", 400)
    questions[1][4] = Question("a reptile often mistaken for an amphibian",
                               "what is a turtle?", 500)

    catagories[2] = "Household Pets"
    questions[2][0] = Question("slobbery", "what is a dog?", 100)
    questions[2][1] = Question("cute an fuzzy", "what is a cat?", 200)
    questions[2][2] = Question("long and slithery", "what is a snake?", 300)
    questions[2][3] = Question("sometimes lives in a sewer", "what is a rat?", 400)
    questions[2][4] = Question("a reptile often mistaken for an amphibian",
                               "what is a turtle?", 500)

    catagories[3] = "Household Pets"
    questions[3][0] = Question("slobbery", "what is a dog?", 100)
    questions[3][1] = Question("cute an fuzzy", "what is a cat?", 200)
    questions[3][2] = Question("long and slithery", "what is a snake?", 300)
    questions[3][3] = Question("sometimes lives in a sewer", "what is a rat?", 400)
    questions[3][4] = Question("a reptile often mistaken for an amphibian",
                               "what is a turtle?", 500)
    catagories[4] = "Household Pets"
    questions[4][0] = Question("slobbery", "what is a dog?", 100)
    questions[4][1] = Question("cute an fuzzy", "what is a cat?", 200)
    questions[4][2] = Question("long and slithery", "what is a snake?", 300)
    questions[4][3] = Question("sometimes lives in a sewer", "what is a rat?", 400)
    questions[4][4] = Question("a reptile often mistaken for an amphibian",
                               "what is a turtle?", 500)

    catagories[5] = "Household Pets"
    questions[5][0] = Question("slobbery", "what is a dog?", 100)
    questions[5][1] = Question("cute an fuzzy", "what is a cat?", 200)
    questions[5][2] = Question("long and slithery", "what is a snake?", 300)
    questions[5][3] = Question("sometimes lives in a sewer", "what is a rat?", 400)
    questions[5][4] = Question("a reptile often mistaken for an amphibian",
                               "what is a turtle?", 500)

    # set a few as answered
    questions[3][3].answered = True
    questions[2][4].answered = True

    app = wx.App(0)
    game = Game(catagories, questions)
    frame = MainFrame(None, game)
    frame.Show(True)
    app.MainLoop()

