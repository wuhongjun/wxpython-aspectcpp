#!/usr/bin/python 
#-*- coding: utf-8 -*-
import wx
import wx.aui
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'aspectc++',size=(1024,768))

        #layout
        self.mgr=wx.aui.AuiManager(self)
        leftText=wx.TextCtrl(self,-1,'leftText',wx.DefaultPosition,wx.Size(200,768),wx.NO_BORDER | wx.TE_MULTILINE)
        rightText=wx.TextCtrl(self,-1,'rightText',wx.DefaultPosition,wx.Size(824,600),wx.NO_BORDER | wx.TE_MULTILINE)
        bottomText=wx.TextCtrl(self,-1,'bottomText',wx.DefaultPosition,wx.Size(824,168),wx.NO_BORDER | wx.TE_MULTILINE)
        self.mgr.AddPane(bottomText,wx.aui.AuiPaneInfo().Bottom())
        self.mgr.AddPane(leftText,wx.aui.AuiPaneInfo().Left().Layer(1))
        self.mgr.AddPane(rightText,wx.aui.AuiPaneInfo().Center().Layer(2))
        self.mgr.Update()

        #menuBar
        menuBar=wx.MenuBar()
        menuFile=wx.Menu()
        menuBar.Append(menuFile,u'工程')
        self.SetMenuBar(menuBar)

        #menuFile
        menuFile.Append(1001,u'新建')
        menuFile.Append(1002,u'打开')

class MyApp(wx.App):
    def OnInit(self):
        frame=MyFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return 1
if __name__ == '__main__':
    app=MyApp()
    app.MainLoop()