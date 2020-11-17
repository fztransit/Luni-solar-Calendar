from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# 支持单击的标签
class Label(QLabel):
	clicked = pyqtSignal()  # 设定信号名及参数类型

	def __init__(self, parent=None):
		super(QLabel, self).__init__(parent)
		self.setFont(QFont("family", 15))
		#self.setContentsMargins(15, 15, 15, 15)
		self.setAlignment(Qt.AlignCenter)


	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.clicked.emit()  # 设置信号参数并传入槽函数


# 默认可编辑、带滚动条的下拉列表
class ComboBox(QComboBox):
	wheeled = pyqtSignal()

	def __init__(self, parent=None):
		super(ComboBox, self).__init__(parent)
		self.setEditable(True)
		self.setView(QListView())
		self.setStyleSheet("QComboBox {font: 13px} "
		                   "QComboBox QAbstractItemView::item {min-height: 12px; min-width: 80px; }")
		self.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

	def wheelEvent(self, event):
		index = self.currentIndex()
		super().wheelEvent(event)
		if event.isAccepted() and (index == 0 or index == self.count() - 1):
			self.wheeled.emit()  # 在首尾滚动时发送信号
