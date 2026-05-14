# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSplitter, QToolBox, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1000, 682)
        self.mainLayout = QVBoxLayout(Widget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.topBar = QHBoxLayout()
        self.topBar.setObjectName(u"topBar")
        self.selectPlottingFileButton = QPushButton(Widget)
        self.selectPlottingFileButton.setObjectName(u"selectPlottingFileButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectPlottingFileButton.sizePolicy().hasHeightForWidth())
        self.selectPlottingFileButton.setSizePolicy(sizePolicy)

        self.topBar.addWidget(self.selectPlottingFileButton)

        self.filePathLabel = QLabel(Widget)
        self.filePathLabel.setObjectName(u"filePathLabel")
        sizePolicy.setHeightForWidth(self.filePathLabel.sizePolicy().hasHeightForWidth())
        self.filePathLabel.setSizePolicy(sizePolicy)

        self.topBar.addWidget(self.filePathLabel)

        self.topSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBar.addItem(self.topSpacer)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.topBar.addItem(self.horizontalSpacer)

        self.loadConfButton = QPushButton(Widget)
        self.loadConfButton.setObjectName(u"loadConfButton")

        self.topBar.addWidget(self.loadConfButton)

        self.saveConfButton = QPushButton(Widget)
        self.saveConfButton.setObjectName(u"saveConfButton")

        self.topBar.addWidget(self.saveConfButton)

        self.helpButton = QPushButton(Widget)
        self.helpButton.setObjectName(u"helpButton")

        self.topBar.addWidget(self.helpButton)


        self.mainLayout.addLayout(self.topBar)

        self.mainSplitter = QSplitter(Widget)
        self.mainSplitter.setObjectName(u"mainSplitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mainSplitter.sizePolicy().hasHeightForWidth())
        self.mainSplitter.setSizePolicy(sizePolicy1)
        self.mainSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.leftPanel = QWidget(self.mainSplitter)
        self.leftPanel.setObjectName(u"leftPanel")
        self.leftLayout = QVBoxLayout(self.leftPanel)
        self.leftLayout.setObjectName(u"leftLayout")
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.fileRow = QHBoxLayout()
        self.fileRow.setObjectName(u"fileRow")

        self.leftLayout.addLayout(self.fileRow)

        self.plotArea = QFrame(self.leftPanel)
        self.plotArea.setObjectName(u"plotArea")
        sizePolicy1.setHeightForWidth(self.plotArea.sizePolicy().hasHeightForWidth())
        self.plotArea.setSizePolicy(sizePolicy1)
        self.plotArea.setFrameShape(QFrame.Shape.StyledPanel)
        self.plotLayout = QVBoxLayout(self.plotArea)
        self.plotLayout.setObjectName(u"plotLayout")

        self.leftLayout.addWidget(self.plotArea)

        self.mainSplitter.addWidget(self.leftPanel)
        self.rightPanel = QWidget(self.mainSplitter)
        self.rightPanel.setObjectName(u"rightPanel")
        self.rightPanelLayout = QVBoxLayout(self.rightPanel)
        self.rightPanelLayout.setObjectName(u"rightPanelLayout")
        self.rightPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.rightToolBox = QToolBox(self.rightPanel)
        self.rightToolBox.setObjectName(u"rightToolBox")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.elementsLayout = QVBoxLayout(self.page_1)
        self.elementsLayout.setObjectName(u"elementsLayout")
        self.SelectElements = QToolButton(self.page_1)
        self.SelectElements.setObjectName(u"SelectElements")

        self.elementsLayout.addWidget(self.SelectElements)

        self.elementsScrollArea = QScrollArea(self.page_1)
        self.elementsScrollArea.setObjectName(u"elementsScrollArea")
        self.elementsScrollArea.setWidgetResizable(True)
        self.elementsContainer = QWidget()
        self.elementsContainer.setObjectName(u"elementsContainer")
        self.elementsContainer.setGeometry(QRect(0, 0, 905, 448))
        self.tab2_layout = QGridLayout(self.elementsContainer)
        self.tab2_layout.setObjectName(u"tab2_layout")
        self.elementsScrollArea.setWidget(self.elementsContainer)

        self.elementsLayout.addWidget(self.elementsScrollArea)

        self.rightToolBox.addItem(self.page_1, u"Elements")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.simpleParamsLayout = QGridLayout(self.page_3)
        self.simpleParamsLayout.setObjectName(u"simpleParamsLayout")
        self.rightToolBox.addItem(self.page_3, u"Parameters")
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.iterLayout = QVBoxLayout(self.page_4)
        self.iterLayout.setObjectName(u"iterLayout")
        self.rightToolBox.addItem(self.page_4, u"Iterlist")

        self.rightPanelLayout.addWidget(self.rightToolBox)

        self.mainSplitter.addWidget(self.rightPanel)

        self.mainLayout.addWidget(self.mainSplitter)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Zeeman config maker", None))
        self.selectPlottingFileButton.setText(QCoreApplication.translate("Widget", u"Select File to Plot", None))
        self.filePathLabel.setText(QCoreApplication.translate("Widget", u"No file selected", None))
        self.loadConfButton.setText(QCoreApplication.translate("Widget", u"Load Configuration", None))
        self.saveConfButton.setText(QCoreApplication.translate("Widget", u"Save Configuration", None))
        self.helpButton.setText(QCoreApplication.translate("Widget", u"Help", None))
        self.SelectElements.setText(QCoreApplication.translate("Widget", u"Select Elements", None))
        self.rightToolBox.setItemText(self.rightToolBox.indexOf(self.page_1), QCoreApplication.translate("Widget", u"Elements", None))
        self.rightToolBox.setItemText(self.rightToolBox.indexOf(self.page_3), QCoreApplication.translate("Widget", u"Parameters", None))
        self.rightToolBox.setItemText(self.rightToolBox.indexOf(self.page_4), QCoreApplication.translate("Widget", u"Iterlist", None))
    # retranslateUi

