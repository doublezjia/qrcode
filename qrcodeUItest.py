# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qrcodeUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
import cv2
from pyzbar import pyzbar

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(523, 460)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelCamera = QtWidgets.QLabel(self.centralwidget)
        self.labelCamera.setGeometry(QtCore.QRect(60, 30, 361, 281))
        self.labelCamera.setObjectName("labelCamera")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 380, 75, 23))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelCamera.setText(_translate("MainWindow", "labelCamera"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

        self.pushButton.clicked.connect(self.Paizhao)
        self.frameThread = FrameThread(0,self.labelCamera)
        self.frameThread.start()

    def Paizhao(self):
        self.frameThread.paizhao = 1


# 摄像头获取图像线程
class FrameThread(QThread):
    imgLab = None
    device = None
    paizhao = 0

    def __init__(self,deviceIndex, imgLab):
        QThread.__init__(self)
        self.imgLab = imgLab
        self.deviceIndex = deviceIndex

        # 初始化，获取图像
        self.device = cv2.VideoCapture(self.deviceIndex)
        # # 视频帧宽高
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)


    def run(self):
        if self.device.isOpened():
            try:
                while True:
                    ret,frame = self.device.read()
                    height, width, bytesPerComponent = frame.shape
                    bytesPerLine = bytesPerComponent * width

                    if self.paizhao == 1:
                        cv2.imwrite('456.jpg',frame)
                        self.paizhao = 0

                    # 识别二维码条形码，把帧转为灰度方便识别
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    self.Decode_qrcode(gray)

                    # 变换彩色空间顺序
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
                    # 转为QImage对象
                    image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(image)

                    # 图像显示的大小
                    pixmap = pixmap.scaled(400, 300, QtCore.Qt.KeepAspectRatio)
                    self.imgLab.setPixmap(pixmap)
            finally:
                self.device.release()

    # 识别二维码
    def Decode_qrcode(self,image):
        barcodes = pyzbar.decode(image)
        for barcode in barcodes:
            # 提取二维码的边界框的位置
            # 画出图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)
            # 提取二维码数据为字节对象，所以如果我们想在输出图像上
            # 画出来，就需要先将它转换成字符串
            barcodeData = barcode.data.decode('utf-8')
            barcodeType = barcode.type

            # 向终端打印二维码类型数据和二维码数据
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        return image