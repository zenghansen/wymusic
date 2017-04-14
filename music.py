"""
重新设计，主要用于熟悉设计模式。
多线程/漂亮界面的设计等。

以网易云音乐为模板。
# 基本没考虑网络的出错问题。
# 不过也考虑了一些。
# 对于放在线程QThread里的错误捕获如果要显示警示框: QDialog exec_
# 需要使用信号槽，捕获后发出信号，然后在主线程中创建并显示，否则会导致程序错误。
# 
"""
from wymusic.childmod.DetailSings import DetailSings
from wymusic.mod.Header import Header
from wymusic.mod.MainContent import MainContent
from wymusic.mod.Navigation import Navigation

__author__ = 'cyrbuzz'

import sys
import random

#sys.path.append('widgets')
#sys.path.append('networks')
#sys.path.append('apis')

from wymusic.widgets.base  import *
from wymusic.widgets.player import *
from wymusic.widgets.native import NativeMusic


"""用于承载整个界面。所有窗口的父窗口，所有窗口都可以在父窗口里找到索引。"""
class Window(QWidget):
    """Window 承载整个界面。"""
    def __init__(self):
        super(Window, self).__init__()
        self.setObjectName('MainWindow') #样式用到该名字
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('resource/format.ico'))
        self.setWindowTitle("Music")
        with open('QSS/window.qss', 'r') as f:  #加载样式的方式
            self.setStyleSheet(f.read())
        self.resize(1022, 670)

        self.header = Header(self) #头部
        self.navigation = Navigation(self) #左边导航
        self.playWidgets = PlayWidgets(self) #底部播放组件
        self.mainContent = MainContent(self) #主要内容区
        self.nativeMusic = NativeMusic(self) #本地音乐
        # self.player = Player(self)

        self.mainContents = QTabWidget()
        self.mainContents.tabBar().setObjectName("mainTab")
        self.mainContents.currentChanged.connect(self.addTabHistory)
        # 用于存储Tab的历史，方便前后切换。
        # 只存储5个，不考虑效率问题。
        self.history = []
        self.currentIndex = -1
        # 前后切换时也会触发currentChanged信号，
        # 前后切换时不允许增加新的历史也不允许删除旧的历史。
        self.isTab = False

        # 加载tab设置。
        self.setContents()
        # 设置布局小细线。
        self.setLines()
        # 设置布局。
        self.setLayouts()

    def setContents(self):
        """设置tab界面。"""
        # 将需要切换的窗口做成Tab，并隐藏tabBar，这样方便切换，并且可以做前进后退功能。
        # 他的父窗口为什么是mainContent是历史问题。暂不需要修改。
        self.detailSings = DetailSings(self.mainContent)
        self.mainContents.addTab(self.mainContent, '')
        self.mainContents.addTab(self.detailSings, '')
        self.mainContents.addTab(self.nativeMusic, '')
        self.navigation.nativeListFunction = lambda: self.mainContents.setCurrentIndex(2)

        self.mainContents.setCurrentIndex(0)

    def addTab(self, widget, name=''):
        self.mainContents.addTab(widget, name)

    def allTab(self):
        return self.mainContents.count()

    def setTabIndex(self, index):
        self.mainContents.setCurrentIndex(index)

    def addTabHistory(self, index):
        length = len(self.history)
        if not self.isTab:
            if length < 5:
                self.history.append(index)
            else:
                self.history.pop(0)
                self.history.append(index)
            # 不是前后切换时将当前的索引定为末尾一个。
            self.currentIndex = length
        else:
            self.isTab = False


    def prevTab(self):
        # 前一个的切换。
        if self.currentIndex == 0 or self.currentIndex == -1:
            return
        else:
            self.isTab = True
            self.currentIndex -= 1
            self.mainContents.setCurrentIndex(self.history[self.currentIndex])

    def nextTab(self):
        # 后一个的切换。

        if self.currentIndex == len(self.history)-1 or self.currentIndex == -1:
            return
        else:
            self.isTab = True
            self.currentIndex += 1
            self.mainContents.setCurrentIndex(self.history[self.currentIndex])

    def setLines(self):
        """设置布局小细线。"""
        self.line1 = QFrame()
        self.line1.setObjectName("line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Plain)
        self.line1.setLineWidth(2)

    def setLayouts(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.header)
        self.mainLayout.addWidget(self.line1)

        self.contentLayout = QHBoxLayout()

        self.contentLayout.addWidget(self.navigation)
        self.contentLayout.addWidget(self.mainContents)

        self.contentLayout.setSpacing(0)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)   


        self.mainLayout.addLayout(self.contentLayout)
        self.mainLayout.addWidget(self.playWidgets)

        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)




if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()

    main.show()
    # 当前音乐的显示信息。
    # 因为需要布局之后重新绘制的宽高。
    # 这个宽高会在show之后才会改变。
    # 需要获取宽，高并嵌入到父窗口里。
    main.playWidgets.currentMusic.resize(main.navigation.width(), 64)
    main.playWidgets.currentMusic.move(0, main.height()-64-main.playWidgets.height())

    sys.exit(app.exec_())
