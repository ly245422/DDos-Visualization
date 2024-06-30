import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor, QFont
from server import ServerDisplay, Server
from intro import drawIntro
from StackBarChart import StackBarChart
from piechart import PieChart
from barchart import BarChart
from Defend import Defend
from Attack import Attack

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serverNum = 5 # 初始化总服务器个数
        self.cloudNum = 1 # 初始化云服务器个数
        self.totalAttackRequest = 3000  # 初始化总恶意请求个数
        self.commonRequest = initCommonRequest(self.serverNum)  # 初始化正常流量
        self.capacity = initCapacity(self.serverNum) # 初始化过滤能力
        locs = generateServerPositions(self.serverNum) # 初始化服务器位置

        # 初始化服务器 （位置、正常请求数量、处理能力）
        self.S = []
        self.S = initServer(pos=locs, commonRequest=self.commonRequest, capacity=self.capacity)  # 总 S

        # 初始化恶意攻击流量
        self.attackRequests = Attack(totalAttackRequests=self.totalAttackRequest, serverNum=self.serverNum, servers=self.S)
        print("attackRequests:", self.attackRequests)
        # 设定服务器的攻击流量
        self.S = attackServer(self.attackRequests, self.S)

        # 经过  分配策略的请求数量
        # defendRequests, ic, ik = Defend(self.commonRequest, attackRequests, self.capacity, wc=0.01, num=self.serverNum)
        self.ic, self.ik = Defend(serverNum=self.serverNum, servers=self.S)
        # print("ic", self.ic)
        # print("ik", self.ik)

        # 设定服务器的防御流量
        # self.S = defendServer(defendRequests, self.S)

        # 界面设计
        # 定义总界面
        self.setWindowTitle("Demo")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 设置背景颜色为白色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('white'))
        self.setPalette(palette)
        central_widget.setAutoFillBackground(True)
        central_widget.setPalette(palette)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # 创建第一列布局
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, 6)

        # 创建 Label 1 位置的控件 标题 并添加到布局中
        title = QFont("Swis721 Cn BT", 24)
        title.setWeight(QFont.Bold)  # 设置字体加粗
        label1 = QLabel("\n           AN APPROACH TO SOLVE EC DDOS ATTACK\n")
        label1.setFont(title)
        left_layout.addWidget(label1, 1)

        # 创建第一列上部布局
        left_top_layout = QHBoxLayout()

        # 创建输入部分
        input_font = QFont("Swis721 Cn BT", 18)
        input_font.setWeight(QFont.Bold)

        input_layout = QFormLayout()

        label2 = QLabel("  输入攻击总请求个数:")
        label2.setFont(input_font)
        self.requests_num = QLineEdit()
        self.requests_num.setFixedHeight(80)
        self.requests_num.setFont(QFont("Swis721 Cn BT", 14))  # 设置输入框内文字的字体和大小
        self.requests_num.setStyleSheet("border: 1.5px solid #ccc; padding: 5px;")
        input_layout.addRow(label2, self.requests_num)

        label3 = QLabel("  输入服务器个数:")
        label3.setFont(input_font)
        self.num = QLineEdit()
        self.num.setFixedHeight(80)
        self.num.setFont(QFont("Swis721 Cn BT", 14))  # 设置输入框内文字的字体和大小
        self.num.setStyleSheet("border: 1.5px solid #ccc; padding: 5px;")
        input_layout.addRow(label3, self.num)

        self.btn = QPushButton('确认')
        self.btn.setFixedHeight(90)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #459183;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 30px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2A5950;
            }
        """)
        input_layout.addRow(self.btn)
        self.btn.clicked.connect(self.onButtonClick)

        left_top_layout.addLayout(input_layout, 2)

        # 创建 Label 5、Label 6 位置的控件 介绍 并添加到布局中
        intro = drawIntro()
        left_top_layout.addWidget(intro, 2)

        left_layout.addLayout(left_top_layout, 2)

        # 在 Label 3 下方添加横线
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        left_layout.addWidget(line1)

        # 创建 Label 4 位置的控件 服务器
        self.serverDisplay = ServerDisplay(self.S, self.totalAttackRequest)
        left_layout.addWidget(self.serverDisplay, 6)

        # 创建第二列布局
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, 4)

        # 创建 Label 7 位置的控件 饼图 并添加到布局中
        self.PieChart = PieChart(self.S)
        right_layout.addWidget(self.PieChart, 3)

        # 创建 Label 8 位置的控件 条形图 并添加到布局中
        self.BarChart = BarChart(self.ic, self.ik)
        right_layout.addWidget(self.BarChart, 3)

        # 创建 Label 6 位置的控件 堆栈条形图 并添加到布局中
        self.stackBarChart = StackBarChart(self.S, self.ik)
        right_layout.addWidget(self.stackBarChart, 3)

        # 调整各列的拉伸策略
        left_layout.setContentsMargins(0, 0, 10, 0)  # 添加一些间距
        right_layout.setContentsMargins(10, 0, 0, 0)  # 添加一些间距

        # 设置左侧布局的拉伸因子，使第一个 label 占 1/3，第二个 label 占 2/3
        left_layout.setStretch(0, 1)
        left_layout.setStretch(1, 2)
        com = []
        # for i in range(len(self.S)-1):
        #     com.append(round(self.S[i+1].getRequest()))
        # print("ewwcw", com)


    def onButtonClick(self): # 计算结果并显示
        if self.serverNum != int(self.num.text()):
            self.serverNum = int(self.num.text())
            locs = generateServerPositions(self.serverNum)
            self.commonRequest = initCommonRequest(self.serverNum)  # 初始化正常流量
            self.capacity = initCapacity(self.serverNum)  # 初始化过滤能力
            self.S = initServer(pos=locs, commonRequest=self.commonRequest, capacity=self.capacity)  # 总 S
        self.totalAttackRequest = int(self.requests_num.text())
        # 初始化恶意攻击流量
        self.attackRequests = Attack(totalAttackRequests=self.totalAttackRequest, serverNum=self.serverNum, servers=self.S)
        # 设定服务器的攻击流量
        self.S = attackServer(self.attackRequests, self.S)
        # 经过  分配策略的请求数量
        # defendRequests, ic, ik = Defend(self.commonRequest, attackRequests, self.capacity, wc=0.01, num=self.serverNum)
        self.ic, self.ik = Defend(serverNum=self.serverNum, servers=self.S)
        self.serverDisplay.refreshServerDisplay(totalAttackRequest=self.totalAttackRequest, S=self.S)
        self.stackBarChart.refreshChart(self.S, self.ik)
        self.PieChart.refreshChart(self.S)
        self.BarChart.refreshChart(self.ic, self.ik)

def initCommonRequest(serverNum):
    commomRequest = [0]
    for i in range(serverNum):
        commomRequest.append(50 + i*250)
    print("commonRequest:", commomRequest)
    return commomRequest


def initCapacity(serverNum):
    capacity = [0, 50]
    for i in range(serverNum-1):
        if i % 2 == 0:
            capacity.append(capacity[-1])
        else:
            capacity.append(capacity[-1]*2)
    print("capacity:", capacity)
    # capacity = [0, 50, 50, 100, 100, 200]
    return capacity


def generateServerPositions(num_servers, y_base=240, y_variation=180):
    positions = []
    # 云服务器的位置
    positions.append((95, 125))
    x = 80
    for i in range(num_servers):
        x_step = random.randint(int(600 / num_servers), 200)
        x = x + x_step
        if x > 510:
            x = 80
            y_base += 200
        if y_base > 500:
            y_base = 240
        y = y_base + random.randint(-y_variation // 2, y_variation // 2)
        positions.append((x, y))

    print("positions:", positions)
    return positions


def initServer(pos, commonRequest, capacity):
    S = []
    for i in range(len(commonRequest)):
        S.append(Server(commonRequest=commonRequest[i], pos=pos[i], capacity=capacity[i]))
    # S.append(Server(request[len(request)-1], (650, 100)))
    return S


def attackServer(attackRequests, S):
    for i in range(len(S)):
        S[i].updateAttackRequest(attackRequests[i])
    return S




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
