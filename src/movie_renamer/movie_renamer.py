import sys
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
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit(self)
        folder_button = QPushButton("选择文件夹", self)
        folder_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(QLabel("文件夹路径:"))
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(folder_button)
        self.layout.addLayout(folder_layout)

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

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.folder_input.setText(folder)

    def log(self, message):
        self.log_output.append(message)

    def rename_files(self):
        folder_path = self.folder_input.text()
        match_string = self.match_input.text()
        offset = int(self.offset_input.text())
        refactors = refactor.MovieRefactor(folder_path)
        renameNum = refactors.RenameVideoFiles(match_string, offset)

        self.log(f'文件夹：{folder_path} 共 {renameNum} 个文件重命名完成')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenameApp()
    window.show()
    sys.exit(app.exec_())