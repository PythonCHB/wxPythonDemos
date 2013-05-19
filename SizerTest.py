#!/usr/bin/env python2.3

import wx

class MainWindow(wx.Frame):
    """ This window displays a button """
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self, parent , -1, title)

        self.List = map(str, range(10) ) # just to get a list of text items

        #Create a box inside to contain everything except the outputbox

        # what's this for?
        #innersizerbox =wx.BoxSizer(wx.HORIZONTAL)

        #Create panel to contain other widgets (everything except the outputbox)
        #use a panel if the widgets are logically grouped, but make a class for it in this case.
        #self.panel = wx.Panel(self,-1,style=wx.ALIGN_BOTTOM|wx.ALIGN_CENTER)

        #Create a flexsizer to contain other widgets (everything except the
        #outputbox) need 2 rows and 9 columns
        # 18 widgets?, I count ten. and you had rows and columns backward.
        flexsizer= wx.FlexGridSizer(5,2,0,0)

        #Create a box to which to write output
        self.outputbox = wx.TextCtrl(self, -1, "",size=wx.DefaultSize,
                                     style=wx.TE_READONLY|wx.TE_WORDWRAP|wx.TE_MULTILINE)


        self.file_input = wx.RadioButton(self, 31, label='Read input from file',
                                        pos=(-1,-1))
        self.gui_input = wx.RadioButton(self, 36, label='Select command below',
                                        pos=(1,-1))

        #wx.EVT_RADIOBUTTON(self, 31, self.SetMode)
        #wx.EVT_RADIOBUTTON(self, 36, self.SetMode)

        #was this ever used?
        #radiosizer = wx.BoxSizer(wx.HORIZONTAL)
        flexsizer.Add(self.file_input,1,wx.ALL, 10)
        flexsizer.Add(self.gui_input,1, wx.EXPAND|wx.ALL, 15)

        #Create combosizer which will contain the combobox and its label
        combosizer = wx.BoxSizer(wx.HORIZONTAL)

        #Create a Command Drop Down
        self.combolabel = wx.StaticText(self,-1,"Please select a command:")
        self.combo=wx.ComboBox(self, 30, " ",
                              wx.Point(wx.ALIGN_LEFT),
                              wx.DefaultSize,
                              self.List, wx.CB_DROPDOWN)
        #wx.EVT_COMBOBOX(self, 30, self.CommandCallback)

        combosizer.Add(self.combolabel, 1, wx.EXPAND|wx.ALL, 10)
        combosizer.Add(self.combo, 2, wx.EXPAND|wx.ALL, 10)
        flexsizer.Add(combosizer, 2, wx.EXPAND, 10)

        #Create a box to accept parameters
        self.parameterslabel = wx.StaticText(self, -1, "Enter parameters:")
        self.parameters=wx.TextCtrl(self,-1,"", size=wx.DefaultSize)

        parametersizer = wx.BoxSizer(wx.HORIZONTAL)
        parametersizer.Add(self.parameterslabel,0,wx.ALL, 10)
        parametersizer.Add(self.parameters,1, wx.ALL, 15)

        flexsizer.Add(parametersizer,1,3,wx.ALL,10)

        #Create button 1
        self.buttonone = wx.Button(self, 32, label= "ONE",
                                  style = wx.BU_BOTTOM ,size=(150,20),
                                  name = "one")
        #wx.EVT_BUTTON(self, 32, self.One_Func)

        #Create button 2
        self.buttontwo = wx.Button(self, 33, label= "TWO",
                                  style = wx.BU_BOTTOM ,size=(150,20),
                                  name = "two")
        #wx.EVT_BUTTON(self, 33, self.Two_Func)

        #Create button 3
        self.buttonthree = wx.Button(self, 34, label= "THREE",
                                  style = wx.BU_BOTTOM ,size=(150,20),
                                  name = "three")
        #wx.EVT_BUTTON(self, 34, self.Three_Func)

        #Create button 4
        self.buttonfour = wx.Button(self, 35, label= "FOUR",
                                  style = wx.BU_BOTTOM ,size=(150,20),
                                  name = "four")
        #wx.EVT_BUTTON(self, 35, self.Four_Func)

        timeoutwarning=wx.StaticText(self, -1, 'Disable Timeouts Prior to Use')

        flexsizer.Add(self.buttonone,4, wx.ALL|wx.ALIGN_RIGHT, 10)
        flexsizer.Add(self.buttontwo, 5, wx.ALL|wx.ALIGN_RIGHT, 10)
        flexsizer.Add(self.buttonthree, 6, wx.ALL|wx.ALIGN_RIGHT, 10)
        flexsizer.Add(self.buttonfour, 8, wx.ALL|wx.ALIGN_RIGHT, 10)
        flexsizer.Add(timeoutwarning, 9, wx.ALL|wx.ALIGN_BOTTOM, 10)

        #Now add the output box and the flexgridsizer to the outerboxsize
        #Create the outer sizer which is essentially the main window
        # no, it's not a Window...it does do the layout for the main window.
        # I like to build fromt eh inside out, so I put this here. It's really a matter of taste.
        outerboxsizer = wx.BoxSizer(wx.VERTICAL)
        outerboxsizer.Add(self.outputbox, 1, wx.EXPAND|wx.ALL, 10)
        outerboxsizer.Add(flexsizer)
        #Connect the outerboxsizer to the window (self)
        self.SetSizer(outerboxsizer)
        self.Fit()
        

    def SetMode(self):
        pass

    def OnQuit(self,Event):
        self.Destroy()

        
class MyApp(wx.App):
    def OnInit(self):

        frame = MainWindow(None, -1, "Micro App")
        self.SetTopWindow(frame)
        frame.Show()
        
        return True
        

app = MyApp(0)
app.MainLoop()





