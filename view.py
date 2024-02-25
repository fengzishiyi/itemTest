from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QPainter

from item import Item
from edge import Edge


class View(QGraphicsView):

    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.gr_scene = scene
        self.parent = parent

        self.edge_enable = False
        self.drag_edge = None

        self.init_ui()

    def init_ui(self):
        self.setScene(self.gr_scene)

        self.setRenderHints(QPainter.Antialiasing |                    # 抗锯齿
                            # QPainter.HighQualityAntialiasing |         # 高品质抗锯齿
                            QPainter.TextAntialiasing |                # 文字抗锯齿
                            QPainter.SmoothPixmapTransform |           # 使图元变换更加平滑
                            QPainter.LosslessImageRendering)           # 不失真的图片渲染

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)            # 设置拖拽模式
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:
            item = Item()
            item.setPos(0, 0)
            self.gr_scene.add_node(item)
        if event.key() == Qt.Key_E:
            self.edge_enable = ~self.edge_enable

    def mousePressEvent(self, event):
        item = self.get_item_at_click(event)
        if event.button() == Qt.RightButton:
            if isinstance(item, Item):
                self.gr_scene.remove_node(item)
        elif self.edge_enable:
            if isinstance(item, Item):
                self.edge_drag_start(item)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.edge_enable:
            self.edge_enable = False
            item = self.get_item_at_click(event)

            if isinstance(item, Item) and item is not self.drag_start_item:
                self.edge_drag_end(item)
            else:
                self.drag_edge.remove()
                self.drag_edge = None
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self.edge_enable and self.drag_edge is not None:
            sc_pos = self.mapToScene(pos)
            self.drag_edge.gr_edge.set_dst(sc_pos.x(), sc_pos.y())
            self.drag_edge.gr_edge.update()
        super().mouseMoveEvent(event)

    def get_item_at_click(self, event):
        pos = event.pos()
        item = self.itemAt(pos)
        return item

    def edge_drag_start(self, item):
        self.drag_start_item = item
        self.drag_edge = Edge(self.gr_scene, self.drag_start_item, None)

    def edge_drag_end(self, item):
        new_edge = Edge(self.gr_scene, self.drag_start_item, item) # 拖拽结束，确定
        self.drag_edge.remove()
        self.drag_edge = None
        new_edge.store()
