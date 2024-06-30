import math
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint

class Server():
    def __init__(self, commonRequest, pos, capacity):
        self.commonRequest = commonRequest
        self.attackRequest = 0  # 恶意攻击流量
        self.defendRequest = 0 # 防御流量
        self.request = self.attackRequest + self.defendRequest  # 最终处理流量
        self.pos = pos # 服务器位置
        self.capacity = capacity # 服务器处理能力

    def getPos(self): # 得到位置
        return self.pos

    def getCapacity(self): # 得到过滤能力
        return self.capacity

    def getCommonRequest(self): # 得到正常流量
        return self.commonRequest

    def getAttackRequest(self): # 得到攻击流量
        return self.attackRequest

    def getDefendRequest(self): # 得到防御流量
        return self.defendRequest

    def getRequest(self): # 得到总共流量
        self.request = self.attackRequest + self.defendRequest
        return self.request

    def updateAttackRequest(self, attackRequest): # 更新攻击流量
        self.attackRequest = attackRequest

    def updateDefendRequest(self, defendRequest): # 更新防御流量
        self.defendRequest = defendRequest


class ServerDisplay(QWidget):
    def __init__(self, S, totalAttackRequest):
        super(ServerDisplay, self).__init__()
        self.resize(800, 600)
        self.totalAttackRequest = totalAttackRequest
        self.servers = S
        self.setMouseTracking(True)  # 启用鼠标跟踪
        self.cloudImage = QPixmap("figure/cloud_gray.jpg").scaled(180, 140, Qt.KeepAspectRatio)  # 加载并缩小图片

    def paintEvent(self, event):
        painter = QPainter(self)
        size = self.size()

        # 设置圆角矩形的画笔和画刷
        painter.setPen(Qt.NoPen)  # 设置没有边框
        # painter.setBrush(QColor(169, 169, 169, 255))  # 设置灰色填充
        painter.setBrush(QColor(225, 225, 225, 255))  # 设置浅灰色填充

        # 定义圆角矩形的大小和位置
        rect_width = 870
        rect_height = 750
        rect_x = 10
        rect_y = 30
        radius = 90

        # 绘制圆角矩形
        painter.drawRoundedRect(rect_x, rect_y, rect_width, rect_height, radius, radius)

        # 设置画笔宽度
        painter.setPen(QPen(Qt.black, 4))


        # 绘制相邻点之间的线条
        for i in range(len(self.servers)):
            if i == 0:
                continue
            for j in range(i, len(self.servers)):
                if i == j:
                    continue
                # 计算线条的起点和终点
                x = int((self.servers[i].pos[0] / 800) * size.width())
                y = int((self.servers[i].pos[1] / 600) * size.height())
                x1 = int((self.servers[j].pos[0] / 800) * size.width())
                y1 = int((self.servers[j].pos[1] / 600) * size.height())
                if math.sqrt(pow(x-x1,2)+pow(y-y1,2)) < 500:
                    start_point = QPoint(x, y)
                    end_point = QPoint(x1, y1)

                    # 绘制线条
                    painter.drawLine(start_point, end_point)

        data = []
        for i in range(len(self.servers) - 1):
            data.append(self.servers[i + 1].getAttackRequest())
        min_value = round(min(data))
        max_value = round(max(data))
        step = (max_value - min_value) // 5
        legends = []
        bound = []
        for i in range(6):
            lower_bound = min_value + i * step
            upper_bound = min_value + (i + 1) * step
            legends.append(f"{round(lower_bound)} ~ {round(upper_bound)}")
            bound.append(lower_bound)
        # print("bound:", bound)



        # 绘制点
        for i in range(len(self.servers)):
            if i == 0 or self.servers[i].getAttackRequest() < bound[1]:
                pen = QPen(QColor("#A2FFEC"))
            elif self.servers[i].getAttackRequest() > bound[1] and self.servers[i].getAttackRequest() < bound[2]:
                pen = QPen(QColor("#6BE4CC"))
            elif self.servers[i].getAttackRequest() > bound[2] and self.servers[i].getAttackRequest() < bound[3]:
                pen = QPen(QColor("#4A9E8E"))
            elif self.servers[i].getAttackRequest() > bound[3] and self.servers[i].getAttackRequest() < bound[4]:
                pen = QPen(QColor("#459183"))
            else:
                pen = QPen(QColor("#2A5950"))
            pen.setWidth(20)
            painter.setPen(pen)
            x = int((self.servers[i].pos[0] / 800) * size.width())
            y = int((self.servers[i].pos[1] / 600) * size.height())

            if i == 0:
                # 在第一个服务器的位置绘制图片
                painter.drawPixmap(x - self.cloudImage.width() // 2, y - self.cloudImage.height() // 2,
                                   self.cloudImage)
            else:
                # # 绘制点
                # painter.drawPoint(x, y)
                # 绘制圆圈
                # 设置画刷以填充圆形
                painter.setBrush(pen.color())
                # 绘制实心圆
                radius = 5 * round(self.servers[i].getCapacity() / 50)  # 设置圆形半径
                painter.drawEllipse(QPoint(x, y), radius, radius)

        # 绘制图例
        legend_x = size.width() - 300
        legend_y = size.height() - 300
        legend_font = QFont("Swis721 Cn BT", 14)
        legend_font.setWeight(QFont.Bold)
        painter.setFont(legend_font)

        painter.setPen(Qt.black)
        painter.setBrush(QColor("#A2FFEC"))
        painter.drawEllipse(legend_x, legend_y, 20, 20)
        painter.drawText(legend_x + 35, legend_y + 20, legends[0])

        painter.setPen(Qt.black)
        painter.setBrush(QColor("#6BE4CC"))
        painter.drawEllipse(legend_x, legend_y + 40, 20, 20)
        painter.drawText(legend_x + 35, legend_y + 60, legends[1])

        painter.setPen(Qt.black)
        painter.setBrush(QColor("#4A9E8E"))
        painter.drawEllipse(legend_x, legend_y + 80, 20, 20)
        painter.drawText(legend_x + 35, legend_y + 100, legends[2])

        painter.setPen(Qt.black)
        painter.setBrush(QColor("#459183"))
        painter.drawEllipse(legend_x, legend_y + 120, 20, 20)
        painter.drawText(legend_x + 35, legend_y + 140, legends[3])

        painter.setPen(Qt.black)
        painter.setBrush(QColor("#2A5950"))
        painter.drawEllipse(legend_x, legend_y + 160, 20, 20)
        painter.drawText(legend_x + 35, legend_y + 180, legends[4])

        # pen = QPen(QColor("#FF7C80"))
        # pen.setWidth(20)
        # painter.setPen(pen)
        # x = int((self.servers[0].pos[0] / 800) * size.width())
        # y = int((self.servers[0].pos[1] / 600) * size.height())
        # # 绘制点
        # painter.drawPoint(x, y)

        # for i, point in enumerate(self.points):
        #     # 根据点的索引设置画笔颜色
        #     if i == len(self.points) - 1:
        #         pen = QPen(QColor("#FF7C80"))
        #     else:
        #         pen = QPen(QColor("#5DC6B1"))
        #     pen.setWidth(20)
        #     painter.setPen(pen)
        #     x = int((point[0] / 800) * size.width())
        #     y = int((point[1] / 600) * size.height())
        #     # 绘制点
        #     painter.drawPoint(x, y)


        # # 绘制绿色长方形
        # rect_width = 450
        # rect_height = 90
        # rect_x = 870  # 向右移动 20 像素
        # rect_y = 80  # 向下移动 20 像素
        # painter.setPen(Qt.NoPen)  # 无边框
        # painter.setBrush(QColor(74, 158, 142, 200))  # 绿色填充
        # painter.drawRect(rect_x, rect_y, rect_width, rect_height)

        # 绘制灰色圆形
        circle_radius = 140
        circle_center_x = circle_radius + 950  # 向右移动 40 像素
        circle_center_y = circle_radius + 100  # 向下移动 40 像素
        painter.setPen(Qt.NoPen)  # 无边框
        painter.setBrush(QColor(74, 158, 142, 200))  # 灰色填充
        painter.drawEllipse(QPoint(circle_center_x, circle_center_y), circle_radius, circle_radius)

        # 写 total request
        font = QFont("Swis721 Cn BT", 18)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        pen = QPen(Qt.black)  # 设置字体为黑色
        painter.setPen(pen)
        painter.drawText(970, 220, "The total request")
        painter.drawText(1080, 270, "is")

        font = QFont("Swis721 Cn BT", 28)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        pen = QPen(Qt.black)  # 设置字体为黑色
        painter.setPen(pen)
        painter.drawText(1040, 340, str(self.totalAttackRequest))

        painter.end()

    def refreshServerDisplay(self, totalAttackRequest, S):
        self.totalAttackRequest = totalAttackRequest
        self.servers = S
        self.update()

    def mouseMoveEvent(self, event):
        # 获取鼠标当前位置
        mouse_pos = event.pos()
        # 检查鼠标是否在绘制的点附近
        for i in range(len(self.servers)):
            x = int((self.servers[i].getPos()[0] / 800) * self.width())
            y = int((self.servers[i].getPos()[1] / 600) * self.height())
            distance = ((mouse_pos.x() - x) ** 2 + (mouse_pos.y() - y) ** 2) ** 0.5
            if distance < 20:  # 如果鼠标距离点的距离小于20像素，则显示基本信息
                request_info = f"Server {i}\n" + f"Capacity : {self.servers[i].getCapacity()}\n" + f"Common Request : {self.servers[i].getCommonRequest()}\n" + f"Attack Request : {round(self.servers[i].getAttackRequest())}"
                self.setToolTip(request_info)
                return

        # 如果鼠标不在任何点附近，则清空提示信息
        self.setToolTip("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    points = [(150, 300), (350, 300), (550, 300)]  # Example points
    widget = ServerDisplay(points,100)
    widget.show()
    sys.exit(app.exec_())
