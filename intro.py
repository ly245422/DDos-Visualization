import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint
import pyqtgraph as pg

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.cloudImage = QPixmap("figure/cloud.jpg").scaled(120, 120, Qt.KeepAspectRatio)  # 加载并缩小图片

    def paintEvent(self, event):
        painter = QPainter(self)

        # 设置画笔宽度
        painter.setPen(QPen(Qt.black, 2))

        # 放置图片
        painter.drawPixmap(190 - self.cloudImage.width() // 2, 130 - self.cloudImage.height() // 2,
                           self.cloudImage)
        # pen = QPen(QColor("#FF7C80"))
        # pen.setWidth(20)
        # painter.setPen(pen)
        # painter.drawPoint(290, 180)

        # 添加 Intro
        font = QFont("Swis721 Cn BT", 24)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        pen = QPen(Qt.black)  # 设置字体为黑色
        painter.setPen(pen)
        painter.drawText(90, 50, "Intro")

        # 在红点下方添加文字
        font = QFont("Swis721 Cn BT", 18)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        pen = QPen(Qt.black) # 设置字体为黑色
        painter.setPen(pen)
        painter.drawText(100, 230, "Cloud Server")

        # 绘制绿点
        pen = QPen(QColor("#5DC6B1"))
        pen.setWidth(20)
        painter.setPen(pen)
        painter.setBrush(pen.color())
        radius = 15
        painter.drawEllipse(QPoint(490, 130), radius, radius)
        # painter.drawPoint(590, 180)

        # 在绿点下方添加文字
        font = QFont("Swis721 Cn BT", 18)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        pen = QPen(Qt.black)  # 设置字体为黑色
        painter.setPen(pen)
        painter.drawText(440, 230, "Server")

def drawIntro():
    widget = MyWidget()
    return widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = drawIntro()
    widget.show()
    sys.exit(app.exec_())


