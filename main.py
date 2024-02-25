import sys
from PySide6.QtWidgets import QApplication,QGraphicsScene,QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from scene import Scene
from view import View

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = Scene(self) # parent=self
        self.view = View(self.scene,self) # scene由view托管


        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        self.setCentralWidget(self.view)
        self.setWindowTitle('Graphics Demo')



app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
