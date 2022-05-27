from pydoc import doc
import sys
from xml.etree.ElementTree import tostring
from PyQt5 import uic
# from PyQt5.QtGui import QImage, QPainter, QPen, QPixmap
# from PyQt5.QtWidgets import QPushButton, QSizePolicy
# from PyQt5.QtWidgets import QFileDialog, QStatusBar
# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

import cv2
import os
import numpy as np
import ffmpeg
import subprocess
from datetime import datetime

ui = uic.loadUiType("VideoMaker.ui")[0]

class MyWindow(QMainWindow, ui):

    def __init__(self):
        self.chosen_points = []
        super().__init__()
        self.setupUi(self)
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.mediaPlayer.setVideoOutput(self.viewer)
        
        self.pb_import.clicked.connect(self.open)
        self.pb_export.clicked.connect(self.save)

        self.listview.clicked.connect(self.preview)
        
        self.radio_1920.setChecked(True)
        self.filelist = None
        self.selectedFile = None
        self.entry = None
        self.srcWidth = 0
        self.srcHeight = 0
        self.dir = None 
        
        self.setAcceptDrops(True)
        
    
    def open(self):
        self.listview.clear()
        if(self.dir==None):
            self.dir = "D:/color/test"
        else:
            self.dir = None
        file_names = QFileDialog.getOpenFileNames(self,
                            "Open Video File",self.dir,'"Videos (*.mp4)')
        self.filelist =list(file_names[0])
        
        for file in self.filelist:
            self.listview.addItem(file)
 
        
    def preview(self, index):

      
        selected  = self.listview.currentItem().text()
        
        print(selected)
        
        if self.selectedFile!='':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(selected)))
        
        self.mediaPlayer.play()
        

            
                    
    def save(self):

        if self.radio_1920.isChecked():
            self.srcWidth = 1920
            self.srcHeight = 1080
        else:
            self.srcWidth = 3840
            self.srcHeight = 2160
          

        listfile = "list.txt"
        f = open(listfile,'w')
        for file in self.filelist:
            f.write("file '"+ file+"'\n")
        f.close()
        
        outputfile = datetime.now().strftime("%m%d-%H_%M_%S")+"_merged.mp4"
        resizeOption = " -vf scale="+str(self.srcWidth)+"x"+str(self.srcHeight)+" "
        print(resizeOption)

        subprocess.run("ffmpeg -f concat -safe 0 -i " + listfile + resizeOption + outputfile) 
   
        print("File merge Done.")
      
      
      
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        self.filelist = [u.toLocalFile() for u in event.mimeData().urls()]

        self.entry = QStandardItemModel()
        for file in self.filelist:
            print(file)
            self.entry.appendRow(QStandardItem(file))
        self.listview.setModel(self.entry)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()