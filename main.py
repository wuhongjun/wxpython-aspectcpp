#!/usr/bin/python 
#-*- coding: utf-8 -*-
import wx
import wx.aui
import os
import shutil
import subprocess
from wx import stc
import ctags
from ctags import CTags, TagEntry
from cppHighLight import CppSTC
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
        self.rightText=CppSTC(self,-1,pos=wx.DefaultPosition,size=wx.Size(824,600),style=0)
        self.bottomText=wx.TextCtrl(self,-1,'',wx.DefaultPosition,wx.Size(824,168),wx.NO_BORDER | wx.TE_MULTILINE)
        self.syntaxTree=wx.TreeCtrl(self,size=(200,600))
        self.SyntaxItemToLine=dict()#synatex item and line

        self.mgr.AddPane(self.bottomText,wx.aui.AuiPaneInfo().Bottom())
        self.mgr.AddPane(self.tree,wx.aui.AuiPaneInfo().Left().Layer(1))
        self.mgr.AddPane(self.syntaxTree,wx.aui.AuiPaneInfo().Left().Layer(1))
        self.mgr.AddPane(self.rightText,wx.aui.AuiPaneInfo().Center().Layer(2))
        self.mgr.Update()

        #leftDirs
        self.treeRoot=self.tree.AddRoot('/home/willzhang/wx')
        appendDir(self.tree,self.treeRoot,'/home/willzhang/wx')
        self.tree.Expand(self.treeRoot)

        #menuBar
        menuBar=wx.MenuBar()
        menuProject=wx.Menu()
        menuEdit=wx.Menu()
        menuRun=wx.Menu()
        menuGraph=wx.Menu()
        menuBar.Append(menuProject,u'工程')
        menuBar.Append(menuEdit,u'编辑')
        menuBar.Append(menuRun,u'运行')
        menuBar.Append(menuGraph,u'视图')
        self.SetMenuBar(menuBar)

        #menuProject
        menuProject.Append(1001,u'新建')
        menuProject.Append(1002,u'打开')
        menuEdit.Append(2001,u'保存')
        menuRun.Append(3001,u'编译')
        menuRun.Append(3002,u'运行')
        menuRun.Append(3003,u'编译并运行')
        menuGraph.Append(4001,u'调用关系图')
        menuGraph.Append(4002,u'生成分析树')

        #Bind
        self.Bind(wx.EVT_MENU,self.newProject,id=1001)
        self.Bind(wx.EVT_MENU,self.openProject,id=1002)
        self.tree.Bind(wx.EVT_RIGHT_DOWN,self.RightClick)
        self.tree.Bind(wx.EVT_LEFT_DCLICK,self.LeftDClick)
        self.syntaxTree.Bind(wx.EVT_LEFT_DCLICK,self.SyntaxLeftDClick)
        self.Bind(wx.EVT_MENU,self.saveFile,id=2001)
        self.Bind(wx.EVT_MENU,self.compile,id=3001)
        self.Bind(wx.EVT_MENU,self.exeRun,id=3002)
        self.Bind(wx.EVT_MENU,self.compileAndRun,id=3003)
        self.Bind(wx.EVT_MENU,self.FunctionGraph,id=4001)
        self.Bind(wx.EVT_MENU,self.Tokenizer,id=4002)

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
            self.rightText.SetText(fp.read().decode("utf-8"))
            fp.close()
    def RightClick(self,event):
        self.PopupMenu(MyPopupMenu(self),event.GetPosition())
    def SyntaxLeftDClick(self,event):
        theLine=self.SyntaxItemToLine[self.syntaxTree.GetItemText(self.syntaxTree.GetSelection())]
        #self.rightText.SetInsertionPoint(theLine*824)
        texts=self.rightText.GetText().split('\n')
        cnt=0
        for i in range(theLine):
            cnt+=len(texts[i])+1
        self.rightText.GotoPos(cnt-1)
        #self.rightText.SetInsertionPoint(cnt-1)
    def newProject(self,event):
        self.projectDir=self.GetPath()
        newProjectDialog = wx.TextEntryDialog(self,"",'project name','')
        if newProjectDialog.ShowModal() == wx.ID_OK:
            self.projectName=newProjectDialog.GetValue()
        newProjectDialog.Destroy()
        self.projectDir+=self.projectName+'/'
        os.mkdir(self.projectDir)
        os.system('touch '+self.projectDir+'/.project')
        os.system('cp /home/willzhang/wxpython-aspectcpp/data/wx.ah '+self.projectDir+'/wx.ah')
        self.tree.DeleteAllItems()
        self.treeRoot=self.tree.AddRoot(self.projectName)
        appendProject(self.tree,self.treeRoot,self.projectDir)
        self.tree.Expand(self.treeRoot)
    def openProject(self,event):
        filterFile="All files (.project) |.project"
        openDialog=wx.FileDialog(self,u"选择文件",os.getcwd(),"",filterFile,wx.OPEN)
        if openDialog.ShowModal()==wx.ID_OK:
            self.projectDir=openDialog.GetPath()[:-8]
            self.projectName=self.projectDir.split('/')[-2]
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
                fp.write(self.rightText.GetText().encode('utf-8'))
                fp.close()
            saveDialog.Destroy()
        else:
            fp=open(self.filePath,'w')
            fp.write(self.rightText.GetText().encode('utf-8'))
            fp.close()
    def compile(self,event):
        cmd="ag++ "
        files=open(self.projectDir+'/'+'.project','r').readlines()
        for File in files:
            if File[:-1].endswith('.cpp') or File[:-1].endswith('.cc'):
                cmd+=File[:-1]+' '
        os.chdir(self.projectDir)
        os.system(cmd+' 2>tmpfile')
        compile_info_fp=open('tmpfile','r')
        compile_info=compile_info_fp.read()
        compile_info_fp.close()
        self.bottomText.SetValue(compile_info)
    def exeRun(self,event):
        os.chdir(self.projectDir)
        os.system('./a.out')
    def compileAndRun(self,event):
        self.compile(event)
        self.exeRun(event)
    def FunctionGraph(self,event):
        os.chdir(self.projectDir)
        fp=open('FunctionGraph.dot','w')
        fp.write('digraph G { \n')
        fp.close()
        self.compileAndRun(event)
        fp=open('FunctionGraph.dot','a')
        fp.write('}')
        fp.close();
        os.system("dot -Tpng -o a.png FunctionGraph.dot");
        cmd='xdg-open '+self.projectDir+'a.png'
        os.system(cmd)
    def Tokenizer(self,event):
        os.chdir(self.projectDir)
        cmd='ctags --fields=afmikKlnsStz '+self.filePath
        os.system(cmd)
        tagFile = CTags('tags')
        self.SyntaxItemToLine.clear()
        self.syntaxTree.DeleteAllItems()
        syntaxTreeRoot=self.syntaxTree.AddRoot(self.tree.GetItemText(self.tree.GetSelection()))
        varNode=self.syntaxTree.AppendItem(syntaxTreeRoot,u'变量')
        funcNode=self.syntaxTree.AppendItem(syntaxTreeRoot,u'函数')
        classNode=self.syntaxTree.AppendItem(syntaxTreeRoot,u'类')
        entry=TagEntry()
        while True:
            status = tagFile.next(entry)
            if status:
                if entry['kind'] == 'function':
                    itemID=self.syntaxTree.AppendItem(funcNode,entry['pattern'][2:-2])
                    self.SyntaxItemToLine[self.syntaxTree.GetItemText(itemID)]=entry['lineNumber']
                elif entry['kind'] == 'variable':
                    itemID=self.syntaxTree.AppendItem(varNode,entry['pattern'].split(' ')[0][2:]+' '+entry['name'])
                    self.SyntaxItemToLine[self.syntaxTree.GetItemText(itemID)]=entry['lineNumber']
                elif entry['kind'] == 'class' or entry['kind'] == 'struct':
                    itemID=self.syntaxTree.AppendItem(classNode,entry['pattern'][2:-2])
                    self.SyntaxItemToLine[self.syntaxTree.GetItemText(itemID)]=entry['lineNumber']
                else:
                    pass
            else:
                break
        #keys=self.SyntaxItemToLine.keys()
        #for i in keys:
        #    print i,self.SyntaxItemToLine[i]
        self.syntaxTree.Expand(syntaxTreeRoot)
        self.syntaxTree.Expand(varNode)
        self.syntaxTree.Expand(funcNode)
        self.syntaxTree.Expand(classNode)
class MyApp(wx.App):
    def OnInit(self):
        frame=MyFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return 1
if __name__ == '__main__':
    app=MyApp()
    app.MainLoop()