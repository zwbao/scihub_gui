# 用 PyQt5 写一个 scihub 下载器

PyQt 是一个创建 GUI 应用程序的工具包，是 Python 和 Qt 的结合体，可以用 Python 编写跨平台（包括 UNIX，Windows 和 Mac）的 GUI 应用程序。结合自带的 Qt Designer 可视化工具进行界面设计，我们可以非常快速地开发出一款功能强大、界面美观的 GUI 应用程序。

在这个例子中我们将从零开始用用 PyQt5 写一个界面化的 scihub 下载器，先来预览一下成品（监听黏贴板 --> 识别 DOI --> 下载文章 --> 根据文章题目重命名 --> 弹出消息框）：

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1w7l1om1g30tx0c71kx.gif)

完成的步骤包含以下四部分，在本文中我们将介绍前两个部分，即设计 UI：

1. 用 Qt Designer 设计界面，生成 `.ui` 格式的界面
2. 用 `pyuic5` 将 `.ui` 转为 `.py`
3. 构建主程序
4. 打包 `.py` 为可执行文件

## 1. 环境准备

安装 PyQt5

```
pip3 install PyQt5
```

安装 PyQt5-tools

```
pip3 install pyqt5-tools
```

安装 pyuic5-tool

```
pip3 install pyuic5-tool
```

## 2. 设计 UI

打开 Qt Designer （在 Anaconda 的 `bin` 目录下），Qt Designer 是一个非常强大的 GUI 设计工具，有了它我们就可以在程序设计中更快地开发设计出程序界面，避免了用纯代码来写一个窗口的繁琐，同时 PyQt 也支持界面与逻辑分离。Qt Designer 生成的文件格式为：`.ui`。

打开 Qt Designer 可见到如下界面，主要分为四个区域：**项目区**、**控件区**、**编辑区**、**属性区**。

Qt Designer 使用起来非常简单，**编辑区**显示了软件的主要界面，我们只需将所需的控件从**控件区**拖入编辑区即可添加控件，接着我们可以在**属性区**调整这些控件的属性，**项目区**则用于显示控件之间的层级关系。

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1weqz3rlj30zk0judh1.jpg)

首先，我们需要新建窗口，点击右上角的新建图标：

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1wfqy3c7j308r05v3yg.jpg)

选择 QVGA 纵向：

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1wg2tvsjj30gx0gz0sv.jpg)

现在编辑区即创建了一个空白的窗口：

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1ybzypwxj30zk0juwfm.jpg)

在本文的例子中我们需要添加三个控件：

![](https://tva1.sinaimg.cn/large/0081Kckwly1gk1yek8avjj306z09qweb.jpg)

- `QLabel`：标签，该标签可以放纯文本，链接或者富文本信息。

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1xmypeanj307302l0sk.jpg)

- `QTextEdit`：多行文本框，可以显示多行文本内容，当文本内容超出控件显示范围时，可显示滚动条，`Qtextedit` 不仅可以用来显示文本还可以用来显示 HTML 文档。

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1xnc95qkj307205f0sm.jpg)

- `QPushButton`：命令按钮，按下（或者单击）按钮以命令脚本执行某个操作。

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1xmjdefrj306y02da9v.jpg)

将这三个控件分别从**控件区**分别拖入**编辑区**后，在**项目区**右键 MainWindow，选择布局，选择垂直布局，这样即使我们调整窗口的大小，这三个控件的相对位置保持不变。

![](https://tva1.sinaimg.cn/large/0081Kckwly1gk2kkwuec8j30fa0gx75j.jpg)

添加了所有控件之后，下一步便是分别设置控件的属性，进一步调整控件。在这个例子中，我们的任务是更改 `QLabel` 和 `QPushButton` 的默认文本并加粗字体，同时还需将 `QLabel` 居中。

双击 TextLabel 编辑 `QLabel` 的文本为 `请输入 DOI`，接着在属性框，font 选择粗体。

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1xtzgbibj30i3086jrf.jpg)

alignment 水平选择居中：

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1xv7akbnj30ig0a4jrp.jpg)

同样，双击 PushButton 编辑按钮文本为 `Download`：

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1xw7qvw3j30ht06v749.jpg)

至此我们已完成了所有界面设计：

![](https://tva1.sinaimg.cn/large/0081Kckwly1gk1yek8avjj306z09qweb.jpg)

点击右上角的保存图标另存为：

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1y1kdawtj30ci061q2t.jpg)

使用 UI Designer 设计好窗体并保存为文件 `scihub_ui.ui` 后，要在 Python  里使用这个窗体，需要将 `.ui` 转换为 python 格式，这里将借助 `pyuic5` 工具，在命令行中输入：

```
pyuic5 -o scihub_ui.py scihub_ui.ui
```

转换成功后，打开 `scihub_ui.py` 文件，我们可以简单看一下这个脚本里的内容，代码里首先 `import` 了 PyQt5 相关库，并定义了名为 `Ui_MainWindow` 的 `class`，这个 `class` 主要包含两个函数 `setupUi()` 和 `retranslateUi()`。`setupUi()` 用于窗体的初始化，初始化了各个控件成员 `self.xx`，这与我们在 `Qt Designer` 里添加的控件是一一对应的。`retranslateUi()` 设置了窗体的标题、标签的文字、按钮的标题。

```
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scihub_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(240, 320)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 211, 251))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 240, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "请输入 DOI"))
        self.pushButton.setText(_translate("MainWindow", "Download"))

```

在下一部分中我们将介绍如何使用这种界面与逻辑分离的 GUI 程序框架，并构建主函数。

## 3. 构建主程序

### 3.1 界面与逻辑分离的 GUI 程序框架

这里我们采用单继承的界面封装方法，编写主程序 `scihub_gui.py` 框架，代码如下：

```
## 单继承方法，能更好地进行界面与逻辑的分离
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qt import QStandardPaths
from scihub_ui import Ui_MainWindow

class CustomUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent) # 调用父类构造函数，self 就是一个 QMainWindow 对象
        self.ui = Ui_MainWindow() # 创建UI 对象
        self.ui.setupUi(self) # 构造UI

if __name__ == '__main__':
    app = QApplication(sys.argv) # 创建app，用 QApplication 类
    cutomUI = CustomUI()
    cutomUI.show()
    sys.exit(app.exec_())
```

### 3.2 实现文献下载功能

本来自己写了个简单的脚本，但前两天在 GitHub 上看到了功能更完善的脚本，所以这里不妨做个调包侠。脚本地址：https://github.com/zaytoun/scihub.py

这个脚本可实现根据 `DOI | PMID | URL` 下载文献 PDF，使用方法也非常简单：

```
from scihub import SciHub

sh = SciHub()
result = sh.download('http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=1648853', path='paper.pdf')
```

我们将该 `Scihub.py` 脚本下载下来，放在 `scihub_gui.py` 的同一目录下，方便调用。

下载文献后，可用 `PyPDF2` 包提取 PDF 信息，以根据文献标题重命名 PDF 文件：

```
from PyPDF2 import PdfFileReader

with open('paper.pdf', 'rb') as f:
    pdf = PdfFileReader(f)
    info = pdf.getDocumentInfo()
    title = info.title
```

### 3.3 PyQt5 的事件处理机制

PyQt5 有一个独一无二的信号和槽机制来处理事件。信号和槽用于对象之间的通信。当指定事件发生，一个事件信号会被发射。槽可以被任何 Python 脚本调用。当和槽连接的信号被发射时，槽会被调用。

在 Qt 中，每一个 QObject 对象和 PyQt 中所有继承自 QWidget 的控件（这些都是 QObject 的子对象）都支持信号与槽机制。当信号发射时，连接的槽函数将会自动执行。在 PyQt 5 中信号与槽通过 `控件名.信号.connect(槽函数)` 方法连接。

在我们这个小程序中共包含了两类信号：

1. 识别黏贴板的变化
2. 识别按钮动作

所以下一步我们为 `scihub_gui.py` 脚本加上亿点点细节，用 `QApplication.clipboard()` 读取黏贴板信息并重定向输出流（展示在文本区域内），绑定按钮事件（获取参数&触发请求），最后用 `QMessageBox` 弹出信息框。最终 `scihub_gui.py` 的代码如下：

```
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.Qt import QStandardPaths
from scihub_ui import Ui_MainWindow
from scihub import SciHub
from PyPDF2 import PdfFileReader
import os

class CustomUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cb = QApplication.clipboard()
        self.cb.dataChanged.connect(self.monitor_clipboard)
        self.ui.textEdit.setText(self.cb.text())
        self.ui.pushButton.clicked.connect(self.buttClicked)

    def monitor_clipboard(self):
        if self.cb.text():
            self.ui.textEdit.setText(self.cb.text())

    def buttClicked(self):
        try:
            curPath = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation) # 默认保存在 ~/Documents
            pdf_name = "/paper.pdf" # 默认文件名为 paper.pdf
            test = SciHub()
            textEditber = self.ui.textEdit.toPlainText()
            test.download(textEditber, path= curPath + pdf_name)
            with open(curPath + pdf_name, 'rb') as f:
                pdf = PdfFileReader(f)
                info = pdf.getDocumentInfo()
                title = info.title

                if title != None and title != "":
                    file_name = title.replace(' ',"_")
                    file_name = file_name + ".pdf"
                    os.rename(curPath + pdf_name, curPath + "/" + file_name)
                else:
                    file_name = "paper.pdf"
        except:
            QMessageBox.information(self, '', '下载失败')

        else:
            QMessageBox.information(self, '', file_name + '下载完成')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    cutomUI = CustomUI()
    cutomUI.show()
    sys.exit(app.exec_())
```

> 对于一些功能较复杂的程序我们可以把这些进行逻辑操作的函数放到一个新的 `.py` 文件中，这样可以方便后期维护代码。但在这里因为程序比较简单，所以就直接放在主程序中了。
> 
> 踩过的坑：在 Qt 中， 当我们需要不调用 QFileDialog 保存文件时，得用 `QStandardPaths` 指定路径，否则打包出来的软件没法保存。

完成上面的步骤，直接运行程序就可以看到界面啦，复制 DOI 或 PMID，点击  **Download** 即可下载文献了~

![](https://tva1.sinaimg.cn/large/0081Kckwgy1gk1w7l1om1g30tx0c71kx.gif)

## 4. 打包程序为 Mac App

这里我们用 `pyinstaller` 来生成可执行程序，安装 `pyinstaller`：

```
pip install pyinstaller
```

准备一个软件图标 icon：

![](https://tva1.sinaimg.cn/large/0081Kckwly1gk8ex2hnruj303k03kt8l.jpg)

> 可用网站转换 png 至 ico 格式：https://www.easyicon.net/covert/

打包：

```
pyinstaller --windowed --onefile --clean --noconfirm scihub_gui.py -p scihub.py -i scihub.icns
```

在 `dist` 目录下即可看到打包好的程序：

![](https://tva1.sinaimg.cn/large/0081Kckwly1gk8f29i2wyj304t01i3ya.jpg)

要是你也装了 Anaconda，你会发现这么简单的小程序体积居然有 100M+，这是因为 Anaconda 里内置了很多库，打包的时候打包了很多不必要的模块进去。所有为了缩小 App 的体积，我们最好在一个新的虚拟环境中进行打包。

创建环境：

```
conda create -n scihubgui python=3.7
```

激活环境：

```
conda activate scihubgui
```

安装依赖：

```
pip install -r requirements.txt
```

- `requirements.txt`：

```
altgraph==0.17
beautifulsoup4==4.9.3
certifi==2020.6.20
chardet==3.0.4
idna==2.10
macholib==1.14
powerline-status==2.7
pyinstaller==4.0
pyinstaller-hooks-contrib==2020.9
PyPDF2==1.26.0
PyQt5==5.15.1
PyQt5-sip==12.8.1
PySocks==1.7.1
requests==2.24.0
retrying==1.3.3
six==1.15.0
soupsieve==2.0.1
urllib3==1.25.11
```

打包程序：

```
pyinstaller --windowed --onefile --clean --noconfirm scihub_gui.py -p scihub.py -i scihub.icns
```

现在可以看到程序的大小缩小了一半以上（但感觉还是太大了，需要再研究下）。

我已将所有代码上传至 GitHub：https://github.com/zwbao/scihub_gui

## 教程推荐

1. Qt Documentation： https://doc.qt.io/
2. Qt for Python： https://doc.qt.io/qtforpython/#project
3. PyQt5 中文教程： https://github.com/maicss/PyQt5-Chinese-tutorial
4. 《Python Qt GUI与数据可视化编程》


