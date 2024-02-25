from PySide6.QtWidgets import (QGraphicsItem,
                               QGraphicsPathItem)
from PySide6.QtGui import (QColor, QPen,
                           QPainterPath)
from PySide6.QtCore import (Qt,
                            QPointF)


class Edge:
    def __init__(self, scene, start_item, end_item):
        super().__init__()
        self.scene = scene
        self.start_item = start_item
        self.end_item = end_item

        self.gr_edge = edge(self)
        self.scene.add_edge(self.gr_edge)

        if self.start_item is not None:
            self.update_positions()

    def store(self):
        self.scene.add_edge(self.gr_edge)

    def update_positions(self):
        src_pos = self.start_item.pos()
        patch = self.start_item.width / 2

        self.gr_edge.set_scr(src_pos.x()+patch, src_pos.y()+patch)

        if self.end_item is not None:
            end_pos = self.end_item.pos()
            self.gr_edge.set_dst(end_pos.x() + patch, end_pos.y() + patch)
        else:
            self.gr_edge.set_dst(src_pos.x() + patch, src_pos.y() + patch)
        self.gr_edge.update()

    def remove_from_current_items(self):
        self.end_item = None
        self.start_item = None

    def remove(self):
        self.remove_from_current_items()
        self.scene.remove_edge(self.gr_edge)
        self.gr_edge = None


class edge(QGraphicsPathItem):
    def __init__(self, edge_wrap, parent=None):
        super().__init__(parent)

        self.edge_wrap = edge_wrap
        self.width = 3.0
        self.pos_src = [0,0] #起点
        self.pos_dst = [0,0] #终点

        self._pen = QPen(QColor('#000')) #画线的
        self._pen.setWidthF(self.width) #float

        self._pen_dragging = QPen(QColor('#000')) #拖拽式
        self._pen_dragging.setStyle(Qt.DashDotLine)
        self._pen_dragging.setWidthF(self.width)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1) # 让线条出现在所有图元的最下层

    def set_scr(self, x, y):
        self.pos_src = [x,y]

    def set_dst(self, x, y):
        self.pos_dst = [x,y]

    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))
        path.lineTo(self.pos_dst[0], self.pos_dst[1])
        return path

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        return self.calc_path()

    def paint(self, painter, option, widget=None):
        self.setPath(self.calc_path())
        path = self.path()
        if self.edge_wrap.end_item is None:
            # 包装类中存储了线条开始和结束位置的图元
            # 刚开始拖拽线条时，并没有结束位置的图元，所以是None
            # 这个线条画的是拖拽路径，点线
            painter.setPen(self._pen_dragging)
            painter.drawPath(path)
        else:
            painter.setPen(self._pen)
            painter.drawPath(path)






