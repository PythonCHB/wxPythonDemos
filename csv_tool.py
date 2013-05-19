#!/usr/bin/env python


"""

csv_tool.py

This is a small, simple app that simply reads, writes, and lets you edit CSV files.

It's not a spreadsheet, as it doesn't handle any calculations or anything -- just text in CSV files

"""
import sys, os
import csv

import wx
import wx.grid

# empty table:
empty_table = []
for i in range(30):
    row = []
    for j in range(8):
        row.append("")
    empty_table.append(row)

class CSVTable(wx.grid.PyGridTableBase):
    def __init__(self, filename=None):
        wx.grid.PyGridTableBase.__init__(self)

        if filename is None:
            self.table = empty_table
            self._comp_size()
        else:
            self.LoadFromFile(filename)

    def _comp_size(self):
        cols = 0
        for row in self.table:
            cols = max(len(row), cols)
        self.num_cols = cols
        self.num_rows = len(self.table)

    def LoadFromFile(self, filename):
        
        try:
            reader = csv.reader(file(filename, 'rU'),
                                dialect='excel')# [optional keyword args])
        except csv.Error:
            dlg = wx.E
        self.table = [row for row in reader]
        self._comp_size()
        
    def Save(self, filename):
        """
        save the table to the given filename
        """
        # first cleanout empty rows
        self.RemoveEmptyStuff()
        writer = csv.writer(file(filename, 'wb'),
                            dialect='excel')
        
        writer.writerows(self.table)

    def RemoveEmptyStuff(self):
        """
        removes empty rows at the end of the table
        and columns at the right of the table
        
        not used right now....
        """
        # strip the extra rows
        for i in range(len(self.table)-1, -1, -1):
            empty_row = True
            for j, cell in enumerate(self.table[i]):
                if cell:
                    empty_row=False
            if empty_row:
                del self.table[i]
            else:
                break
        # look for max columns:
        max_col = 0
        for row in self.table:
            for j, cell in enumerate(row):
                if cell:
                    max_col = max(j, max_col)
        # strip the extra columns
        for i in range(len(self.table)):
            self.table[i] = self.table[i][:max_col+1]

        self._comp_size()

    def GetNumberRows(self):
        """Return the number of rows in the grid"""
        return len(self.table)

    def GetNumberCols(self):
        """Return the number of columns in the grid"""
        return self.num_cols

    def IsEmptyCell(self, row, col):
        """Return True if the cell is empty"""
        try:
            self.table[row][col]
        except IndexError:
            return True
        return False

    def GetTypeName(self, row, col):
        """Return the name of the data type of the value in the cell"""
        return wx.grid.GRID_VALUE_STRING

    def GetValue(self, row, col):
        """Return the value of a cell"""
        print "GetValue called:", row, col
        try:
            return self.table[row][col]
        except IndexError:
            return ""
    
    def SetValue(self, row, col, value):
        """Set the value of a cell"""
        self.table[row][col] = value

class ButtonBar(wx.Panel):
    def __init__(self, Grid, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.Grid = Grid
        self.MainFrame = parent
        
        
        OpenButton = wx.Button(self, label="Open")
        OpenButton.Bind(wx.EVT_BUTTON, self.OnOpen)

        SaveButton = wx.Button(self, label="Save")
        SaveButton.Bind(wx.EVT_BUTTON, self.OnSave)

        SaveAsButton = wx.Button(self, label="Save As")
        SaveAsButton.Bind(wx.EVT_BUTTON, self.OnSaveAs)

        AutoSizeButton = wx.Button(self, label="AutoSize")
        AutoSizeButton.Bind(wx.EVT_BUTTON, self.OnAutoSize)
        
        S = wx.BoxSizer(wx.HORIZONTAL)
        S.Add(OpenButton, 0, wx.ALL, 5)
        S.Add(SaveButton, 0, wx.ALL, 5)
        S.Add(SaveAsButton, 0, wx.ALL, 5)
        S.Add(AutoSizeButton, 0, wx.ALL, 5)
        self.SetSizer(S)
        
    def OnAutoSize(self, evt=None):
        self.Grid.AutoSize()

    def OnOpen(self, evt=None):
        self.MainFrame.OnOpen()

    def OnSave(self, evt=None):
        self.MainFrame.OnSave()

    def OnSaveAs(self, evt=None):
        self.MainFrame.OnSaveAs()


class CSVGrid(wx.grid.Grid):
    def __init__(self, *args, **kwargs):
        wx.grid.Grid.__init__(self, *args, **kwargs)
        
        # set up the TableBase
        self.table = CSVTable()
        self.SetTable( self.table )
    
    def LoadNewFile(self, filename):
        self.table.LoadFromFile(filename)
        self.SetTable(self.table)
        #self.AutoSize()
        self.ForceRefresh()
        #self.SetTable( table)

    def SaveFile(self, filename):
        self.table.Save(filename)
        self.SetTable(self.table)


class CSVFrame(wx.Frame):
    def __init__(self, title = "CSV Editor"):
        wx.Frame.__init__(self, None, size = (800, 600), title=title)

        ##Build the menu bar
        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        
        item = FileMenu.Append(wx.ID_EXIT, text = "&Exit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)

        item = FileMenu.Append(wx.ID_ANY, text = "&Open")
        self.Bind(wx.EVT_MENU, self.OnOpen, item)

        item = FileMenu.Append(wx.ID_ANY, text = "&Save")
        self.Bind(wx.EVT_MENU, self.OnSave, item)

        item = FileMenu.Append(wx.ID_ANY, text = "&SaveAs")
        self.Bind(wx.EVT_MENU, self.OnSaveAs, item)

        item = FileMenu.Append(wx.ID_PREFERENCES, text = "&Preferences")
        self.Bind(wx.EVT_MENU, self.OnPrefs, item)

        MenuBar.Append(FileMenu, "&File")
        
        HelpMenu = wx.Menu()

        item = HelpMenu.Append(wx.ID_HELP, "CSV &Help",
                                "Help for this simple CSV reader")
        self.Bind(wx.EVT_MENU, self.OnHelp, item)

        ## this gets put in the App menu on OS-X
        item = HelpMenu.Append(wx.ID_ABOUT, "&About",
                                "More information About this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        MenuBar.Append(HelpMenu, "&Help")

        self.SetMenuBar(MenuBar)

        self.grid = CSVGrid(self)

        self.ButtonBar = ButtonBar(self.grid, self)
        
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(self.ButtonBar, 0, wx.EXPAND)
        S.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(S)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.CurrentFilename = ""
    
    def OpenFile(self, filename):
        self.grid.LoadNewFile(filename)
        self.CurrentFilename = os.path.abspath(filename)
        self.SetTitle(filename)
        self.grid.Layout()
        self.grid.Refresh()
        self.grid.Update()


    
    def OnQuit(self,Event):
        self.Destroy()
        
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self,
                               "This is a small program to view\n"
                               "and edit simple CSV files\n",
                               "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnHelp(self, event):
        dlg = wx.MessageDialog(self, "This would be help\n"
                                     "If there was any\n",
                                "CSV Help", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnOpen(self, event=None):
        if self.CurrentFilename:
            cur_dir, cur_name = os.path.split(self.CurrentFilename)
        else:
            cur_dir = "."
            cur_name = ""
        dlg = wx.FileDialog(self, 'Choose a csv file to open',
                            cur_dir,
                            '',
                            '*.csv',
                            wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            f = dlg.GetPath()
            self.OpenFile(f)
        dlg.Destroy()

    def OnSave(self, event=None):
        if self.CurrentFilename:
            self.grid.SaveFile(self.CurrentFilename)
        else:
            self.OnSaveAs(event)
            
    def OnSaveAs(self, event=None):
        self.CurrentFilename
        if self.CurrentFilename:
            cur_dir, cur_name = os.path.split(self.CurrentFilename)
        else:
            cur_dir = os.getcwd()
            cur_name = ""
        dlg = wx.FileDialog(self, 'filename to save',
                            cur_dir,
                            cur_name,
                            '*.csv',
                            wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.grid.SaveFile(filename)
        dlg.Destroy()


    def OnPrefs(self, event):
        dlg = wx.MessageDialog(self,
                               "This would be an preferences Dialog\n"
                               "If there were any preferences to set.\n",
                               "Preferences", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
class MyApp(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)
        
        # This catches events when the app is asked to activate by some other
        # process
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)

    def OnInit(self):

        self.frame = CSVFrame()
        self.frame.Show()

        import sys

        try:
            f = sys.argv[1]
            self.frame.OpenFile(f)
        except IndexError:
            pass

        return True

    def BringWindowToFront(self):
        try: # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except:
            pass
        
    def OnActivate(self, event):
        # if this is an activate event, rather than something else, like iconize.
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()
    
    def OpenFileMessage(self, filename):
        dlg = wx.MessageDialog(None,
                               "This app was just asked to open:\n%s\n"%filename,
                               "File Dropped",
                               wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        self.frame.OpenFile(filename)

    def MacOpenFile(self, filename):
        """Called for files droped on dock icon, or opened via finders context menu"""
        if filename == sys.argv[0]:
            pass # there was no filename in command line
        else:
            self.frame.OpenFile(filename)
        
    def MacReopenApp(self):
        """Called when the doc icon is clicked, and ???"""
        self.BringWindowToFront()

    def MacNewFile(self):
        pass
    
    def MacPrintFile(self, file_path):
        pass
 

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()





