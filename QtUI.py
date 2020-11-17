from CustomizeWidgets import *
from PerpetualCalendar import *

class GUI(QMainWindow):
	def __init__(self):
		super().__init__()
		self.wnlWidget = QWidget()
		self.setupUI()

	def setupUI(self):
		pe = QPalette()
		pe.setColor(QPalette.Window, QColor(250, 255, 255))  # F0FFFF、FFFAFA、FFFAF0
		self.setPalette(pe)
		self.setFixedSize(470, 380)
		self.setWindowTitle("万年历")
		self.setCentralWidget(self.wnlWidget)
		self.calendarUI()

		displayDate(self)
		self.show()

	def calendarUI(self):
		self.gridWNL = QGridLayout()
		self.wnlWidget.setLayout(self.gridWNL)
		self.gridWNL.setSpacing(0)
		self.hlayWNL = QHBoxLayout()
		self.hlayWNL.setContentsMargins(3, 0, 5, 0)
		self.gridWNL.addLayout(self.hlayWNL, 0, 0, 1, 7)
		self.cblCentury = ComboBox()
		for i in range(startCentury, endCentury+1):
			if i < 0: self.cblCentury.addItem('BC' + str(abs(i)) + '世纪')
			elif i == 0: continue
			else: self.cblCentury.addItem(str(i) + '世纪')
		self.cblCentury.currentIndexChanged.connect(lambda : yearItems(self))
		self.cblCentury.activated.connect(lambda : displayDate(self))
		self.cblCentury.setMaximumWidth(80)
		self.cblCentury.setFocusPolicy(False)
		self.hlayWNL.addWidget(self.cblCentury)
		self.cblYear = ComboBox()
		self.cblYear.setFixedWidth(82)
		self.btnLastYear = QPushButton('<')
		self.btnNextYear = QPushButton('>')
		self.cblYear.activated.connect(lambda : displayDate(self))
		self.cblYear.wheeled.connect(lambda :jumpYear(self))
		self.btnLastYear.clicked.connect(self.thisJumpMonth)
		self.btnNextYear.clicked.connect(self.thisJumpMonth)
		self.btnLastYear.setMaximumSize(16, 22)
		self.btnNextYear.setMaximumSize(16, 22)
		self.hlayWNL.addStretch()
		self.hlayWNL.addWidget(self.btnLastYear)
		self.hlayWNL.addWidget(self.cblYear)
		self.hlayWNL.addWidget(self.btnNextYear)
		self.cblMonth = ComboBox()
		for i in range(12):
			self.cblMonth.addItem(str(i + 1) + '月')
		self.cblMonth.setMaxVisibleItems(12)
		self.cblMonth.setFocusPolicy(False)
		self.cblMonth.setMaximumWidth(60)
		self.btnLastMonth = QPushButton("<")
		self.btnNextMonth = QPushButton(">")
		self.cblMonth.activated.connect(lambda : displayDate(self))
		self.cblMonth.wheeled.connect(lambda :jumpMonth(self))
		self.btnLastMonth.clicked.connect(self.thisJumpMonth)
		self.btnNextMonth.clicked.connect(self.thisJumpMonth)
		self.btnLastMonth.setMaximumSize(16, 22)
		self.btnNextMonth.setMaximumSize(16, 22)
		self.hlayWNL.addStretch()
		self.hlayWNL.addWidget(self.btnLastMonth)
		self.hlayWNL.addWidget(self.cblMonth)
		self.hlayWNL.addWidget(self.btnNextMonth)
		self.hlayWNL.addStretch()
		self.btnToday = QPushButton("今日")
		self.btnToday.clicked.connect(lambda : displayDate(self))
		self.btnToday.setMaximumWidth(36)
		self.hlayWNL.addWidget(self.btnToday)
		self.labMonday = Label("一")
		self.labTuesday = Label("二")
		self.labWednesday = Label("三")
		self.labThursday = Label("四")
		self.labFriday = Label("五")
		self.labSaturday = Label("六")
		self.labSunday = Label("日")
		labWeeks = [self.labMonday, self.labTuesday, self.labWednesday, self.labThursday, self.labFriday, self.labSaturday, self.labSunday]
		for i in range(7):
			self.gridWNL.addWidget(labWeeks[i], 1, i)
			labWeeks[i].setMaximumHeight(40)
		self.lab00, self.lab01, self.lab02, self.lab03, self.lab04, self.lab05, self.lab06 = Label(), Label(), Label(), Label(), Label(), Label(), Label()
		self.lab10, self.lab11, self.lab12, self.lab13, self.lab14, self.lab15, self.lab16 = Label(), Label(), Label(), Label(), Label(), Label(), Label()
		self.lab20, self.lab21, self.lab22, self.lab23, self.lab24, self.lab25, self.lab26 = Label(), Label(), Label(), Label(), Label(), Label(), Label()
		self.lab30, self.lab31, self.lab32, self.lab33, self.lab34, self.lab35, self.lab36 = Label(), Label(), Label(), Label(), Label(), Label(), Label()
		self.lab40, self.lab41, self.lab42, self.lab43, self.lab44, self.lab45, self.lab46 = Label(), Label(), Label(), Label(), Label(), Label(), Label()
		self.lab50, self.lab51, self.lab52, self.lab53, self.lab54, self.lab55, self.lab56 = Label(), Label(), Label(), Label(), Label(), Label(), Label()
		self.labs = [[self.lab00, self.lab01, self.lab02, self.lab03, self.lab04, self.lab05, self.lab06],
		        [self.lab10, self.lab11, self.lab12, self.lab13, self.lab14, self.lab15, self.lab16],
		        [self.lab20, self.lab21, self.lab22, self.lab23, self.lab24, self.lab25, self.lab26],
		        [self.lab30, self.lab31, self.lab32, self.lab33, self.lab34, self.lab35, self.lab36],
		        [self.lab40, self.lab41, self.lab42, self.lab43, self.lab44, self.lab45, self.lab46],
		        [self.lab50, self.lab51, self.lab52, self.lab53, self.lab54, self.lab55, self.lab56], ]
		for i in range(6):
			for j in range(7):
				self.labs[i][j].setFixedSize(48, 48)
				self.labs[i][j].clicked.connect(lambda : displayDate(self))
				self.gridWNL.addWidget(self.labs[i][j], i + 2, j)
		self.labInfo = QLabel()
		self.labInfo.setStyleSheet("QLabel{ font:14px; }")
		self.labInfo.setAlignment(Qt.AlignHCenter)
		self.labInfo.setContentsMargins(0, 6, 5, 6)
		self.labInfo.setWordWrap(True)
		self.labInfo.setFixedWidth(120)
		self.gridWNL.addWidget(self.labInfo, 0, 7, 8, 1)

	def thisJumpMonth(self):
		if self.sender() == self.btnLastMonth:
			lastMonth(self)
		elif self.sender() == self.btnNextMonth:
			nextMonth(self)
		elif self.sender() == self.btnLastYear:
			lastYear(self)
		elif self.sender() == self.btnNextYear:
			nextYear(self)
		displayDate(self)