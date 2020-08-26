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
from datetime import datetime

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(546, 519)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 391, 331))
        self.groupBox.setObjectName("groupBox")
        self.cameraLabel = QtWidgets.QLabel(self.groupBox)
        self.cameraLabel.setGeometry(QtCore.QRect(10, 20, 371, 291))
        self.cameraLabel.setText("")
        self.cameraLabel.setObjectName("cameraLabel")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 350, 521, 141))
        self.groupBox_2.setObjectName("groupBox_2")
        self.cameraText = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.cameraText.setGeometry(QtCore.QRect(10, 20, 501, 111))
        self.cameraText.setObjectName("cameraText")
        self.cameraText.setReadOnly(True)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(410, 10, 121, 331))
        self.groupBox_3.setObjectName("groupBox_3")
        self.cameraBtn = QtWidgets.QPushButton(self.groupBox_3)
        self.cameraBtn.setGeometry(QtCore.QRect(10, 30, 101, 31))
        self.cameraBtn.setObjectName("cameraBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QrCode"))
        self.groupBox.setTitle(_translate("MainWindow", "画 面"))
        self.groupBox_2.setTitle(_translate("MainWindow", "信 息"))
        self.groupBox_3.setTitle(_translate("MainWindow", "功 能"))
        self.cameraBtn.setText(_translate("MainWindow", "拍 照"))

        self.cameraBtn.clicked.connect(self.Photograph)
        self.frameThread = FrameThread(0, self.cameraLabel)
        self.frameThread.signal.connect(self.cameraTextCallback)
        self.frameThread.start()

    def Photograph(self):
        self.frameThread.photograph = 1

    def cameraTextCallback(self,message):
        if message:
            self.cameraText.appendPlainText(str(message))

# 摄像头获取图像线程
class FrameThread(QThread):
    imgLab = None
    device = None
    photograph = 0

    # 创建信号,括号里填写信号传递的参数
    signal = QtCore.pyqtSignal(str)
    # 创建线程锁
    qmut = QtCore.QMutex()

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
        self.qmut.lock()

        if self.device.isOpened():
            try:
                while True:
                    ret,frame = self.device.read()
                    height, width, bytesPerComponent = frame.shape
                    bytesPerLine = bytesPerComponent * width

                    if self.photograph == 1:
                        photo = '%s.jpg' % datetime.now().strftime('%Y%m%d%H%M%S')
                        cv2.imwrite(photo,frame)
                        self.photograph = 0
                        self.signal.emit('[INFO] Photograph is Successful,The photo is %s' % photo)

                    # 识别二维码条形码，把帧转为灰度方便识别
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    message = self.Decode_qrcode(gray)
                    if message:
                        self.signal.emit(str(message))

                    # 变换彩色空间顺序
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
                    # 转为QImage对象
                    image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(image)

                    pixmap = pixmap.scaled(400, 300, QtCore.Qt.KeepAspectRatio)
                    self.imgLab.setPixmap(pixmap)
            finally:
                self.device.release()

        self.qmut.unlock()

    # 识别二维码
    def Decode_qrcode(self,image):
        message = None
        barcodes = pyzbar.decode(image)

        # for barcode in barcodes:
        #     # 提取二维码的边界框的位置
        #     # 画出图像中条形码的边界框
        #     (x, y, w, h) = barcode.rect
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)
        #     # 提取二维码数据为字节对象，所以如果我们想在输出图像上
        #     # 画出来，就需要先将它转换成字符串
        #     barcodeData = barcode.data.decode('utf-8')
        #     barcodeType = barcode.type
        #
        #     # 向终端打印二维码类型数据和二维码数据
        #     message = "[INFO] Found {} barcode: {}".format(barcodeType, barcodeData)
        #     print(message)
        if barcodes:
            barcodeData = barcodes[0].data.decode('utf-8')
            barcodeType = barcodes[0].type
            message = "[INFO] Found {} barcode: {}".format(barcodeType, barcodeData)
            print(message)
        return message