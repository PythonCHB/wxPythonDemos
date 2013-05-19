######################################################################
# Name:        MatrixLed                                             #
# Purpose:     A LED Matrix Display                                  #
#                                                                    #
# Author:      Pinassi "O-Zone" Michele <o-zone@siena.linux.it>      #
# Licence:     Same as wxPython's                                    #
#                                                                    #
# v1.0 - Initial Release                                             #
#                                                                    #
######################################################################

import wx
import time
import Numeric as N

class LEDMatrix(wx.Window):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name=""):
        
        wx.Window.__init__(self, parent, id, pos, size, style, name)

        self.parent = parent

        self.bgColour = wx.NamedColour("GREY76")
        self.fgColour = wx.NamedColour("LIGHTBLUE2")
        self.onColour = wx.NamedColour("DEEPSKYBLUE4")
	self.charSpace = 9
	
	self.romAlpha = { "A" :   "0001000000101000010001001000001011111110100000101000001010000010",
                    	  "B" :   "1111111001000001010000010111111001000001010000010100000111111110",
			  "C" :   "0011111001000000100000001000000010000000100000000100000000111110",
			  "D" :   "1111100001000100010001000100010001000100010001000100010011111000",
			  "E" :   "1111111001000000010000000100000001111000010000000100000011111110",
			  "F" :   "1111111001000000010000000111100001000000010000000100000001000000",
			  "G" :   "0011110001000010100000001000000010000000100001100100001000111100",
			  "H" :   "0100001001000010010000100100001001111110010000100100001001000010",
			  "I" :   "0011100000010000000100000001000000010000000100000001000000111000",
			  "L" :   "0100000001000000010000000100000001000000010000000100000001111110",
			  "M" :   "1000001011000110101010101001001010000010100000101000001010000010",
			  "N" :   "1100001001100010010100100100101001000110010000100100001001000010",
			  "O" :   "0011110001000010010000100100001001000010010000100100001000111100",
			  "P" :   "1111110001000010010000100111110001000000010000000100000001000000",
			  "Q" :   "0011110001000010010000100100001001000010010000100100011000111111",
			  "R" :   "1111110001000010010000100111110001010000010010000100010001000010",
			  "S" :   "0011110001000010010000000010000000011100000000100100001000111100",
			  "T" :   "1111111000010000000100000001000000010000000100000001000000010000",
			  "U" :   "0100001001000010010000100100001001000010010000100100001000111100",
			  "V" :   "1000001010000010100000100100010001000100001010000010100000010000",
			  "Z" :   "1111111010000010000001000000100000010000001000000100001011111110",
			  "X" :   "1000000101000010001001000001100000011000001001000100001010000001",
			  "Y" :   "0100001001000010001001000001100000010000000100000001000000010000",
			  "W" :   "",
			  "K" :   "",
			  "J" :   "",
			  "0" :   "",
			  "1" :   "",
			  "2" :   "",
			  "3" :   "",
			  "4" :   "",
			  "5" :   "",
			  "6" :   "",
			  "7" :   "",
			  "8" :   "",
			  "9" :   "",
			  ":" :   "",
			  "." :   "",
			  " " :   "0000000000000000000000000000000000000000000000000000000000000000"
		        }

        

        self.SetForegroundColour(wx.Colour(0, 204, 204))

        # Event handling
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

	# Now for the starting value
	self.DoArray()

    def OnSize(self, event):
	print "OnSize X:",self.matrix_x,"Y:",self.matrix_y
	# Salvare l'array precedente
	temp_x = self.matrix_x
	temp_y = self.matrix_y
##	tempArray = [[0 for i in range(temp_x)] for i in range(temp_y)]
##	for x in range(temp_x):
##	    for y in range(temp_y):
##		tempArray[y][x] = self.matrixArray[y][x]
        tempArray = self.matrixArray.copy()
	
	# Ricreare l'array
	self.DoArray()
	
	# Copiare i dati dell'array precedente su quello nuovo
	#for x in range(temp_x):
	#    for y in range(temp_y):
	#	self.matrixArray[y][x] = tempArray[y][x]
        self.matrixArray[:,:] = tempArray[:,:]

        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self._selColours(self.bgColour, dc)
        w, h = self.GetSize()
	print "OnPaint()"
	self._doClear(dc)
        #dc.DrawRectangle((0, 0), (w, h))
        #self._doMatrix(dc)
	self._doUpdate(dc)

    def DoArray(self):
        w, h = self.GetSize()
	self.matrixArray = [[0 for i in range(w)] for i in range(h)]
	self.matrix_x = w
	self.matrix_y = h
	print "DoArray X:",w,"Y:",h
    
    def _doUpdate(self,dc):
        self._selColours(self.onColour, dc)
	print "doUpdate X:",self.matrix_x,"Y:",self.matrix_y
	for x in range(self.matrix_x):
	    for y in range(self.matrix_y):
		if int(self.matrixArray[y][x]):
    		    self._drawXY(x,y,dc)		

    def _doClear(self,dc):
        self._selColours(self.bgColour, dc)
	print "doClear X:",self.matrix_x,"Y:",self.matrix_y
	for x in range(self.matrix_x):
	    for y in range(self.matrix_y):
		if (self.matrixArray[y][x] == 0):
    		    self._drawXY(x,y,dc)		
		    		
    def _doMatrix(self, dc):
        w, h = self.GetSize()
        self._selColours(self.fgColour, dc)
	x = y = 0
	for x in range(w/4):
	    for y in range(h/4):
    		self._drawXY(x,y,dc)

    def _drawXY(self,x,y,dc):
	dc.DrawRectangle((x*4)+2, (y*4)+2, 3, 3)

    def _selColours(self, colour, dc):
        dc.SetPen(wx.Pen(colour, 1, wx.SOLID))
        dc.SetBrush(wx.Brush(colour, wx.SOLID))
        
    def _drawAlpha(self,dc,char,ox,oy):
	alpha = self.romAlpha[char]
        for y in range(0, 8):
	    for x in range(0, 8):
        	if int(alpha[(y*8)+x]):
		    self.matrixArray[oy+y][ox+x] = 1;
		    		    
    def SetValue(self, value):
	vo = value.upper()
        dc = wx.PaintDC(self)
        self._selColours(self.onColour, dc)
	cx = 5
        for x in range(0, len(vo)):
	    self._drawAlpha(dc,vo[x],cx,5)
	    cx = cx + self.charSpace

    def EVTUpdate(self,evt): # A method to Bind UPDATE to an EVENT
        dc = wx.PaintDC(self)
        start = time.time()
	self._doClear(dc)
        print "_doClear took %f seconds"%(time.time()-start)
        start = time.time()
	self._doUpdate(dc)    
        print "_doUpdate took %f seconds"%(time.time()-start)
    
    def ShiftLeft(self): # Alpha - Don't use !
	print "ShiftLeft"
	for x in range(0,self.matrix_x-1):
	    for y in range(0,self.matrix_y-1):
		if int(self.matrixArray[y][x]):
		    self.matrixArray[y][x-1] = self.matrixArray[y][x];
		    self.matrixArray[y][x] = 0
    
    
	    
