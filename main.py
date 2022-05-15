import sys
from QtUI import *


if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle('Fusion')

	ui = GUI()
	app.exec_()