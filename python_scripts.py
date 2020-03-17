import sys
from qtpy import QtGui, QtCore, QtWidgets
from os import listdir, system
from os.path import isfile, join
import subprocess, platform
from functools import partial
import json
import os

class Python_Scripts_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Python_Scripts_Window,self).__init__()
        dirpath = self.getDirPath()
        try:
            fileList = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
            pythonScriptsList, docList = self.classifyFiles(fileList)
            
            if len(pythonScriptsList) > 0 and dirpath is not None:
                scriptlayout = QtWidgets.QVBoxLayout()
                doclayout = QtWidgets.QVBoxLayout()
                scriptbox = QtWidgets.QGroupBox("Python example scripts")
                docbox = QtWidgets.QGroupBox("Documentation")
                mainbox = QtWidgets.QVBoxLayout()
           
                listButtons = []
                for elem in pythonScriptsList:
                    b = QtWidgets.QPushButton(elem[0:-3])
                    b.clicked.connect(partial(self.startScript, join(dirpath, elem)))
                    listButtons.append(b)
                    scriptlayout.addWidget(listButtons[-1])
                    scriptlayout.addStretch()
               
                scriptbox.setLayout(scriptlayout)
                mainbox.addWidget(scriptbox)
           
                if len(docList)>0:
                    for elem in docList:
                        b = QtWidgets.QPushButton(elem[0:-3])
                        b.clicked.connect(partial(self.openTextFile, join(dirpath, elem)))
                        listButtons.append(b)
                        doclayout.addWidget(listButtons[-1])
                        doclayout.addStretch()
                   
                    docbox.setLayout(doclayout)
                    mainbox.addWidget(docbox)
           
                self.setCentralWidget(QtWidgets.QWidget(self))
                self.centralWidget().setLayout(mainbox)
           
                self.setWindowTitle("Python example scripts")
                self.setFixedSize(450,self.sizeHint().height())
           
                self.show()
            else:
                QtWidgets.QMessageBox.critical(None,'Error','No script was found. Is the directory correctly specified?',QtWidgets.QMessageBox.Cancel)
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(None,'Error','Directory was not found. Is the directory correctly specified?',QtWidgets.QMessageBox.Cancel)
       
    def classifyFiles(self,fileList):
        pythonScriptsList = []
        docList = []
        for elem in fileList:
            if elem[-3:] == ".py" and elem != "__init__.py":
                pythonScriptsList.append(elem)
            elif elem[-3:] == ".md":
                docList.append(elem)
        return pythonScriptsList, docList
    
    def startScript(self,filepath):
        if platform.system() == 'Darwin':       # macOS
            cmd = r'directory=$(pwd); osascript -e "tell app \"terminal\" to do script \"cd $directory; python ' + filepath + r'\""'
            p = subprocess.call(cmd, shell=True)
        elif platform.system() == 'Windows':    # Windows
            p = subprocess.call('start "" ' + filepath, shell=True)
        else:                                   # linux variants
            p = subprocess.call(['gnome-terminal -- python ' + filepath], shell=True)
        
        return p
    
    def openTextFile(self,filepath):
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open -a TextEdit ' + filepath), shell=True)
        elif platform.system() == 'Windows':    # Windows
            from os import startfile
            startfile(filepath)
        else:                                   # linux variants
            system('xdg-open ' + filepath)
            
    def getDirPath(self):
        path = None
        try:
            with open('config.json') as json_data_file:
                data = json.load(json_data_file)
                path = data["dirpath"]
        
        except IOError:
            QtWidgets.QMessageBox.critical(None,'Error','Configuration file was not found.',QtWidgets.QMessageBox.Cancel)
            
        except (json.JSONDecodeError, TypeError):
            QtWidgets.QMessageBox.critical(None,'Error','Unreadable configuration file.',QtWidgets.QMessageBox.Cancel)

        return path

if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    window = Python_Scripts_Window()
    sys.exit(app.exec_())
