# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QLabel,
    QSizePolicy, QWidget)

class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(400, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(About.sizePolicy().hasHeightForWidth())
        About.setSizePolicy(sizePolicy)
        About.setMinimumSize(QSize(400, 400))
        About.setMaximumSize(QSize(400, 400))
        self.label = QLabel(About)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 320, 151, 31))
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2 = QLabel(About)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 350, 151, 31))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line = QFrame(About)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 290, 401, 20))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_5 = QLabel(About)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(120, 160, 151, 31))
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_6 = QLabel(About)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 200, 151, 31))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_6.setOpenExternalLinks(True)
        self.label_8 = QLabel(About)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(120, 200, 151, 31))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_9 = QLabel(About)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(240, 200, 151, 31))
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_7 = QLabel(About)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(120, 10, 151, 31))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.label_7.setFont(font2)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_10 = QLabel(About)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(60, 50, 281, 61))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_10.setWordWrap(True)
        self.label_10.setMargin(0)
        self.label_10.setIndent(0)
        self.label_4 = QLabel(About)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(220, 350, 151, 31))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"About", None))
        self.label.setText(QCoreApplication.translate("About", u"Alisher Berik", None))
        self.label_2.setText(QCoreApplication.translate("About", u"Damir Tazhyev", None))
        self.label_5.setText(QCoreApplication.translate("About", u"Used libraries", None))
        self.label_6.setText(QCoreApplication.translate("About", u"OpenCV", None))
        self.label_8.setText("")
        self.label_9.setText(QCoreApplication.translate("About", u"pybind11", None))
        self.label_7.setText(QCoreApplication.translate("About", u"Image Resizer", None))
        self.label_10.setText(QCoreApplication.translate("About", u"A tool for resizing images using classical interpolation methods (Nearest Neighbor, Bilinear, Bicubic, Lanczos) and AI-based super-resolution", None))
        self.label_4.setText(QCoreApplication.translate("About", u"June 2026", None))
    # retranslateUi

