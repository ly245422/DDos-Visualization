import sys
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice

def on_hover(slice):
    slice.setExploded(not slice.isExploded)
    slice.setLabelVisible(not slice.isLabelVisible())

class PieChart(QMainWindow):
    def __init__(self, S, parent=None):
        super(PieChart, self).__init__(parent)

        # 设置窗口大小
        self.resize(800, 500)

        self.base_color = QColor("#5DC6B1")
        self.createChart(S)

    def createChart(self, S):
        # 设置饼图数据
        self.pieSeries = QPieSeries()
        for i in range(len(S)-1):
            self.pieSeries.append('Server '+str(i+1)+" : "+str(round(S[i+1].getAttackRequest())), S[i+1].getAttackRequest())
        self.pieSeries.hovered.connect(on_hover)

        self.applySliceStyles()

        # 创建图表
        self.chart = QChart()
        self.chart.addSeries(self.pieSeries)
        self.chart.setTitle('DDos 攻击策略')

        # 设置标题字体加粗
        font = QFont("Swis721 Cn BT", 18)
        font.setBold(True)
        self.chart.setTitleFont(font)

        # 设置图例字体大小
        self.chart.legend().setFont(QFont("Arial", 12))
        # 设置图例位置为右侧
        self.chart.legend().setAlignment(Qt.AlignRight)

        # 图表视图
        chartView = QChartView(self.chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartView)

    def applySliceStyles(self):
        # 设置每个饼片的笔刷颜色和透明度
        for i, slice in enumerate(self.pieSeries.slices()):
            # 计算透明度
            alpha = i * 36
            color = self.base_color.lighter(alpha)
            slice.setBrush(color)

    def refreshChart(self, S):
        self.pieSeries.clear()
        for i in range(len(S)-1):
            self.pieSeries.append('Server '+str(i+1)+" : "+str(round(S[i+1].getAttackRequest())), S[i+1].getAttackRequest())
        # self.pieSeries.append('Server1', S[0])
        # self.pieSeries.append('Server2', p2)
        # self.pieSeries.append('Server3', p3)
        # self.pieSeries.append('Server4', p4)
        # self.pieSeries.append('Server5', p5)
        # self.pieSeries.append('Server6', p6)
        # self.pieSeries.append('Server7', p7)
        self.applySliceStyles()
        self.chart.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PieChart()
    window.show()
    sys.exit(app.exec())
