
from PyQt5 import QtCore, QtGui, QtWidgets #pip install pyqt5(pip install python3-pyqt5)
from PyQt5.QtWidgets import QPushButton

from gui import info, facegui, trendgui


def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

        MainWindow.setPalette(palette)
        #MainWindow.resize(800, 600)
        MainWindow.showFullScreen()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #-------------------------------------------------------------------------------------
        # maingui.init_main(self, MainWindow)
        # facegui.init_facescan(self, MainWindow)
        
        # maingui.start_mirror(self, MainWindow)
        info.init_info(self, MainWindow)
        facegui.init_hair_gui(self, MainWindow)
        trendgui.init_trend(self, MainWindow)
        #-------------------------------------------------------------------------------------

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

