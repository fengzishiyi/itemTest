import math

from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import QLine


class Scene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundBrush(QColor('#5F4DA7'))
        self.setSceneRect(0, 0, 500, 500)

        self.nodes = []
        self.edges = []

    # 添加图元
    def add_node(self, node):
        self.nodes.append(node)
        self.addItem(node)

    # 移除图元,连接
    def remove_node(self, node):
        self.nodes.remove(node)
        for edge in self.edges:
            if edge.edge_wrap.start_item is node or edge.edge_wrap.end_item is node:
                self.remove_edge(edge)
        self.removeItem(node)

    # 添加边
    def add_edge(self, edge):
        self.edges.append(edge)
        self.addItem(edge)

    # 移除边
    def remove_edge(self, edge):
        self.edges.remove(edge) # 删列表
        self.removeItem(edge) #删画布
