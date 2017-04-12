"""歌单详情页。"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QTabWidget, QAbstractItemView, QVBoxLayout, QHBoxLayout, QTableWidget
from wymusic.widgets.base import ScrollArea


class DetailSings(ScrollArea):

    def __init__(self, parent=None):
        super(DetailSings, self).__init__(self)

        # self.hide()
        self.parent = parent
        self.setObjectName('detailSings')
        with open('QSS/detailSings.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        self.musicList = []

        # 建立索引。
        self.grandparent = self.parent.parent
        self.player = self.grandparent.playWidgets.player
        self.playList = self.grandparent.playWidgets
        self.currentMusic = self.grandparent.playWidgets.currentMusic

        self.setLabels()
        self.setButtons()
        self.setTabs()
        self.setLayouts()

    def setLabels(self):
        self.picLabel = QLabel(self.frame)
        self.picLabel.setObjectName('picLabel')
        self.picLabel.setMinimumSize(200, 200)
        self.picLabel.setMaximumSize(200, 200)

        self.titleLabel = QLabel(self.frame)
        self.titleLabel.setObjectName('titleLabel')
        self.titleLabel.setWordWrap(True)

        self.authorPic = QLabel(self.frame)
        self.authorName = QLabel(self.frame)
        self.authorName.setObjectName('authorName')
        self.authorName.setMaximumHeight(28)

        self.descriptionLabel = QLabel(self.frame)
        self.descriptionLabel.setObjectName('descriptionLabel')
        self.descriptionLabel.setMaximumWidth(450)
        self.descriptionLabel.setMaximumHeight(100)
        self.descriptionLabel.setWordWrap(True)

    def setButtons(self):
        self.showButton = QPushButton("歌单")
        self.showButton.setObjectName('showButton')
        self.showButton.setMaximumSize(36, 20)

        self.descriptionButton = QPushButton(" 简介 ：")
        self.descriptionButton.setObjectName('descriptionButton')
        self.descriptionButton.setMaximumSize(36, 36)

        self.playAllButton = QPushButton("全部播放")
        self.playAllButton.setIcon(QIcon('resource/playAll.png'))
        self.playAllButton.setObjectName('playAllButton')
        self.playAllButton.setMaximumSize(90, 24)

    def setTabs(self):
        self.contentsTab = QTabWidget(self.frame)

        self.singsTable = QTableWidget()
        self.singsTable.setObjectName('singsTable')
        self.singsTable.setMinimumWidth(self.width())
        self.singsTable.setColumnCount(3)
        self.singsTable.setHorizontalHeaderLabels(['音乐标题', '歌手', '时长'])

        self.singsTable.setColumnWidth(0, self.width()/3*1.25)
        self.singsTable.setColumnWidth(1, self.width()/3*1.25)
        self.singsTable.setColumnWidth(2, self.width()/3*0.5)
        # self.singsTable.horizontalHeader().setVisible(False)
        self.singsTable.horizontalHeader().setStretchLastSection(True)
        self.singsTable.verticalHeader().setVisible(False)
        self.singsTable.setShowGrid(False)
        self.singsTable.setAlternatingRowColors(True)

        self.singsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.singsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.singsTable.itemDoubleClicked.connect(self.itemDoubleClickedEvent)

        self.contentsTab.addTab(self.singsTable, "歌曲列表")

    def itemDoubleClickedEvent(self):
        currentRow = self.singsTable.currentRow()
        data = self.musicList[currentRow]

        self.playList.setPlayerAndPlayList(data)


    def setLayouts(self):
        self.mainLayout = QVBoxLayout()

        self.topLayout = QHBoxLayout()

        self.descriptionLayout = QVBoxLayout()
        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.showButton)
        self.titleLayout.addSpacing(5)
        self.titleLayout.addWidget(self.titleLabel)

        self.authorLayout = QHBoxLayout()
        self.authorLayout.addWidget(self.authorPic)
        self.authorLayout.addWidget(self.authorName)
        self.authorLayout.addStretch(1)

        self.descriptLayout = QHBoxLayout()
        self.descriptLayout.addWidget(self.descriptionButton)
        self.descriptLayout.addWidget(self.descriptionLabel)

        self.descriptionLayout.addLayout(self.titleLayout)
        self.descriptionLayout.addLayout(self.authorLayout)
        self.descriptionLayout.addSpacing(5)
        self.descriptionLayout.addWidget(self.playAllButton)
        self.descriptionLayout.addSpacing(10)
        self.descriptionLayout.addLayout(self.descriptLayout)

        self.descriptionLayout.setSpacing(0)

        self.topLayout.addWidget(self.picLabel)
        self.topLayout.addSpacing(18)
        self.topLayout.addLayout(self.descriptionLayout)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.contentsTab)

        self.frame.setLayout(self.mainLayout)

    def test(self):
        self.titleLabel.setText("［日系］电音&人声，电毒侵入脑电波！")
        self.picLabel.setStyleSheet('''QLabel {border-image: url(cache/566527372.jpg); padding: 10px;}''')
        self.authorName.setText("Nothing")
        self.descriptionLabel.setText("test"*30)

        self.singsTable.setRowCount(4)