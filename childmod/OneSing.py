"""一个用于承载歌单简单信息的QFrame。"""
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QTableWidgetItem


class OneSing(QFrame):
    # 大量创建，这样可以省内存。
    __solts__ = ('parent', 'ggparent', 'detailFrame', 'transTime', 'row', 'column', 'ids',
                 'picName', 'picLabel', 'nameLabel',
                 'mainLayout',
                 'mousePos',
                 'result')

    def __init__(self, row, column, ids=None, parent=None, picName=None):
        super(OneSing, self).__init__()
        if parent:
            self.parent = parent
            self.ggparent = self.parent.parent.parent
            self.detailFrame = self.ggparent.detailSings
            self.transTime = self.parent.transTime
        else:
            self.parent = None
            self.ggparent = None
            self.detailFrame = None
            self.transTime = None

        self.setObjectName('oneSing')
        # 自己的位置信息。
        self.row = row
        self.column = column
        # 歌单号。
        self.ids = ids
        # 大图的缓存名。
        self.picName = picName

        self.setMinimumSize(180, 235)

        self.picLabel = QLabel(self)
        self.picLabel.setObjectName('picLabel')
        self.picLabel.setMinimumSize(180, 180)
        self.picLabel.setMaximumSize(180, 180)

        self.nameLabel = QLabel(self)
        self.nameLabel.setMaximumWidth(180)
        self.nameLabel.setWordWrap(True)

        self.mainLayout = QVBoxLayout()

        self.mainLayout.addWidget(self.picLabel)
        self.mainLayout.addWidget(self.nameLabel)

        self.setLayout(self.mainLayout)

        self.parent.mainLayout.addWidget(self, self.row, self.column)

    def setStyleSheets(self, styleSheet=None):
        if styleSheet:
            self.setStyleSheet(styleSheet)

    def mousePressEvent(self, event):
        # 记录下当前鼠标的位置。
        self.mousePos = QCursor.pos()

    def mouseReleaseEvent(self, event):
        # 先进行判断，防止误点将鼠标移开后还是会判断为已经点击的尴尬。
        if QCursor.pos() != self.mousePos:
            return
        else:
            self.parent.singsThread.setTarget(self.requestsDetail)
            self.parent.singsThread.finished.connect(self.setDetail)
            self.parent.singsThread.start()

    def requestsDetail(self):
        """请求本歌单的详情，并复制给detailSings."""
        result = self.parent.api.details_playlist(self.ids)
        self.result = result

    def setDetail(self):
        # 方便书写。
        result = self.result
        self.detailFrame.musicList = []
        self.detailFrame.singsTable.clearContents()
        # 一些信息，包括展示大图，标题，创建者，简介。
        self.detailFrame.picLabel.setStyleSheet('''QLabel {border-image: url(cache/%s); padding: 10px;}'''%(self.picName))
        self.detailFrame.titleLabel.setText(result['name'])
        self.detailFrame.authorName.setText(result['creator']['nickname'])
        # 简介有些太长了，暂时只截取前107个字符。
        description = result['description']
        # 有些没有简介会报错的。
        if not description:
            description = ''
        self.detailFrame.descriptionLabel.setText(description[:107])
        # 这边添加歌曲的信息到table。
        self.detailFrame.singsTable.setRowCount(result['trackCount'])
        for i, j in zip(result['tracks'], range(result['trackCount'])):
            names = i['name']
            musicName = QTableWidgetItem(names)
            self.detailFrame.singsTable.setItem(j, 0, musicName)

            author = i['artists'][0]['name']
            musicAuthor = QTableWidgetItem(author)
            self.detailFrame.singsTable.setItem(j, 1, musicAuthor)

            times = self.transTime(i['duration']/1000)
            musicTime = QTableWidgetItem(times)
            self.detailFrame.singsTable.setItem(j, 2, musicTime)

            music_img = i['album']['blurPicUrl']

            self.detailFrame.musicList.append({'url': i['mp3Url'], 'name': names, 'time':times, 'author':author, 'music_img': music_img})

        self.parent.singsThread.finished.disconnect()

        # 隐藏原来的区域，显示现在的区域。
        self.ggparent.mainContents.setCurrentIndex(1)

