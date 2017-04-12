"""一个Tab，网易云的全部歌单。"""
from PyQt5.QtWidgets import QFrame, QGridLayout
from wymusic.childmod.OneSing import OneSing
from wymusic.widgets import addition
from wymusic.widgets.base import RequestThread, Timer
from wymusic.apis import netEaseApi
from wymusic.networks import network

# netEaseApi
netEase = netEaseApi.NetEaseWebApi()
class NetEaseSingsArea(QFrame):
    """全部歌单。"""

    def __init__(self, parent=None):
        super(NetEaseSingsArea, self).__init__(parent)
        self.parent = parent
        self.transTime = addition.itv2time

        self.setObjectName("allSingsArea")
        # self.frame.setObjectName("allSings")
        # 为什么有的需要加utf-8呢，因为有中文。
        with open('QSS/neteaseSings.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        self.picManager = network.NetWorkThread(self)
        self.userPicManager = network.NetWorkThread(self)
        # 连接滑轮到底的信号槽。
        # 同时连接图片下载的线程全部完成的信号槽。
        # 若一轮图片下载完成并且滑到底部则进行下一次线程，否则将不会。
        self.parent.scrollDown.connect(self.sliderDownEvent)
        self.picManager.allFinished.connect(self.picManagerFinishedEvent)
        # 用于存储结果。
        self.result = []
        # 歌单的索引。
        self.singsFrames = []
        # 歌单显示名的url。
        self.singPicUrls = []
        # 歌单名称。
        self.singNames = []
        # 歌单id。
        self.singIds = []

        # 一个是否滑到底部的flag。
        self.sliderDown = False

        # 布局用row。
        self.gridRow = 0
        # 布局用column。
        self.gridColumn = 0

        # 主布局。
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setHorizontalSpacing(10)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        # 用于网易云的每次请求的歌单数量。
        self.offset = 0
        # 用于记录次数，多线程的同步。

        self.api = netEase

        # 一个线程，初始化用于请求歌单的全部内容。
        self.netThread = RequestThread(self, self.getSings)
        self.netThread.finished.connect(self.setSings)
        self.netThread.setFlag(True)
        self.netThread.start()
        # 另一个线程，无限循环的时钟，用于检测当picManager处于工作状态时，暂停下一轮请求。
        self.timerThread = Timer(self, self.picManager.picFinished)
        self.timerThread.finished.connect(self.setSings2)
        # 第三个线程，与第一个一样。
        self.singsThread = RequestThread(self)

    def getSings(self):
        """请求一波歌单，一次30个。设置offset会设置请求量。"""
        for i in self.api.all_playlist(offset=self.offset):
            self.result.append(i)
            self.singNames.append(i['name'])
            self.singPicUrls.append(i['coverImgUrl'])
            self.singIds.append(i['id'])

    def setSings(self):
        # 先生成QFrame，并附上名字，图片稍后再获取。
        for i in range(30):
            i += self.offset
            picName = self.singPicUrls[i][self.singPicUrls[i].rfind('/')+1:]
            frame = OneSing(self.gridRow, self.gridColumn, self.singIds[i], self, picName)
            frame.nameLabel.setText(self.singNames[i])

            # 建立起索引，一是防止垃圾回收了，二是可以找到他的地址。
            self.singsFrames.append(frame)

            # 用于布局，一行4个。
            if self.gridColumn == 3:
                self.gridColumn = 0
                self.gridRow += 1
            else:
                self.gridColumn += 1

        # 设置url。
        self.picManager.setUrl(self.singPicUrls)

        # 如果没有在工作那就直接进行就好了。
        if self.picManager.picFinished:
            # 没有在工作，加载图片。
            self.pics = self.picManager.startGet(self.singsFrames)
            # 开启监控的线程，如果是初始化时，没有加载完成就拉到最低时，也可以监控到。
            self.timerThread.start()
        else:
            # 在进行工作，并且监控线程也在工作就不做操作，否则两次start会报错也没有必要。
            if self.timerThread.isFinished() == False:
                pass
            # 下两步可合为一步，懒得改了。
            elif self.timerThread.times == 0:
                self.timerThread.timer = 1
                self.timerThread.start()
            else:
                self.timerThread.start()

    def setSings2(self):
        # 上面那个的副本，只用于发起请求图片的函数。
        # 监控线程的完成槽。
        # 先判断图片线程是否在工作，如果没有在工作，那么就判断请求新歌单的线程有没有在工作，
        # 如果新歌单的线程在工作，那么就重新开启监控线程，因为还不到要进行图片请求的时候。
        # 否则将进行新的图片请求。
        if self.picManager.picFinished:
            if self.netThread.isRunning():
                self.timerThread.start()
            else:
                self.picManager.setUrl(self.singPicUrls)
                self.picManager.startGet(self.singsFrames)

    def sliderDownEvent(self):
        """滑轮到底的事件。"""
        if self.isHidden() == False:
            self.offset += 30
            # 判断是否在工作，免得多次start。
            if self.netThread.isRunning():
                return
            else:
                self.netThread.start()

    def picManagerFinishedEvent(self):
        # 图片线程已经完成，进行标记。
        self.picManager.picFinished = True
        # 让监控线程停止。
        self.timerThread.setVar(True)

