
"""标题栏，包括logo，搜索，登陆，最小化/关闭。"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QPushButton, QLabel, QHBoxLayout
from wymusic.widgets import addition

class Header(QFrame):#QFrame模块和Qwidget的区别，QFrame支持样式的实例

    def __init__(self, parent=None):
        """头部区域，包括图标/搜索/设置/登陆/最大/小化/关闭。"""

        super(Header, self).__init__()
        self.setObjectName('Header')

        self.parent = parent
        with open('QSS/header.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        # 加载按钮设置。
        self.setButtons()
        # 加载标签设置。
        self.setLabels()
        # 加载输入框设置。
        self.setLineEdits()
        # 加载小细线装饰。
        self.setLines()
        # 加载布局设置。
        self.setLayouts()

    def setButtons(self):
        """创建所有的按钮。"""

        self.closeButton = QPushButton('×', self)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setMinimumSize(21, 17)
        self.closeButton.clicked.connect(self.parent.close)

        self.showminButton = QPushButton('_', self)
        self.showminButton.setObjectName("minButton")
        self.showminButton.setMinimumSize(21, 17)
        self.showminButton.clicked.connect(self.parent.showMinimized)

        self.loginButton = QPushButton("未登录 ▼", self)
        self.loginButton.setObjectName("loginButton")

        self.prevButton = QPushButton("<")
        self.prevButton.setObjectName("prevButton")
        self.prevButton.setMaximumSize(28, 22)
        self.prevButton.setMinimumSize(28, 22)
        self.prevButton.clicked.connect(self.parent.prevTab)

        self.nextButton = QPushButton(">")
        self.nextButton.setObjectName("nextButton")
        self.nextButton.setMaximumSize(28, 22)
        self.nextButton.setMinimumSize(28, 22)
        self.nextButton.clicked.connect(self.parent.nextTab)

    def setLabels(self):
        """创建所需的所有标签。"""
        self.logoLabel = QLabel(self)
        self.logoPixmap = QPixmap(r'resource//format.png')
        self.logoLabel.setPixmap(self.logoPixmap.scaled(22, 22))
        self.logoLabel.setMaximumSize(22, 22)

        self.descriptionLabel = QLabel(self)
        self.descriptionLabel.setText("<b>Music<b>")

        self.userPix = QLabel(self)
        self.nouserPix = QPixmap(r'resource//nouser.png')
        self.userPix.setPixmap(self.nouserPix.scaled(22, 22))
        self.userPix.setMaximumSize(22, 22)

    def setLineEdits(self):
        """创建搜素框。"""
        self.searchLine = addition.SearchLineEdit(self)
        self.searchLine.setPlaceholderText("搜索音乐, 歌手, 歌词, 用户")

    def setLines(self):
        """设置装饰用小细线。"""
        self.line1 = QFrame(self)
        self.line1.setObjectName("line1")
        self.line1.setFrameShape(QFrame.VLine)
        self.line1.setFrameShadow(QFrame.Plain)
        self.line1.setMaximumSize(1, 25)

    def setLayouts(self):
        """设置布局。"""
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.logoLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addSpacing(70)
        self.mainLayout.addWidget(self.prevButton)
        self.mainLayout.addWidget(self.nextButton)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.searchLine)
        # self.mainLayout.addWidget(self.searchButton)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.userPix)
        self.mainLayout.addSpacing(7)
        self.mainLayout.addWidget(self.loginButton)
        self.mainLayout.addSpacing(7)
        self.mainLayout.addWidget(self.line1)
        self.mainLayout.addSpacing(30)
        self.mainLayout.addWidget(self.showminButton)
        self.mainLayout.addSpacing(3)
        self.mainLayout.addWidget(self.closeButton)


        self.setLayout(self.mainLayout)

    """重写鼠标事件，实现窗口拖动。"""
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.m_drag = True
            self.parent.m_DragPosition = event.globalPos()-self.parent.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and Qt.LeftButton:
                self.parent.move(event.globalPos()-self.parent.m_DragPosition)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.m_drag = False
