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
        #videoWidget = QVideoWidget()
        #self.layout_view.addWidget(videoWidget)
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
        # self.entry = QStandardItemModel()
        # for file in self.filelist:
        #    self.entry.appendRow(QStandardItem(file))
        # self.listview.setModel(self.entry)            
        
        
        
    def preview(self, index):
        # item = self.entry.itemFromIndex(index)
        # idx = item.index().row()
        #self.selectedFile = self.filelist[idx]
        
      
        selected  = self.listview.currentItem().text()
        
        print(selected)
        
        if self.selectedFile!='':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(selected)))
        
        self.mediaPlayer.play()
        
        # if(self.mediaPlayer.mediaChanged(self.selectedFile)):
        #     self.mediaPlayer.play()
        
        # if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
        #     self.mediaPlayer.pause()
        # else:
        #     self.mediaPlayer.play()
       
       
    #label code
        #cap = cv2.VideoCapture(self.selectedFile)
        # while(cap.isOpened()):
        #     ret,frame = cap.read()
        #     if not ret:
        #         print("No frame")
        #         break
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          
        #     h,w,c = frame.shape
        #     qimg = QImage(frame.data,w,h,w*c,QImage.Format_RGB888)
            
        #     pixmap = QPixmap.fromImage(qimg)
        #     p = pixmap.scaled(self.label.size(),Qt.KeepAspectRatio)
        #     self.label.setPixmap(p)
            
                    
    def save(self):
        #video = ffmpeg.input(self.filelist[0])
        if self.radio_1920.isChecked():
            self.srcWidth = 1920
            self.srcHeight = 1080
        else:
            self.srcWidth = 3840
            self.srcHeight = 2160
          
        # list = self.filelist
        # str = ''
        # separtor = '|'
        # for idx, val in enumerate(list):
        #     str += val + ('' if idx == len(list) -1 else separtor)
        # print(str)
        # for file in self.filelist:
        #     do
            
    #     files = []
    #     for file in self.filelist:
    #         files = ffmpeg.input(file)
    #         #files += ffmpeg.input(str(file))
    #    # files += st
    #     print(files)
        listfile = "list.txt"
        f = open(listfile,'w')
        for file in self.filelist:
            f.write("file '"+ file+"'\n")
        f.close()
        
        outputfile = datetime.now().strftime("%m%d-%H_%M_%S")+"_merged.mp4"
        resizeOption = " -vf scale="+str(self.srcWidth)+"x"+str(self.srcHeight)+" "
        print(resizeOption)
        # stream = ffmpeg.input(self.filelist[0])
        # stream = ffmpeg.filter('scale',self.width,-1)
        # stream = ffmpeg.output(stream, 'output.mp4')
        # ffmpeg.run(stream)
        
        #subprocess.run( ["ffmpeg", "-i", self.filelist[0],  "-vf", "scale = 1920x1080", "output.mp4"] )
        #subprocess.run( ["ffmpeg", "-f", "concat", "-i", files, "-c","copy","output2.mp4"] )
        #os.system("ffmpeg -i input.mp4 -vf scale=1920x1080 output.mp4")
        #os.system("ffmpeg -f concat -safe 0 -i <(for f in ./*.mp3; do echo "file '$PWD/$f'"; done) -c copy output.mp4")
        #subprocess.run(["ffmpeg", "-i","\\concat:"+ files+"\\" ,"-c","copy","merged.mp4"])
      #  subprocess.run("ffmpeg -f concat -safe 0 -i " + listfile + resizeOption+ " -c copy "+outputfile) 
        subprocess.run("ffmpeg -f concat -safe 0 -i " + listfile + resizeOption + outputfile) 
   
        print("File merge Done.")
        #subprocess.run("ffmpeg -f concat -i "+ files +"-c copy merged.mp4") 
        #     ffmpeg
        #     .input(self.filelist[0])
        #     .filter('scale',1920,-1)
        #     .output('result.mp4', vframes=1)
        # )
        # video = ffmpeg.input(self.filelist[0])
        # video = ffmpeg.filter('scale',1920,-1)
        # video = ffmpeg.output(video,'output.mp4')
      #  ffmpeg.run(video)
      
      
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