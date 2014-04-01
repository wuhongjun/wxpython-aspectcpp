#!/usr/bin/python 
#-*- coding: utf-8 -*-
import wx
import wx.aui
import os
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'aspectc++',size=(1024,768))

        #layout
        self.mgr=wx.aui.AuiManager(self)
        self.leftText=wx.TextCtrl(self,-1,'leftText',wx.DefaultPosition,wx.Size(200,768),wx.NO_BORDER | wx.TE_MULTILINE)
        self.rightText=wx.TextCtrl(self,-1,'rightText',wx.DefaultPosition,wx.Size(824,600),wx.NO_BORDER | wx.TE_MULTILINE)
        self.bottomText=wx.TextCtrl(self,-1,'bottomText',wx.DefaultPosition,wx.Size(824,168),wx.NO_BORDER | wx.TE_MULTILINE)
        self.mgr.AddPane(self.bottomText,wx.aui.AuiPaneInfo().Bottom())
        self.mgr.AddPane(self.leftText,wx.aui.AuiPaneInfo().Left().Layer(1))
        self.mgr.AddPane(self.rightText,wx.aui.AuiPaneInfo().Center().Layer(2))
        self.mgr.Update()

        #menuBar
        menuBar=wx.MenuBar()
        menuProject=wx.Menu()
        menuFile=wx.Menu()
        menuBar.Append(menuProject,u'工程')
        menuBar.Append(menuFile,u'文件')
        self.SetMenuBar(menuBar)

        #menuProject
        menuProject.Append(1001,u'新建')
        menuProject.Append(1002,u'打开')

        #menuFile
        menuFile.Append(2001,u'新建')
        menuFile.Append(2002,u'打开')
        menuFile.Append(2003,u'保存')

        #Bind
        self.Bind(wx.EVT_MENU,self.newFile,id=2001)
        self.Bind(wx.EVT_MENU,self.openFile,id=2002)
        self.Bind(wx.EVT_MENU,self.saveFile,id=2003)

        self.filePath=''
    def newFile(self,event):
        self.rightText.SetValue('')
        self.fp=''
    def openFile(self,event):
        filterFile="All files (*.*) |*.*"
        openDialog=wx.FileDialog(self,u"选择文件",os.getcwd(),"",filterFile,wx.OPEN)
        if openDialog.ShowModal()==wx.ID_OK:
            self.filePath=openDialog.GetPath()
            fp=open(self.filePath)
            self.rightText.SetValue(fp.read())  
            fp.close()
        openDialog.Destroy()
    def saveFile(self,event):
        if self.filePath == '':
            filterFile="All files (*.*) |*.*"
            saveDialog=wx.FileDialog(self,u"选择文件",os.getcwd(),"",filterFile,wx.SAVE)
            if saveDialog.ShowModal() == wx.ID_OK:
                self.filePath=saveDialog.GetPath()
                fp=open(self.filePath,'w')
                fp.write(self.rightText.GetValue())
                fp.close()
            saveDialog.Destroy()
        else:
            fp=open(self.filePath,'w')
            fp.write(self.rightText.GetValue())
            fp.close()
class MyApp(wx.App):
    def OnInit(self):
        frame=MyFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return 1
if __name__ == '__main__':
    app=MyApp()
    app.MainLoop()