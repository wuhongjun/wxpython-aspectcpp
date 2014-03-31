#!/usr/bin/python 
#-*- coding: utf-8 -*-
import wx
import wx.aui
class MyFrame(wx.Frame):
    def __init__(self,*args,**kwargs):
        wx.Frame.__init__(self,*args,**kwargs)
        self.mgr=wx.aui.AuiManager(self)

        leftPanel=wx.Panel(self,-1,size=(200,150))
        rightPanel=wx.Panel(self,-1,size=(200,150))
        bottomPanel=wx.Panel(self,-1,size=(200,150))

        self.mgr.AddPane(leftPanel,wx.aui.AuiPaneInfo().Bottom())
        self.mgr.AddPane(rightPanel,wx.aui.AuiPaneInfo().Left().Layer(1))
        self.mgr.AddPane(bottomPanel,wx.aui.AuiPaneInfo().Center().Layer(2))
        self.mgr.Update()
class MyApp(wx.App):
    def OnInit(self):
        frame=MyFrame(None,-1,"布局")
        frame.Show()
        self.SetTopWindow(frame)
        return 1
if __name__ == '__main__':
    app=MyApp(0)
    app.MainLoop()
