import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from ui.dashboard import Dashboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL DATA Version Checker")
        self.setGeometry(100, 100, 1000, 700)
        self.setCentralWidget(Dashboard())
        self.setWindowIcon(QIcon('icons/favicon.png'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 