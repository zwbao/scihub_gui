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
            curPath = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
            pdf_name = "/paper.pdf"
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