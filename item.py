from PySide6.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap

from paths import Paths


class Item(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pix = QPixmap(Paths.icon('small_bocchi48.png')) # 设置图片
        self.width = 50
        self.height = 50
        self.setPixmap(self.pix) # 添加图片
        self.setFlag(QGraphicsItem.ItemIsSelectable) # 可选
        self.setFlag(QGraphicsItem.ItemIsMovable) # 可动

    # 当item移动，连接跟随
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for gr_edge in self.scene().edges:
                gr_edge.edge_wrap.update_positions()
        

