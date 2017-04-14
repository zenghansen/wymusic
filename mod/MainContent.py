"""主要内容区，包括最新的歌单。"""
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout
from wymusic.childmod.NetEaseSingsArea import NetEaseSingsArea
from wymusic.widgets.base import ScrollArea


class MainContent(ScrollArea):
    # 定义一个滑到了最低部的信号。
    # 方便子控件得知已经滑到了最底部，要做些加载的动作。

    def __init__(self, parent=None):
        """主内容区，包括推荐歌单等。"""
        super(MainContent, self).__init__()
        self.parent = parent
        self.setObjectName("MainContent")

        # self.detailSings = DetailSings(self)
        # 连接导航栏的按钮。
        with open("QSS/mainContent.qss", 'r', encoding='utf-8') as f:
            self.style = f.read()
            self.setStyleSheet(self.style)


        self.tab = QTabWidget()
        self.tab.setObjectName("contentsTab")
        self.indexNetEaseSings = NetEaseSingsArea(self)
        self.tab.addTab(self.indexNetEaseSings, "网易云歌单")

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.tab)
        # self.mainLayout.addWidget(self.detailSings)

        self.frame.setLayout(self.mainLayout)

    def addTab(self, widget, name=''):
        self.tab.addTab(widget, name)
