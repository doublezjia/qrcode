#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : zealous (doublezjia@163.com)
# @Date    : 2020/8/20
# @Link    : https://github.com/doublezjia
# @Desc    :

import qrcode
from PIL import Image,ImageEnhance
from pyzbar import pyzbar
import cv2

# 生成二维码
def make_qrcode(imgname):
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_Q,
                       box_size=10,border=4,)
    qr.add_data('hello world')
    qr.make(fit=True)
    img = qr.make_image(fill_color='black',back_color='white')
    img.save('%s.png' % imgname)


# 读取二维码
def decode_qrcode(image):
    # image = Image.open(image)
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        # 提取二维码的边界框的位置
        # 画出图像中条形码的边界框
        (x,y,w,h) = barcode.rect
        cv2.rectangle(image,(x,y),(x + w,y + h),(225,225,225),2)

        # 提取二维码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
        barcodeData = barcode.data.decode('utf-8')
        barcodeType = barcode.type

        # 向终端打印二维码类型数据和二维码数据
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
    return image

# 摄像头
def detect():
    camera = cv2.VideoCapture(0)
    while True:
        ret,frame = camera.read()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = decode_qrcode(frame)
        c = cv2.waitKey(5)
        cv2.imshow('camera',img)
        # # 按q退出
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        # 按esc退出
        if ( c == 27 ):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__' :
    # imgname = '123'
    # # make_qrcode(imgname)
    # deCode = decode_qrcode(imgname)
    # print (deCode)
    detect()
