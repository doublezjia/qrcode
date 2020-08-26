#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : zealous (doublezjia@163.com)
# @Date    : 2020/8/20
# @Link    : https://github.com/doublezjia
# @Desc    :

import sys
from qrcodeUI import Ui_MainWindow
from PyQt5 import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.setFixedSize(widget.width(),widget.height())
    widget.show()
    sys.exit(app.exec_())