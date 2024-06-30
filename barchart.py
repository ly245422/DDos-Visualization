import sys
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
from PyQt5.QtCore import Qt

class BarChart(QMainWindow):
    def __init__(self, ic, ik, parent=None):
        super(BarChart, self).__init__(parent)

        # # 设置窗口标题
        # self.setWindowTitle('实战 Qt for Python: QChart条形图演示')
        # 设置窗口大小
        self.setGeometry(100, 100, 800, 600)
        # self.resize(800, 600)

        self.createChart(ic, ik)

    def createChart(self, ic, ik):
        # 创建条形图系列
        barSeries = QBarSeries()

        for i in range(len(ic)):
            if i == 0:
                barSet = QBarSet(f"On Cloud")
                self.data = ic[1:]
            else:
                self.data = []
                barSet = QBarSet(f"On Edge Server {i}")
                for j in range(len(ic) - 1):
                    self.data.append(ik[j + 1][i - 1])

            barSet.append(self.data)
            barSeries.append(barSet)
            # print(self.data)

        # 创建图表
        self.chart = QChart()
        self.chart.addSeries(barSeries)
        self.chart.setTitle('防御策略')

        # 设置标题字体加粗
        font = QFont("Swis721 Cn BT", 18)
        font.setBold(True)
        self.chart.setTitleFont(font)

        # 设置坐标轴
        categories = [f"Server {i + 1}" for i in range(len(ic) - 1)]

        axisX = QBarCategoryAxis()
        axisX.append(categories)
        self.chart.addAxis(axisX, Qt.AlignBottom)
        barSeries.attachAxis(axisX)

        axisY = QValueAxis()
        self.chart.addAxis(axisY, Qt.AlignLeft)
        barSeries.attachAxis(axisY)

        # 设置网格线加粗并改为黑色
        # gridLinePen = QPen(QColor("black"))
        # gridLinePen.setWidth(1)
        # axisX.setGridLinePen(gridLinePen)
        # axisY.setGridLinePen(gridLinePen)

        # # 设置坐标轴标签字体加粗并改为黑色
        # axisX.setLabelsFont(QFont("Arial"))
        # # axisX.setLabelsColor(QColor("black"))
        # axisY.setLabelsFont(QFont("Arial"))
        # # axisY.setLabelsColor(QColor("black"))
        axisY.setRange(0, 1)  # 设置Y轴范围为0-1

        # 图例属性
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # 图表视图
        chartView = QChartView(self.chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(chartView)


    def refreshChart(self, ic, ik):
        # 创建条形图系列
        barSeries = QBarSeries()

        for i in range(len(ic)):
            if i == 0:
                barSet = QBarSet(f"On Cloud")
                self.data = ic[1:]
            else:
                self.data = []
                barSet = QBarSet(f"On Edge Server {i}")
                for j in range(len(ic) - 1):
                    self.data.append(ik[j + 1][i - 1])

            barSet.append(self.data)
            barSeries.append(barSet)
            # print(self.data)

        # 创建图表
        self.chart = QChart()
        self.chart.addSeries(barSeries)
        self.chart.setTitle('防御策略')

        # 设置标题字体加粗
        font = QFont("Swis721 Cn BT", 18)
        font.setBold(True)
        self.chart.setTitleFont(font)

        # 设置坐标轴
        categories = [f"Server {i + 1}" for i in range(len(ic) - 1)]

        axisX = QBarCategoryAxis()
        axisX.append(categories)
        self.chart.addAxis(axisX, Qt.AlignBottom)
        barSeries.attachAxis(axisX)

        axisY = QValueAxis()
        self.chart.addAxis(axisY, Qt.AlignLeft)
        barSeries.attachAxis(axisY)

        # 设置网格线加粗并改为黑色
        gridLinePen = QPen(QColor("black"))
        # gridLinePen.setWidth(2)
        axisX.setGridLinePen(gridLinePen)
        axisY.setGridLinePen(gridLinePen)

        # # 设置坐标轴标签字体加粗并改为黑色
        # axisX.setLabelsFont(QFont("Arial", 10, QFont.Bold))
        # axisX.setLabelsColor(QColor("black"))
        # axisY.setLabelsFont(QFont("Arial", 10, QFont.Bold))
        # axisY.setLabelsColor(QColor("black"))
        axisY.setRange(0, 1)  # 设置Y轴范围为0-1

        # 图例属性
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # 图表视图
        chartView = QChartView(self.chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartView)

        # for i in range(len(ic) - 1):
        #     self.data = [ic[i + 1]] + ik[i + 1]  # 将ic[i+1]作为第一个数据添加到数据列表中
        # 这里可以更新图表数据，或者直接调用 update() 方法来刷新窗口部件
        self.update()


if __name__ == '__main__':

    ic = [0, 0.4665625319400025, 0.46656253204331133, 0, 0, 0]
    ik = [[], [0.04665625319400025, 0.04665625319400025, 0.0933125063880005, 0.0933125063880005, 0.186625012776001], [0.04665625320433114, 0.04665625320433114, 0.09331250640866227, 0.09331250640866227, 0.18662501281732455], [0.1, 0.1, 0.2, 0.2, 0.4], [0.1, 0.1, 0.2, 0.2, 0.4], [0.1, 0.1, 0.2, 0.2, 0.4]]
    app = QApplication(sys.argv)
    window = BarChart(ic, ik)
    window.show()
    sys.exit(app.exec())
