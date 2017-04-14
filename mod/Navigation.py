
"""左侧的导航栏，包括发现音乐/歌单/本地音乐。"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QLabel, QListWidget, QListWidgetItem, QVBoxLayout
from PyQt5.QtWidgets import QScrollArea


class Navigation(QScrollArea):
    def __init__(self, parent=None):
        """包括发现音乐，MV，我的音乐, 歌单等导航信息。"""
        super(Navigation, self).__init__(parent)
        self.parent = parent
        self.frame = QFrame()
        self.setMaximumHeight(576)
        self.setMaximumWidth(200)

        self.setWidget(self.frame)
        self.setWidgetResizable(True)
        self.frame.setMaximumWidth(200)
        self.frame.setMinimumWidth(200)

        # 定义2个事件函数，方便扩展。
        self.nativeListFunction = self.none
        self.singsFunction = self.none

        with open('QSS/navigation.qss', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)
            self.frame.setStyleSheet(style)

        # 包括显示信息： 推荐 我的音乐 歌单。
        self.setLabels()
        # 包括详细的内容：发现音乐，FM，MV等。
        self.setListViews()

        self.setLayouts()

    def setLabels(self):
        """定义所有的标签。"""
        self.showLabel = QLabel(" 推荐", self)
        self.showLabel.setObjectName("showLabel")

        self.myMusic = QLabel(" 我的音乐", self)
        self.myMusic.setObjectName("myMusic")

        self.singsListLabel = QLabel(" 收藏与创建的歌单", self)
        self.singsListLabel.setObjectName("singsListLabel")


    def setListViews(self):
        """定义承载功能的ListView"""
        self.navigationList = QListWidget()
        self.navigationList.setMinimumHeight(110)
        self.navigationList.setMaximumHeight(110)
        self.navigationList.setObjectName("navigationList")
        self.navigationList.addItem(QListWidgetItem(QIcon('resource/Music.png'), " 发现音乐"))
        self.navigationList.addItem(QListWidgetItem(QIcon('resource/signal.png'), " 私人FM"))
        self.navigationList.addItem(QListWidgetItem(QIcon('resource/movie.png'), " MV"))
        self.navigationList.itemPressed.connect(self.navigationListItemClickEvent)
        self.navigationList.setCurrentRow(0)

        self.nativeList = QListWidget()
        self.nativeList.setObjectName("nativeList")
        self.nativeList.setMinimumHeight(50)
        self.nativeList.setMaximumHeight(50)
        self.nativeList.addItem(QListWidgetItem(QIcon('resource/notes.png')," 本地音乐"))
        self.nativeList.itemPressed.connect(self.nativeListItemClickEvent)

    def setSingsList(self):
        """歌单用按钮显示，不显示在ListWidget里是因为ListWidget只是单个有滚轮，需要全部有滚轮。"""
        self.singsList = []
        # for i in range(25):
        #     self.singsList.append(QPushButton(QIcon('resource/notes.png'),'TestSingsListaaaaaaaaaaaaaaaaaaaaaaaaa'))

        # for i in self.singsList:
        #     i.setCheckable(True)
        #     i.setAutoExclusive(True)
        #     i.clicked.connect(self.singsButtonClickEvent)
        #     self.frame.mainLayout.addWidget(i)
        pass

    def navigationListItemClickEvent(self):
        """用户处理导航栏的点击事件。"""
        # 处理其他组件取消选中。
        for i in self.singsList:
            if i.isChecked():
                i.setCheckable(False)
                i.setCheckable(True)
                break

        self.nativeList.setCurrentRow(-1)

        """处理事件。"""
        self.navigationListFunction()

    def nativeListItemClickEvent(self):
        """本地功能的点击事件。"""
        for i in self.singsList:
            if i.isChecked():
                i.setCheckable(False)
                i.setCheckable(True)
                break

        self.navigationList.setCurrentRow(-1)

        """处理事件。"""
        self.nativeListFunction()

    def singsButtonClickEvent(self):
        """歌单的点击事件。"""
        self.navigationList.setCurrentRow(-1)
        self.nativeList.setCurrentRow(-1)

        """处理事件。"""
        self.singsFunction()

    def setLayouts(self):
        """定义布局。"""
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.showLabel)
        self.mainLayout.addSpacing(3)
        self.mainLayout.addWidget(self.navigationList)
        self.mainLayout.addSpacing(1)

        self.mainLayout.addWidget(self.myMusic)
        self.mainLayout.addSpacing(1)
        self.mainLayout.addWidget(self.nativeList)
        self.mainLayout.addSpacing(1)

        self.mainLayout.addWidget(self.singsListLabel)
        self.mainLayout.addSpacing(1)

        self.setSingsList()
        self.mainLayout.addStretch(1)

        self.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.frame.setLayout(self.mainLayout)


    def navigationListFunction(self):
        #isVisible = self.tab.isVisible()
        if self.navigationList.currentRow() == 0:
            # 发现音乐。
            self.parent.mainContents.setCurrentIndex(0)
    def none(self):
        # 没有用的空函数。
        pass
