
import sys
import asyncio
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from qtpy import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QApplication, QCheckBox
from PyQt6 import uic
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
import asyncio, logging
from ble_serial.bluetooth.ble_interface import BLE_interface
import re

from ble_serial.scan import main as scanner
from bleak import BleakScanner
from bleak import BleakClient

from PyQt6.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from qasync import QEventLoop

##############################################
class Stream(QtCore.QObject):
    newText = pyqtSignal(str)
    def write(self, text):
        self.newText.emit(str(text))

##############################################

class QMainWindow(QMainWindow):
    set_text_signal = pyqtSignal(str)
    def __init__(self,loop):

        super(QMainWindow,self).__init__()
        self.setWindowTitle("IHM PYTHON V0.7 ")

        self.sensor_names = ['TOF', 'Motor Right', 'Motor Left','LineSensor 1','LineSensor 2','LineSensor 3','LineSensor 4','LineSensor 5']
        self.sensor_values = [0XAA, 0X15, 0X15,0X1,0X1,0X1,0X1,0X1]

        self.setupUi(self)
        self.show()
        sys.stdout = Stream(newText=self.onUpdateText)
        self.var_devices = []
        self.loop = loop
        self.notify_hex_value = 0
        self.client = BleakClient
        self.uui_notify = 0
        self.uui_write = 0
        self.uui_read = 0
        self.notify_task = None

#############################################################################################
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(1252, 796)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1191, 721))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setIconSize(QtCore.QSize(32, 32))
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.Tab_main = QtWidgets.QWidget()
        self.Tab_main.setObjectName("Tab_main")
        self.groupBox_connectionpanel = QtWidgets.QGroupBox(self.Tab_main)
        self.groupBox_connectionpanel.setGeometry(QtCore.QRect(10, 0, 291, 231))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_connectionpanel.setFont(font)
        self.groupBox_connectionpanel.setObjectName("groupBox_connectionpanel")
        self.Combo_Box_peripheric = QtWidgets.QComboBox(self.groupBox_connectionpanel)
        self.Combo_Box_peripheric.setGeometry(QtCore.QRect(240, 70, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.Combo_Box_peripheric.setFont(font)
        self.Combo_Box_peripheric.setTabletTracking(False)
        self.Combo_Box_peripheric.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.Combo_Box_peripheric.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.Combo_Box_peripheric.setAutoFillBackground(False)
        self.Combo_Box_peripheric.setObjectName("Combo_Box_peripheric")
        self.pushButton_connect = QtWidgets.QPushButton(self.groupBox_connectionpanel)
        self.pushButton_connect.setEnabled(False)
        self.pushButton_connect.setGeometry(QtCore.QRect(20, 170, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_connect.setFont(font)
        self.pushButton_connect.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_connect.setCheckable(False)
        self.pushButton_connect.setChecked(False)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.textEdit_connectionstatus = QtWidgets.QTextEdit(self.groupBox_connectionpanel)
        self.textEdit_connectionstatus.setGeometry(QtCore.QRect(20, 30, 261, 71))
        self.textEdit_connectionstatus.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.textEdit_connectionstatus.setObjectName("textEdit_connectionstatus")
        self.pushButton_scan_refresh = QtWidgets.QPushButton(self.groupBox_connectionpanel)
        self.pushButton_scan_refresh.setGeometry(QtCore.QRect(20, 120, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_scan_refresh.setFont(font)
        self.pushButton_scan_refresh.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_scan_refresh.setObjectName("pushButton_scan_refresh")
        self.textEdit_connectionstatus.raise_()
        self.pushButton_connect.raise_()
        self.pushButton_scan_refresh.raise_()
        self.Combo_Box_peripheric.raise_()
        self.groupBox_console = QtWidgets.QGroupBox(self.Tab_main)
        self.groupBox_console.setGeometry(QtCore.QRect(750, 10, 421, 671))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_console.setFont(font)
        self.groupBox_console.setObjectName("groupBox_console")
        self.textEdit_console = QtWidgets.QTextEdit(self.groupBox_console)
        self.textEdit_console.setGeometry(QtCore.QRect(10, 30, 401, 601))
        self.textEdit_console.setObjectName("textEdit_console")
        self.checkBox_savelog = QtWidgets.QCheckBox(self.groupBox_console)
        self.checkBox_savelog.setGeometry(QtCore.QRect(340, 640, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_savelog.setFont(font)
        self.checkBox_savelog.setChecked(True)
        self.checkBox_savelog.setObjectName("checkBox_savelog")
        self.groupBox_highlightedsensor = QtWidgets.QGroupBox(self.Tab_main)
        self.groupBox_highlightedsensor.setGeometry(QtCore.QRect(10, 350, 291, 111))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_highlightedsensor.setFont(font)
        self.groupBox_highlightedsensor.setObjectName("groupBox_highlightedsensor")
        self.textEdit_highlightedsensor = QtWidgets.QTextEdit(self.groupBox_highlightedsensor)
        self.textEdit_highlightedsensor.setGeometry(QtCore.QRect(10, 30, 271, 71))
        self.textEdit_highlightedsensor.setObjectName("textEdit_highlightedsensor")
        self.groupBox_receiveddata = QtWidgets.QGroupBox(self.Tab_main)
        self.groupBox_receiveddata.setGeometry(QtCore.QRect(320, 10, 371, 671))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_receiveddata.setFont(font)
        self.groupBox_receiveddata.setObjectName("groupBox_receiveddata")
        self.tableWidget_receiveddata = QtWidgets.QTableWidget(self.groupBox_receiveddata)
        self.tableWidget_receiveddata.setGeometry(QtCore.QRect(10, 30, 351, 601))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_receiveddata.sizePolicy().hasHeightForWidth())
        self.tableWidget_receiveddata.setSizePolicy(sizePolicy)
        self.tableWidget_receiveddata.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget_receiveddata.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_receiveddata.setShowGrid(True)
        self.tableWidget_receiveddata.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.tableWidget_receiveddata.setCornerButtonEnabled(True)
        self.tableWidget_receiveddata.setRowCount(30)
        self.tableWidget_receiveddata.setColumnCount(6)
        self.tableWidget_receiveddata.setObjectName("tableWidget_receiveddata")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_receiveddata.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_receiveddata.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_receiveddata.setHorizontalHeaderItem(2, item)
        self.tableWidget_receiveddata.horizontalHeader().setVisible(False)
        self.tableWidget_receiveddata.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_receiveddata.horizontalHeader().setDefaultSectionSize(117)
        self.tableWidget_receiveddata.horizontalHeader().setMinimumSectionSize(40)
        self.tableWidget_receiveddata.verticalHeader().setVisible(False)
        self.groupBox_controlpanel = QtWidgets.QGroupBox(self.Tab_main)
        self.groupBox_controlpanel.setGeometry(QtCore.QRect(10, 480, 291, 191))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_controlpanel.setFont(font)
        self.groupBox_controlpanel.setObjectName("groupBox_controlpanel")
        self.checkBox_debugmode = QtWidgets.QCheckBox(self.groupBox_controlpanel)
        self.checkBox_debugmode.setGeometry(QtCore.QRect(20, 30, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_debugmode.setFont(font)
        self.checkBox_debugmode.setChecked(False)
        self.checkBox_debugmode.setObjectName("checkBox_debugmode")
        self.pushButton_UpControl = QtWidgets.QPushButton(self.groupBox_controlpanel)
        self.pushButton_UpControl.setGeometry(QtCore.QRect(160, 30, 61, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_UpControl.setFont(font)
        self.pushButton_UpControl.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_UpControl.setObjectName("pushButton_UpControl")
        self.pushButton_StopControl = QtWidgets.QPushButton(self.groupBox_controlpanel)
        self.pushButton_StopControl.setGeometry(QtCore.QRect(160, 80, 61, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_StopControl.setFont(font)
        self.pushButton_StopControl.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_StopControl.setObjectName("pushButton_StopControl")
        self.pushButton_RightControl = QtWidgets.QPushButton(self.groupBox_controlpanel)
        self.pushButton_RightControl.setGeometry(QtCore.QRect(220, 80, 61, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_RightControl.setFont(font)
        self.pushButton_RightControl.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_RightControl.setObjectName("pushButton_RightControl")
        self.pushButton_LeftControl = QtWidgets.QPushButton(self.groupBox_controlpanel)
        self.pushButton_LeftControl.setGeometry(QtCore.QRect(100, 80, 61, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_LeftControl.setFont(font)
        self.pushButton_LeftControl.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_LeftControl.setObjectName("pushButton_LeftControl")
        self.pushButton_BottomControl = QtWidgets.QPushButton(self.groupBox_controlpanel)
        self.pushButton_BottomControl.setGeometry(QtCore.QRect(160, 130, 61, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_BottomControl.setFont(font)
        self.pushButton_BottomControl.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_BottomControl.setObjectName("pushButton_BottomControl")
        self.checkBox_fct1 = QtWidgets.QCheckBox(self.groupBox_controlpanel)
        self.checkBox_fct1.setGeometry(QtCore.QRect(20, 60, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_fct1.setFont(font)
        self.checkBox_fct1.setChecked(False)
        self.checkBox_fct1.setObjectName("checkBox_fct1")
        self.checkBox_fct2 = QtWidgets.QCheckBox(self.groupBox_controlpanel)
        self.checkBox_fct2.setGeometry(QtCore.QRect(20, 90, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_fct2.setFont(font)
        self.checkBox_fct2.setChecked(False)
        self.checkBox_fct2.setObjectName("checkBox_fct2")
        self.tabWidget.addTab(self.Tab_main, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.Combo_Box_peripheric.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_connectionpanel.setTitle(_translate("MainWindow", "Connection panel :"))
        self.pushButton_connect.setText(_translate("MainWindow", "Connect"))
        self.pushButton_scan_refresh.setText(_translate("MainWindow", "Scan and refresh list"))
        self.groupBox_console.setTitle(_translate("MainWindow", "Console :"))
        self.checkBox_savelog.setToolTip(_translate("MainWindow", "<html><head/><body><p>Permet la lecture/ecriture automatiques des registres lorsque le composant est modifié ou une valeur modifiée</p></body></html>"))
        self.checkBox_savelog.setText(_translate("MainWindow", "SaveLog"))
        self.groupBox_highlightedsensor.setTitle(_translate("MainWindow", "Current TOF detection :"))
        self.groupBox_receiveddata.setTitle(_translate("MainWindow", "Received Datas : "))
        item = self.tableWidget_receiveddata.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Sensor"))
        item = self.tableWidget_receiveddata.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Last Value"))
        item = self.tableWidget_receiveddata.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Current Value"))
        self.groupBox_controlpanel.setTitle(_translate("MainWindow", "Control panel"))
        self.checkBox_debugmode.setToolTip(_translate("MainWindow", "<html><head/><body><p>Permet la lecture/ecriture automatiques des registres lorsque le composant est modifié ou une valeur modifiée</p></body></html>"))
        self.checkBox_debugmode.setText(_translate("MainWindow", "Notify"))
        self.pushButton_UpControl.setText(_translate("MainWindow", "UP"))
        self.pushButton_StopControl.setText(_translate("MainWindow", "STOP"))
        self.pushButton_RightControl.setText(_translate("MainWindow", "Right"))
        self.pushButton_LeftControl.setText(_translate("MainWindow", "Left"))
        self.pushButton_BottomControl.setText(_translate("MainWindow", "Bottom"))
        self.checkBox_fct1.setToolTip(_translate("MainWindow", "<html><head/><body><p>Permet la lecture/ecriture automatiques des registres lorsque le composant est modifié ou une valeur modifiée</p></body></html>"))
        self.checkBox_fct1.setText(_translate("MainWindow", "fct1"))
        self.checkBox_fct2.setToolTip(_translate("MainWindow", "<html><head/><body><p>Permet la lecture/ecriture automatiques des registres lorsque le composant est modifié ou une valeur modifiée</p></body></html>"))
        self.checkBox_fct2.setText(_translate("MainWindow", "fct2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_main), _translate("MainWindow", "GUI Utility for Debug"))
        self.textEdit_connectionstatus.setReadOnly(True)
        self.textEdit_highlightedsensor.setReadOnly(True)
        self.textEdit_console.setReadOnly(True)

        # Définissez le nombre de lignes pour la table
        row_count = len(self.sensor_names)
        # Définissez le nombre de colonnes pour la table (2 colonnes dans ce cas)
        self.tableWidget_receiveddata.setColumnCount(2)
        # Définissez les en-têtes de colonnes
        self.tableWidget_receiveddata.setHorizontalHeaderLabels(['Sensor Name', 'Value'])
        self.tableWidget_receiveddata.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_receiveddata.verticalHeader().setVisible(False)
        self.tableWidget_receiveddata.horizontalHeader().setVisible(True)
        # Ajoutez des lignes à la table
        self.tableWidget_receiveddata.setRowCount(row_count)
        # Bouclez à travers les noms de capteurs et les valeurs et ajoutez-les à la table
        for row_index, (sensor_name, sensor_value) in enumerate(zip(self.sensor_names, self.sensor_values)):
            # Ajoutez le nom de capteur à la première colonne
            sensor_name_item = QtWidgets.QTableWidgetItem(sensor_name)
            self.tableWidget_receiveddata.setItem(row_index, 0, sensor_name_item)
            # Ajoutez la valeur à la deuxième colonne
            sensor_value_item = QtWidgets.QTableWidgetItem(str(sensor_value))
            self.tableWidget_receiveddata.setItem(row_index, 1, sensor_value_item)
        self.tableWidget_receiveddata.resizeColumnsToContents()
        self.tableWidget_receiveddata.resizeRowsToContents()
        self.tableWidget_receiveddata.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

###########################################[FUNCTIONS]#####################################################
        self.pushButton_scan_refresh.clicked.connect(self.func_pushButton_scan_refresh)
        self.pushButton_connect.clicked.connect(self.func_pushButton_connect_selected)

        self.pushButton_UpControl.clicked.connect(self.func_pushButton_UpControl_clicked)
        self.pushButton_UpControl.released.connect(self.func_pushButton_UpControl_released)

        self.pushButton_BottomControl.clicked.connect(self.func_pushButton_DownControl_clicked)
        self.pushButton_BottomControl.released.connect(self.func_pushButton_DownControl_released)

        self.pushButton_LeftControl.clicked.connect(self.func_pushButton_LeftControl_clicked)
        self.pushButton_LeftControl.released.connect(self.func_pushButton_LeftControl_released)

        self.pushButton_RightControl.clicked.connect(self.func_pushButton_RightControl_clicked)
        self.pushButton_RightControl.released.connect(self.func_pushButton_RightControl_released)

        self.pushButton_StopControl.clicked.connect(self.func_pushButton_StopControl_clicked)
        #self.pushButton_StopControl.released.connect(self.func_pushButton_StopControl_released)

        self.checkBox_fct1.stateChanged.connect(self.checkBox_fct1_switched)

        self.Combo_Box_peripheric.currentIndexChanged.connect(self.func_Combo_Box_peripheric_selected)
        self.checkBox_debugmode.stateChanged.connect(self.checkBox_debugmode_switched)
###########################################[END]#####################################################

    def checkBox_fct1_switched(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        address = selected_device[0]
        if (self.checkBox_fct1.isChecked()):
            asyncio.ensure_future(self.ble_write(selected_device[0],0X01,0X05))
            self.pushButton_UpControl.setEnabled(False)
            self.pushButton_BottomControl.setEnabled(False)
            self.pushButton_LeftControl.setEnabled(False)
            self.pushButton_RightControl.setEnabled(False)
            self.checkBox_debugmode.setChecked(False)
        else:
            self.func_pushButton_StopControl_clicked()
            self.pushButton_UpControl.setEnabled(True)
            self.pushButton_BottomControl.setEnabled(True)
            self.pushButton_LeftControl.setEnabled(True)
            self.pushButton_RightControl.setEnabled(True)

    def func_pushButton_StopControl_clicked(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        asyncio.ensure_future(self.ble_write(selected_device[0],0X01,0X00))

    def func_pushButton_UpControl_clicked(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        asyncio.ensure_future(self.ble_write(selected_device[0],0X01,0X01))

    def func_pushButton_UpControl_released(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        #asyncio.ensure_future(self.ble_write(selected_device[0],0X01,0X00))

    def func_pushButton_DownControl_clicked(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        asyncio.ensure_future(self.ble_write(selected_device[0],0X01,0X04))

    def func_pushButton_DownControl_released(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        #asyncio.ensure_future(self.ble_write(selected_device[0],0X01,0X00))

    def func_pushButton_LeftControl_clicked(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        asyncio.ensure_future(self.ble_write(selected_device[0],0X01,0X03))

    def func_pushButton_LeftControl_released(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        #asyncio.ensure_future(self.ble_write(selected_device[0],0X01,0X00))

    def func_pushButton_RightControl_clicked(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        asyncio.ensure_future(self.ble_write(selected_device[0],0X01,0X02))

    def func_pushButton_RightControl_released(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        #asyncio.ensure_future(self.ble_write(selected_device[0],0X01,0X00))

    def notification_handler(self,sender, data):
        text = ("{0}: {1}".format(sender, data))
        print(text)
        value = re.search(r"bytearray\(b'([\x00-\xFF]+)'\)", text).group(1)
        self.notify_hex_value = ''.join([format(ord(c), 'x') for c in value])
        print('readed value is :'+(self.notify_hex_value))

    async def ble_write(self,address,device,value):
        print(f"Sending data.. UUID: " + address, 'value: ',value) 
        async with BleakClient(address) as client:
                if (not client.is_connected):
                    raise "client not connected"
                await client.write_gatt_char('0000fe41-8e22-4541-9d4c-21edae82ed19',bytes([1, value]), response=False)
                await asyncio.sleep(0.1)

    async def notify(self,address):
        self.uui_notify = '0000fe42-8e22-4541-9d4c-21edae82ed19'
        async with BleakClient(address) as self.client:
                if (not self.client.is_connected):
                    raise "client not connected"
        await self.client.connect()
        print(f"Client is: {self.client.is_connected}")
        print(f"[NOTIFY SUBSCRIBING is RUNNING]")
        await self.client.start_notify(self.uui_notify, self.notification_handler)
        try:
            await asyncio.sleep(100)
        except asyncio.CancelledError:
            await self.client.disconnect()
            print('[NOTIFY SUBSCRIBING is DONE]')

    def checkBox_debugmode_switched(self):
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        address = selected_device[0]
        if self.checkBox_debugmode.isChecked():
            if self.notify_task and not self.notify_task.done():
                self.notify_task.cancel()
            self.checkBox_fct1.setChecked(False)
            self.notify_task = asyncio.ensure_future(self.notify(address))
            self.pushButton_UpControl.setEnabled(False)
            self.pushButton_BottomControl.setEnabled(False)
            self.pushButton_LeftControl.setEnabled(False)
            self.pushButton_RightControl.setEnabled(False)
        else:
            if self.notify_task and not self.notify_task.done():
                self.notify_task.cancel()
            self.notify_task = None
            self.pushButton_UpControl.setEnabled(True)
            self.pushButton_BottomControl.setEnabled(True)
            self.pushButton_LeftControl.setEnabled(True)
            self.pushButton_RightControl.setEnabled(True)
            
    async def scan(self):
        async with BleakScanner(timeout = 8) as scanner:
            devices = await scanner.discover()
            self.Combo_Box_peripheric.clear()
            for dev in devices:
                print(" Device %s (%s)" % (dev.name, dev.address))
                self.Combo_Box_peripheric.addItem(str(dev.address)+': '+str(dev.name))
        await asyncio.sleep(1)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.scan())

    async def connect(self,address):
        async with BleakClient(address) as self.client:
                if (not self.client.is_connected):
                    raise "client not connected"
                print(f"Get services..") 
                services = await self.client.get_services()
                for service in services:
                    print(f"Service: {service.uuid}")
                    characteristics = await self.client.get_characteristics(service.uuid)
                for characteristic in characteristics:
                    print(f"\t Characteristic: {characteristic.uuid}")
                    descriptors = await self.client.get_descriptors(characteristic.handle)
                for descriptor in descriptors:
                    print(f"\t\t Descriptor: {descriptor.uuid}")
                    print('service :', service.handle, service.uuid, service.description, )
                    characteristics = service.characteristics
                for char in characteristics:
                    if str(char.properties[0]) == "'read'":
                        self.uui_read = char.uuid
                    elif str(char.properties[0]) == "'write'":
                        self.uui_write = char.uuid
                    elif str(char.properties[0]) == "'notify'":
                        self.uui_notify = char.uuid
                
    def func_pushButton_scan_refresh(self):
        self.Combo_Box_peripheric.clear()
        print("Scan is running.. Please wait few seconds!")
        asyncio.ensure_future(self.scan())
        
    def func_Combo_Box_peripheric_selected(self):
        print("Device : "+ str(self.Combo_Box_peripheric.currentText()) + " selected!")
        self.textEdit_connectionstatus.setPlainText(str(self.Combo_Box_peripheric.currentText()))
        if str(self.Combo_Box_peripheric.currentText()) != "":
            self.pushButton_connect.setEnabled(True)
        else:
            self.pushButton_connect.setEnabled(False)
            
    def func_pushButton_connect_selected(self):
        print("Deep scan is running.. on " + self.Combo_Box_peripheric.currentText() +" device!")
        selected_device = self.Combo_Box_peripheric.currentText().split(':')
        asyncio.ensure_future(self.connect(selected_device[0]))

    ##############################[Fonction retour console]##################################""

    def onUpdateText(self, text):
        cursor = self.textEdit_console.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit_console.setTextCursor(cursor)
        self.textEdit_console.ensureCursorVisible()
        if self.checkBox_savelog.isChecked() == 1:
            with open("log.txt", "a") as f:
                f.write(text)

    def __del__(self):
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    application = QApplication(sys.argv)
    loop = QEventLoop(application)
    asyncio.set_event_loop(loop)
    app = QMainWindow(loop)
    app.show()
    with loop:
        loop.run_forever()