#!/usr/bin/python 
#-*- coding: utf-8 -*-
import wx
import wx.aui
import os
def appendDir(tree, treeID, sListDir): 
    try:
        ListFirstDir = os.listdir(sListDir)
        for i in ListFirstDir:
            sAllDir = sListDir+"/"+i
            childID = tree.AppendItem(treeID, i)
            if os.path.isdir(sAllDir):
                appendDir(tree, childID, sAllDir)
    except:
        pass
def appendProject(tree, treeRootID, projectFileDir):
    projectFile_fp=open(projectFileDir+'.project')
    fileInDirList=os.listdir(projectFileDir)
    treeHead=tree.AppendItem(treeRootID,u'头文件')
    treeSource=tree.AppendItem(treeRootID,u'源文件')
    treeAspectHead=tree.AppendItem(treeRootID,u'切面文件') 
    treeOther=tree.AppendItem(treeRootID,u'资源文件')
    projectFileList = projectFile_fp.readlines()
    #for i in fileInDirList:
    #    print i
    #for j in projectFileList:
    #    print j.decode('utf-8')
    for i in fileInDirList:
        for j in projectFileList:
            if i == j.decode('utf-8')[:-1]:
                file_name = i
                if file_name.endswith('.h'):
                    tree.AppendItem(treeHead,file_name)
                elif file_name.endswith('.cc') or file_name.endswith('.cpp'):
                    tree.AppendItem(treeSource,file_name)
                elif file_name.endswith('.ah'):
                    tree.AppendItem(treeAspectHead,file_name)
                else:
                    tree.AppendItem(treeOther,file_name)
class MyPopupMenu(wx.Menu):
    def __init__(self,parent):
        super(MyPopupMenu,self).__init__()
        self.parent = parent
        
        mmi = wx.MenuItem(self,wx.NewId(),u'新建文件')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, parent.newFile, mmi)
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'aspectc++',size=(1024,768))

        #layout
        self.mgr=wx.aui.AuiManager(self)
        
        self.tree=wx.TreeCtrl(self,-1,size=(200,168))
        self.rightText=wx.TextCtrl(self,-1,'',wx.DefaultPosition,wx.Size(824,600),wx.NO_BORDER | wx.TE_MULTILINE)
        self.bottomText=wx.TextCtrl(self,-1,'',wx.DefaultPosition,wx.Size(824,168),wx.NO_BORDER | wx.TE_MULTILINE)
        self.syntaxTree=wx.TreeCtrl(self,size=(200,600))
        self.mgr.AddPane(self.bottomText,wx.aui.AuiPaneInfo().Bottom())
        self.mgr.AddPane(self.tree,wx.aui.AuiPaneInfo().Left().Layer(1))
        self.mgr.AddPane(self.syntaxTree,wx.aui.AuiPaneInfo().Left().Layer(1))
        self.mgr.AddPane(self.rightText,wx.aui.AuiPaneInfo().Center().Layer(2))
        self.mgr.Update()

        #leftDirs
        self.treeRoot=self.tree.AddRoot('D:/wx')
        appendDir(self.tree,self.treeRoot,'D:/wx')
        self.tree.Expand(self.treeRoot)

        #menuBar
        menuBar=wx.MenuBar()
        menuProject=wx.Menu()
        menuEdit=wx.Menu()
        menuBar.Append(menuProject,u'工程')
        menuBar.Append(menuEdit,u'编辑')
        self.SetMenuBar(menuBar)

        #menuProject
        menuProject.Append(1001,u'新建')
        menuProject.Append(1002,u'打开')
        menuEdit.Append(2001,u'保存')

        #Bind
        self.Bind(wx.EVT_MENU,self.newProject,id=1001)
        self.Bind(wx.EVT_MENU,self.openProject,id=1002)
        self.tree.Bind(wx.EVT_RIGHT_DOWN,self.RightClick)
        self.tree.Bind(wx.EVT_LEFT_DCLICK,self.LeftDClick)
        self.Bind(wx.EVT_MENU,self.saveFile,id=2001)

        self.filePath=''
        self.projectDir=''
        self.projectName=''
    

    def reFresh(self):
        self.tree.DeleteAllItems()
        self.treeRoot=self.tree.AddRoot(self.projectName)
        appendProject(self.tree,self.treeRoot,self.projectDir)
        self.tree.Expand(self.treeRoot)
    def GetPath(self):
        itemId=self.tree.GetSelection()
        Path=""
        while True:
            Path=self.tree.GetItemText(itemId)+'/'+Path
            if itemId != self.tree.GetRootItem():
                itemId=self.tree.GetItemParent(itemId)
            else:
                break
        return Path
    def LeftDClick(self,event):
        m_path=self.GetPath()
        if os.path.isfile(m_path[:-1]):
            m_path=m_path[:-1]
        else:
            m_path=self.projectDir+self.tree.GetItemText(self.tree.GetSelection())
        if os.path.isfile(m_path):
            self.filePath=m_path
            fp=open(m_path,'r')
            self.rightText.SetValue(fp.read().decode("utf-8"))
            fp.close()
    def RightClick(self,event):
        self.PopupMenu(MyPopupMenu(self),event.GetPosition())
    def newProject(self,event):
        self.projectDir=self.GetPath()
        newProjectDialog = wx.TextEntryDialog(self,"",'project name','')
        if newProjectDialog.ShowModal() == wx.ID_OK:
            self.projectName=newProjectDialog.GetValue()
        newProjectDialog.Destroy()
        self.projectDir+=self.projectName+'/'
        os.mkdir(self.projectDir)
        open(self.projectDir+'/'+'.project','w').close()
        self.tree.DeleteAllItems()
        self.treeRoot=self.tree.AddRoot(self.projectName)
        appendProject(self.tree,self.treeRoot,self.projectDir)
        self.tree.Expand(self.treeRoot)
    def openProject(self,event):
        filterFile="All files (.project) |.project"
        openDialog=wx.FileDialog(self,u"选择文件",os.getcwd(),"",filterFile,wx.OPEN)
        if openDialog.ShowModal()==wx.ID_OK:
            self.projectDir=openDialog.GetPath()[:-8]
            self.projectName=self.projectDir.split('\\')[-2]
            self.reFresh()
        openDialog.Destroy()
    def newFile(self,event):
        newFileNameDialog=wx.TextEntryDialog(self,"",'file name','')
        newFileNameDialog.ShowModal()
        newFileName=newFileNameDialog.GetValue()
        newFileNameDialog.Destroy()
        self.filePath=self.projectDir+newFileName
        open(self.filePath,'w').close()
        fp_project=open(self.projectDir+'.project','a')
        fp_project.write((newFileName+'\n').encode('utf-8'))
        fp_project.close()
        self.reFresh()
    def openFile(self,event):
        print 1
    def saveFile(self,event):
        if self.filePath == '':
            filterFile="All files (*.*) |*.*"
            saveDialog=wx.FileDialog(self,u"选择文件",os.getcwd(),"",filterFile,wx.SAVE)
            if saveDialog.ShowModal() == wx.ID_OK:
                self.filePath=saveDialog.GetPath()
                fp=open(self.filePath,'w')
                fp.write(self.rightText.GetValue().encode('utf-8'))
                fp.close()
            saveDialog.Destroy()
        else:
            fp=open(self.filePath,'w')
            fp.write(self.rightText.GetValue().encode('utf-8'))
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