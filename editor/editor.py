#!/usr/bin/env python3

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QShortcut
from PyQt5.QtGui import QKeySequence

from dictionarytreeview import DictionaryTreeView


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('editor.ui', self)

        self.tree_view = self.findChild(DictionaryTreeView, 'tree_view')

        # Close window (and application) on Ctrl+Q
        shortcut_close = QShortcut(QKeySequence('Ctrl+Q'), self)
        shortcut_close.activated.connect(self.close)

        # Save and open files
        action_open = self.findChild(QAction, 'action_open')
        action_save = self.findChild(QAction, 'action_save')

        action_save.triggered.connect(self.print_tree)

    def print_tree(self):
        tree = self.tree_view.model.rootItem.toDict()
        print(tree)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec())

