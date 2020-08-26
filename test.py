#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : zealous (doublezjia@163.com)
# @Date    : 2020/8/21
# @Link    : https://github.com/doublezjia
# @Desc    :


import sys
from PyQt5 import QtCore

import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton


def getCameraNum():
    """获取摄像头数量"""
    num = 0
    for i in range(0, 5):
        # 从摄像头中取得视频
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            num += 1
        cap.release()
    return num


class FrameThread(QThread):
    imgLab = None
    device = None
    paizhao = 0

    """摄像头拍照线程，摄像头拍照耗时较长容易卡住UI"""

    def __init__(self, deviceIndex, imgLab):
        QThread.__init__(self)
        self.imgLab = imgLab
        self.deviceIndex = deviceIndex

        self.device = cv2.VideoCapture(self.deviceIndex)  # 从摄像头中取得视频
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

    def run(self):
        if self.device.isOpened():
            try:
                while True:
                    ret, frame = self.device.read()
                    height, width, bytesPerComponent = frame.shape
                    bytesPerLine = bytesPerComponent * width
                    # 变换彩色空间顺序
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
                    # 转为QImage对象
                    image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
                    if self.paizhao == 1:
                        image.save("C:\\img" + str(self.deviceIndex) + ".jpg")
                        self.paizhao = 0
                    pixmap = QPixmap.fromImage(image)
                    pixmap = pixmap.scaled(400, 300, QtCore.Qt.KeepAspectRatio)
                    self.imgLab.setPixmap(pixmap)
            finally:
                self.device.release()
        # if self.cap.isOpened():
        #     # 获取视频播放界面长宽
        #     width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        #     height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        #     # 定义编码器 创建 VideoWriter 对象
        #     while (self.cap.isOpened()):
        #         # 读取帧摄像头
        #         ret, frame = self.cap.read()
        #         image = QtGui.QImage(frame, width, height, QtGui.QImage.Format_Indexed8)
        #         pixmap = QtGui.QPixmap.fromImage(image.mirrored(False, True))
        #         # pixmap = QPixmap('C:\left.jpg')
        #         self.imgLab.setPixmap(pixmap)

    def destroyed(self, QObject=None):
        self.device.release()


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        lb1 = QLabel(self)
        lb2 = QLabel(self)
        btn = QPushButton(self)
        btn.setText("拍照")
        btn.clicked.connect(self.paizhao)

        self.frameThread = FrameThread(0, lb1)
        self.frameThread.start()

        self.frameThread2 = FrameThread(1, lb2)
        self.frameThread2.start()

        hbox.addWidget(lb1)
        hbox.addWidget(lb2)
        hbox.addWidget(btn)
        self.setLayout(hbox)

        self.move(300, 300)
        self.setWindowTitle('像素图控件')
        self.show()

    def paizhao(self):
        self.frameThread.paizhao = 1
        self.frameThread2.paizhao = 1

    def showDate(self, date):
        self.lb1.setText(date.toString())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())