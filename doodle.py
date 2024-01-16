import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsPathItem
from PyQt6.QtGui import QImage, QPixmap, QPainterPath, QPen, QColor
from PyQt6.QtCore import Qt

class DoodleView(QGraphicsView):
    def __init__(self, image=None):
        super().__init__()

        self.enabled = True
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.drawing_path = QPainterPath()
        self.pen = QPen(QColor(Qt.GlobalColor.red), 2)

        self.current_path_item = None

        if image is not None:
            pixmap = QPixmap(image)
            self.scene.addPixmap(pixmap)

    def mousePressEvent(self, event):
        if self.enabled:
            self.drawing_path.moveTo(event.pos().x(), event.pos().y())
            self.current_path_item = QGraphicsPathItem(self.drawing_path)
            self.current_path_item.setPen(self.pen)
            self.scene.addItem(self.current_path_item)

    def mouseMoveEvent(self, event):
        if self.current_path_item is not None and self.enabled:
            self.drawing_path.lineTo(event.pos().x(), event.pos().y())
            self.current_path_item.setPath(self.drawing_path)

    def mouseReleaseEvent(self, event):
        if self.enabled:
            self.current_path_item = None

class DoodleWidget(QApplication):
    def __init__(self, image):
        super().__init__(sys.argv)

        self.doodle_view = DoodleView(image)
        self.doodle_view.show()

if __name__ == "__main__":
    image = QImage("F:/PythonProject/Updated2/Kena.png")  # Replace with the path to your image
    doodle_app = DoodleWidget(image)
    sys.exit(doodle_app.exec())
