import sys
import os
import datetime
import refactor
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit)


class RenameApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Movie Renamer")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 第一行：输入文件夹路径
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit(self)
        folder_button = QPushButton("选择文件夹", self)
        folder_button.clicked.connect(self.selectFolder)
        files_button = QPushButton("选择多个文件", self)
        files_button.clicked.connect(self.selectFiles)
        path_layout.addWidget(QLabel("路径:"))
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(folder_button)
        path_layout.addWidget(files_button)
        self.layout.addLayout(path_layout)

        # 第二行：输入匹配字符串
        match_layout = QHBoxLayout()
        self.match_input = QLineEdit(self)
        match_layout.addWidget(QLabel("匹配字符串:"))
        match_layout.addWidget(self.match_input)
        self.layout.addLayout(match_layout)

        # 第三行：输入偏移量
        offset_layout = QHBoxLayout()
        self.offset_input = QLineEdit(self)
        self.offset_input.setText('0')
        offset_layout.addWidget(QLabel("偏移量:"))
        offset_layout.addWidget(self.offset_input)
        self.layout.addLayout(offset_layout)

        # 重命名按钮
        rename_button = QPushButton("重命名", self)
        rename_button.clicked.connect(self.rename_files)
        self.layout.addWidget(rename_button)

        # 日志输出
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)

    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.path_input.setText(folder)

    def selectFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择多个文件")
        if files:
            self.path_input.setText(';'.join(files))

    def log(self, message):
        self.log_output.append(message)

    def rename_files(self):
        path_input = self.path_input.text()
        match_string = self.match_input.text()
        offset = int(self.offset_input.text())
        renameNum = 0

        if os.path.isdir(path_input):
            refactors = refactor.MovieRefactor(path_input)
            renameNum = refactors.RenameVideoFiles(match_string, offset)
            curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log(f'{curTime} 路径：{path_input} 共 {renameNum} 个文件重命名完成')
        else:
            file_paths = path_input.split(';')

            for file_path in file_paths:
                refactors = refactor.MovieRefactor(os.path.dirname(file_path))
                if refactors.RenameFile(file_path, match_string, offset):
                    curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.log(f'{curTime} {path_input} 重命名完成')
                    renameNum += 1

            curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if renameNum == 0:
                self.log(f'{curTime} 选中的文件无需重命名')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenameApp()
    window.show()
    sys.exit(app.exec_())