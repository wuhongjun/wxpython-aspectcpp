#!/usr/bin/python 
#-*- coding: utf-8 -*-
import wx
import wx.aui
import os
def appendDir(tree, treeID, sListDir):
    """遍历路径,将文件生成节点加入到wx的tree中
        tree wx的tree
        treeID 上级treeID
        sListDir 一个绝对路径,会自动遍历下面的子目录
    """
    #有些目录没有权限访问的,避免其报错
    try:
        ListFirstDir = os.listdir(sListDir)
        for i in ListFirstDir:
            sAllDir = sListDir+"/"+i
            #有些目录名非法,无法生成节点,只有try一把
            try:
                childID = tree.AppendItem(treeID, i)
            except:
                childID = tree.AppendItem(treeID, "非法名称")
            #如果是目录,那么递归
            if os.path.isdir(sAllDir):
                appendDir(tree, childID, sAllDir)
    except:
        pass
def appendProject(tree, treeRootID, projectFileDir):
    """只有在projectfile中且在当前目录下的文件才为工程文件
    """
    projectFile_fp=open(projectFileDir+'.project')
    fileInDirList=os.listdir(projectFileDir)
    print 1
    treeHead=tree.AppendItem(treeRootID,'头文件')
    print 2
    treeSource=tree.AppendItem(treeRootID,'源文件')
    print 3
    treeAspectHead=tree.AppendItem(treeRootID,'切面文件')
    print 4
    treeOther=tree.AppendItem(treeRootID,'资源文件')
    print 5
    projectFileList = projectFile_fp.readlines()

    for i in fileInDirList:
        for j in projectFileList:
            if i == j:
                file_name = i
                if file_name.endswith('.h'):
                    tree.AppendItem(treeHead,file_name)
                elif file_name.endswith('.cc') or file_name.endswith('.cpp'):
                    tree.AppendItem(treeSource,file_name)
                elif file_name.endswith('.ah'):
                    tree.AppendItem(treeAspectHead,file_name)
                else:
                    tree.AppendItem(treeOther,file_name)
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
        self.treeRoot=self.tree.AddRoot('/home/willzhang')
        appendDir(self.tree,self.treeRoot,'/home/willzhang/')
        self.tree.Expand(self.treeRoot)

        #menuBar
        menuBar=wx.MenuBar()
        menuProject=wx.Menu()
        menuFile=wx.Menu()
        menuBar.Append(menuProject,u'工程')
        self.SetMenuBar(menuBar)

        #menuProject
        menuProject.Append(1001,u'新建')
        menuProject.Append(1002,u'打开')

        #Bind
        self.Bind(wx.EVT_MENU,self.newProject,id=1001)

        self.filePath=''
        self.projectDir=''
        self.projectName=''
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
    def newProject(self,event):
        self.projectDir=self.GetPath()
        newProjectDialog = wx.TextEntryDialog(self,"",'project name','')
        if newProjectDialog.ShowModal() == wx.ID_OK:
            self.projectName=newProjectDialog.GetValue()
        newProjectDialog.Destroy()
        os.mkdir(self.projectDir+self.projectName)
        os.mknod(self.projectDir+self.projectName+'/'+'.project')
        self.tree.DeleteAllItems()
        self.tree.AddRoot(self.projectName)
        appendProject(self.tree,self.treeRoot,self.projectDir+self.projectName+'/')
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
