import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from Круги import Ui_MainWindow
from PyQt5.QtGui import QPainter, QColor
import PIL


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.around)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawFlag(qp)
        qp.end()

    def around(self):
        x = random.randint(0, 1131)
        y = random.randint(0, 748)
        PIL.ImageDraw.ellipse([x, y, x + random.randint(10, 50), y + random.randint(10, 50)])

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
