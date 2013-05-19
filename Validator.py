#!/usr/bin/env python

import string, wx

class FloatValidator(wx.PyValidator):
    ''' Validates data as it is entered into the text controls. '''

    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        '''Required Validator method'''
        return FloatValidator()

    def Validate(self, win):
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def OnChar(self, event):
        wx.CallAfter(self.SetBackground)
        keycode = int(event.GetKeyCode())
        if keycode < 256:
            print keycode
            key = chr(keycode)
            print keycode, key
            if ( key in string.letters and key <> 'e' ):
                # doesn't let user enter any letter except "e" (used for exponential notation
                return
        event.Skip()

    def SetBackground(self):
        """
        Change the background color if the input is invalid
        """
        ctrl = self.Window
        val = ctrl.Value
        if val == "": val = 0 # allow a blank to equal 0
        try:
            float(val)
            ctrl.BackgroundColour = None
        except ValueError:
            ctrl.BackgroundColour = "red"
            

class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Validator Test")
 
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        
        self.txtEntryOne = wx.TextCtrl(panel, validator=FloatValidator())
        self.txtEntryTwo = wx.TextCtrl(panel, validator=FloatValidator())
        self.txtEntryOne.Bind(wx.EVT_TEXT, self.onTextEntry)
        self.txtEntryTwo.Bind(wx.EVT_TEXT, self.onTextEntry)
        
        self.total = wx.StaticText(panel, label="Total:")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.txtEntryOne, 0, wx.ALL, 4)
        sizer.Add(self.txtEntryTwo, 0, wx.ALL, 4)
        sizer.Add(self.total)
        panel.SetSizer(sizer)

    #----------------------------------------------------------------------
    def onTextEntry(self, event):
        """
        Add up the two text control and display the total
        """
        
        valueOne = self.txtEntryOne.GetValue()
        valueTwo = self.txtEntryTwo.GetValue()
        
        if valueOne == "":
            valueOne = 0
        if valueTwo == "":
            valueTwo = 0
        
        try:
            total = float(valueOne) + float(valueTwo)
            self.total.SetLabel("Total: %0.4g" % total)
        except ValueError:
            self.total.SetLabel("Invalid Input")

# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
