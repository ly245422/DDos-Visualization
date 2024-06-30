import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QFormLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


class PlotCanvas(FigureCanvas):
    def __init__(self, normal_data=None, malicious_data=None, total_traffic=None, parent=None):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.setParent(parent)
        self.plot(normal_data, malicious_data, total_traffic)

    def plot(self, normal_data=None, malicious_data=None, total_traffic=None):
        self.ax.clear()

        # Determine the number of defenders based on the length of normal_data
        num_defenders = len(normal_data)
        defender_indices = np.arange(1, num_defenders + 1)

        # 设置条状图的宽度
        bar_width = 0.3

        # 绘制 Normal Traffic 条状图
        self.ax.bar(defender_indices, normal_data, width=bar_width, label='Normal Traffic', color='skyblue')

        # 绘制 Malicious Traffic 条状图
        self.ax.bar(defender_indices, malicious_data, bottom=normal_data, width=bar_width, label='Malicious Traffic',
                    color='salmon')

        # 绘制 Total Traffic 条状图
        self.ax.bar(defender_indices + bar_width, total_traffic, width=bar_width, label='Total Traffic',
                    color='#4D7AD0')

        self.ax.set_xlabel('Defender Index')
        self.ax.set_ylabel('Traffic')
        self.ax.legend()

        self.draw()


class StackBarChart(QMainWindow):
    def __init__(self, S, ik):
        super().__init__()

        self.setWindowTitle('Traffic Analysis')
        self.resize(800, 600)

        normal_data = [s.getCommonRequest() for s in S[1:]]
        malicious_data = [s.getAttackRequest() for s in S[1:]]
        total = [x + y for x, y in zip(malicious_data, normal_data)]
        print(ik)
        total_malicious_data = []
        for i in range(len(S)-1):
            t = 0
            for j in range(len(S)-1):
                t += ik[j+1][i]*total[i]
            total_malicious_data.append(t)
        # total_malicious_data = [x * y for x, y in zip(total, ik[1:])]
        # print("normal_data:", normal_data)
        # print("malicious_data:", malicious_data)
        # print("ttttt", [x + y for x, y in zip(malicious_data, normal_data)])

        self.canvas = PlotCanvas(normal_data, malicious_data, total_malicious_data)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.canvas)

    def refreshChart(self, S, ik):
        new_normal_data = [s.getCommonRequest() for s in S[1:]]
        new_malicious_data = [s.getAttackRequest() for s in S[1:]]
        total = [x + y for x, y in zip(new_malicious_data, new_normal_data)]
        total_malicious_data = []
        for i in range(len(S) - 1):
            t = 0
            for j in range(len(S) - 1):
                t += ik[j + 1][i] * total[i]
            total_malicious_data.append(t)
        # print("1normal_data:", new_normal_data)
        # print("1malicious_data:", new_malicious_data)
        # print("1ttttt", [x + y for x, y in zip(new_malicious_data, new_normal_data)])

        self.canvas.plot(new_normal_data, new_malicious_data, total_malicious_data)


class MockDefender:
    def __init__(self, common_request, attack_request):
        self.common_request = common_request
        self.attack_request = attack_request

    def getCommonRequest(self):
        return self.common_request

    def getAttackRequest(self):
        return self.attack_request


if __name__ == '__main__':
    # Mock data
    defenders = [MockDefender(1000, 400), MockDefender(900, 450), MockDefender(850, 420), MockDefender(920, 410),
                 MockDefender(880, 430), MockDefender(950, 440), MockDefender(930, 460), MockDefender(870, 470),
                 MockDefender(890, 480), MockDefender(910, 490)]

    app = QApplication(sys.argv)
    mainWin = StackBarChart(defenders)
    mainWin.show()
    sys.exit(app.exec_())
