import os
import shutil
from typing import List, Tuple

from PyQt6 import QtCore, QtGui, QtWidgets

# Reuse data from the tkinter version (expects file_sorter.py in same folder)
from file_sorter import CATEGORIES, LANGUAGES, ABOUT_TEXT

ABOUT_TEXT_EN = (
    "File Sorter v5.0\n\n"
    "Author: Fal1sev4n\n\n"
    "I want to eat shawarma\n\n"
    "GitHub: https://github.com/faliseven"
)
INSTRUCTIONS = {
    'ru': (
        "Как пользоваться FileSorter:\n\n"
        "1) Нажмите «Обзор» и выберите папку.\n"
        "2) Отметьте категории слева (можно искать по названию).\n"
        "3) При необходимости включите «Сортировать во вложенных папках».\n"
        "4) «Предпросмотр» — показывает план без перемещения файлов.\n"
        "5) «Сортировать» — перемещает файлы по подпапкам категорий.\n"
        "6) «Возврат» — отменяет последнее перемещение.\n\n"
        "Примечание: подпапка «Folders» собирает найденные папки (если включена)."
    ),
    'en': (
        "How to use FileSorter:\n\n"
        "1) Click “Browse” and select a folder.\n"
        "2) Check categories on the left (you can search by name).\n"
        "3) Enable “Sort in subfolders” if needed.\n"
        "4) “Preview” shows the plan without moving files.\n"
        "5) “Sort” moves files into category subfolders.\n"
        "6) “Undo” reverts the last move operation.\n\n"
        "Note: the “Folders” subfolder collects found directories (if enabled)."
    ),
}


class SortWorker(QtCore.QObject):
    progressChanged = QtCore.pyqtSignal(int)
    movedOne = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)

    def __init__(self, folder: str, selected_cats: List[str], recursive: bool, lang: str = 'ru'):
        super().__init__()
        self.folder = folder
        self.selected_cats = selected_cats
        self.recursive = recursive
        self.lang = lang
        self._last_moves: List[Tuple[str, str]] = []
        self._abort = False

    def request_abort(self):
        self._abort = True

    @property
    def last_moves(self) -> List[Tuple[str, str]]:
        return self._last_moves

    def _get_files(self, folder: str, recursive: bool) -> List[str]:
        files: List[str] = []
        for root, dirs, filenames in os.walk(folder):
            for name in filenames:
                files.append(os.path.join(root, name))
            if recursive:
                for d in dirs:
                    files.append(os.path.join(root, d))
            if not recursive:
                break
        return files

    def t(self, key: str, *args) -> str:
        try:
            return LANGUAGES[self.lang].get(key, key).format(*args)
        except Exception:
            return key
    @QtCore.pyqtSlot()
    def run(self):
        files = self._get_files(self.folder, self.recursive)
        total = max(len(files), 1)
        moved = 0

        for idx, item_path in enumerate(files):
            if self._abort:
                break
            item = os.path.basename(item_path)
            # folders handling
            if os.path.isdir(item_path):
                if 'Folders' in self.selected_cats:
                    dest_dir = os.path.join(os.path.dirname(item_path), 'Folders')
                    os.makedirs(dest_dir, exist_ok=True)
                    try:
                        dest_path = os.path.join(dest_dir, item)
                        shutil.move(item_path, dest_path)
                        self._last_moves.append((dest_path, item_path))
                        self.movedOne.emit(self.t('moved_folder', item))
                        moved += 1
                    except Exception as e:
                        self.movedOne.emit(self.t('error_folder', item, e))
                self.progressChanged.emit(int((idx + 1) * 100 / total))
                QtCore.QCoreApplication.processEvents()
                continue

            ext = os.path.splitext(item)[1].lower()
            moved_flag = False
            for cat in self.selected_cats:
                if cat == 'Folders':
                    continue
                keys = CATEGORIES.get(cat, [])
                if ext in keys or any(k in item.lower() for k in keys if not k.startswith('.')):
                    dest_dir = os.path.join(os.path.dirname(item_path), cat)
                    os.makedirs(dest_dir, exist_ok=True)
                    try:
                        dest_path = os.path.join(dest_dir, item)
                        shutil.move(item_path, dest_path)
                        self._last_moves.append((dest_path, item_path))
                        self.movedOne.emit(self.t('moved', item, cat))
                        moved += 1
                    except Exception as e:
                        self.movedOne.emit(self.t('error', item, e))
                    moved_flag = True
                    break
            if not moved_flag:
                self.movedOne.emit(self.t('skipped', item))

            self.progressChanged.emit(int((idx + 1) * 100 / total))
            QtCore.QCoreApplication.processEvents()

        self.finished.emit(moved)


class FileSorterQt(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FileSorter Qt")
        self.resize(920, 680)
        self.setWindowOpacity(0.96)  # translucent
        self._set_dark_minimal_palette()

        self.lang = 'ru'
        self._thread: QtCore.QThread | None = None
        self._worker: SortWorker | None = None
        self._last_moves: List[Tuple[str, str]] = []

        self._build_ui()

    def _set_dark_minimal_palette(self):
        QtWidgets.QApplication.setStyle("Fusion")
        palette = QtGui.QPalette()
        base = QtGui.QColor(17, 19, 26)
        panel = QtGui.QColor(20, 23, 33)
        text = QtGui.QColor(235, 235, 235)
        acc = QtGui.QColor(0, 224, 255)
        palette.setColor(QtGui.QPalette.ColorRole.Window, base)
        palette.setColor(QtGui.QPalette.ColorRole.WindowText, text)
        palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(15, 17, 23))
        palette.setColor(QtGui.QPalette.ColorRole.AlternateBase, panel)
        palette.setColor(QtGui.QPalette.ColorRole.ToolTipBase, panel)
        palette.setColor(QtGui.QPalette.ColorRole.ToolTipText, text)
        palette.setColor(QtGui.QPalette.ColorRole.Text, text)
        palette.setColor(QtGui.QPalette.ColorRole.Button, panel)
        palette.setColor(QtGui.QPalette.ColorRole.ButtonText, text)
        palette.setColor(QtGui.QPalette.ColorRole.BrightText, acc)
        palette.setColor(QtGui.QPalette.ColorRole.Highlight, acc)
        palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(0, 0, 0))
        self.setPalette(palette)

    def _build_ui(self):
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        root = QtWidgets.QGridLayout(central)
        root.setContentsMargins(8, 8, 8, 8)
        root.setHorizontalSpacing(6)
        root.setVerticalSpacing(6)

        # Top header with title + actions
        header = QtWidgets.QWidget()
        header_l = QtWidgets.QHBoxLayout(header)
        header_l.setContentsMargins(4, 0, 4, 0)
        header_l.setSpacing(6)
        self.title_lbl = QtWidgets.QLabel("FileSorter")
        f = self.title_lbl.font()
        f.setBold(True)
        self.title_lbl.setFont(f)
        header_l.addWidget(self.title_lbl)
        header_l.addStretch(1)
        self.btn_about = QtWidgets.QPushButton(self.t('about'))
        self.btn_help = QtWidgets.QPushButton("Help" if self.lang == 'en' else "Инструкция")
        self.btn_lang = QtWidgets.QPushButton(self.t('lang'))
        self.btn_about.clicked.connect(self._show_about)
        self.btn_help.clicked.connect(self._show_help)
        self.btn_lang.clicked.connect(self._toggle_lang)
        header_l.addWidget(self.btn_about)
        header_l.addWidget(self.btn_help)
        header_l.addWidget(self.btn_lang)

        # Sidebar
        sidebar = QtWidgets.QFrame()
        sidebar.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        sidebar_l = QtWidgets.QVBoxLayout(sidebar)
        sidebar_l.setContentsMargins(12, 10, 12, 10)
        sidebar_l.setSpacing(8)

        self.cat_label = QtWidgets.QLabel(self.t('categories'))
        font = self.cat_label.font()
        font.setBold(True)
        self.cat_label.setFont(font)
        sidebar_l.addWidget(self.cat_label)

        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText("Поиск...")
        self.search.textChanged.connect(self._filter_categories)
        sidebar_l.addWidget(self.search)

        self.cat_list = QtWidgets.QListWidget()
        self.cat_list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self._populate_categories()
        sidebar_l.addWidget(self.cat_list, 1)

        btns_side = QtWidgets.QHBoxLayout()
        self.btn_all = QtWidgets.QPushButton(self.t('select_all'))
        self.btn_none = QtWidgets.QPushButton(self.t('deselect_all'))
        self.btn_all.clicked.connect(self._select_all)
        self.btn_none.clicked.connect(self._deselect_all)
        btns_side.addWidget(self.btn_all)
        btns_side.addWidget(self.btn_none)
        sidebar_l.addLayout(btns_side)

        # Center
        center = QtWidgets.QFrame()
        center_l = QtWidgets.QGridLayout(center)
        center_l.setContentsMargins(12, 10, 12, 10)
        center_l.setSpacing(8)

        path_row = QtWidgets.QHBoxLayout()
        self.lbl_folder = QtWidgets.QLabel(self.t('select_folder'))
        path_row.addWidget(self.lbl_folder)
        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.setReadOnly(True)
        path_row.addWidget(self.path_edit, 1)
        self.btn_browse = QtWidgets.QPushButton(self.t('browse'))
        self.btn_browse.clicked.connect(self._browse)
        path_row.addWidget(self.btn_browse)
        center_l.addLayout(path_row, 0, 0)

        row_btns = QtWidgets.QHBoxLayout()
        self.btn_undo = QtWidgets.QPushButton(f"↺ {self.t('undo')}")
        self.btn_prev = QtWidgets.QPushButton(f"◧ {self.t('preview')}")
        self.btn_sort = QtWidgets.QPushButton(f"⮞ {self.t('sort')}")
        self.btn_open = QtWidgets.QPushButton(f"⌂ {self.t('open_folder')}")
        row_btns.addWidget(self.btn_undo)
        row_btns.addWidget(self.btn_prev)
        row_btns.addWidget(self.btn_sort)
        row_btns.addWidget(self.btn_open)
        center_l.addLayout(row_btns, 1, 0)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(10)
        center_l.addWidget(self.progress, 2, 0)

        self.preview = QtWidgets.QPlainTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText(self.t('plan'))
        center_l.addWidget(self.preview, 3, 0)

        self.count_lbl = QtWidgets.QLabel("")
        center_l.addWidget(self.count_lbl, 4, 0)

        self.log = QtWidgets.QPlainTextEdit()
        self.log.setReadOnly(True)
        center_l.addWidget(self.log, 5, 0)

        # Status
        status = QtWidgets.QStatusBar()
        self.setStatusBar(status)
        self.status_main = QtWidgets.QLabel(self.t('done'))
        self.status_path = QtWidgets.QLabel("")
        status.addWidget(self.status_main, 1)
        status.addPermanentWidget(self.status_path, 1)

        # Assemble (header in row 0; content in row 1)
        root.addWidget(header, 0, 0, 1, 2)
        root.addWidget(sidebar, 1, 0, 1, 1)
        root.addWidget(center, 1, 1, 1, 1)
        root.setColumnStretch(1, 1)
        root.setRowStretch(1, 1)

        # Controls
        self.recursive = QtWidgets.QCheckBox(self.t('recursive'))
        sidebar_l.addWidget(self.recursive)

        self.btn_prev.clicked.connect(self._preview)
        self.btn_sort.clicked.connect(self._start_sort)
        self.btn_open.clicked.connect(self._open_folder)
        self.btn_undo.clicked.connect(self._undo)

    # --- i18n helpers ---
    def t(self, key: str, *args) -> str:
        try:
            return LANGUAGES[self.lang].get(key, key).format(*args)
        except Exception:
            return key

    def _toggle_lang(self):
        self.lang = 'en' if self.lang == 'ru' else 'ru'
        self._retranslate()
        QtWidgets.QMessageBox.information(self, self.t('lang'), f"{self.t('lang')}: {self.lang.upper()}")

    def _retranslate(self):
        self.title_lbl.setText("FileSorter")
        self.btn_about.setText(self.t('about'))
        # update help/instruction button
        if hasattr(self, 'btn_help'):
            self.btn_help.setText("Help" if self.lang == 'en' else "Инструкция")
        self.btn_lang.setText(self.t('lang'))
        self.cat_label.setText(self.t('categories'))
        self.search.setPlaceholderText("Search..." if self.lang == 'en' else "Поиск...")
        self.lbl_folder.setText(self.t('select_folder'))
        self.btn_browse.setText(self.t('browse'))
        # update sidebar select buttons
        if hasattr(self, 'btn_all'):
            self.btn_all.setText(self.t('select_all'))
        if hasattr(self, 'btn_none'):
            self.btn_none.setText(self.t('deselect_all'))
        self.btn_undo.setText(f"↺ {self.t('undo')}")
        self.btn_prev.setText(f"◧ {self.t('preview')}")
        self.btn_sort.setText(f"⮞ {self.t('sort')}")
        self.btn_open.setText(f"⌂ {self.t('open_folder')}")
        self.preview.setPlaceholderText(self.t('plan'))
        self.recursive.setText(self.t('recursive'))
        # list items remain the same (category labels are titles)

    def _show_about(self):
        content = ABOUT_TEXT if self.lang == 'ru' else ABOUT_TEXT_EN
        QtWidgets.QMessageBox.information(self, self.t('about'), content)

    def _show_help(self):
        text = INSTRUCTIONS.get(self.lang, INSTRUCTIONS['en'])
        QtWidgets.QMessageBox.information(self, "Help" if self.lang == 'en' else "Инструкция", text)

    def _populate_categories(self):
        self.cat_list.clear()
        for cat in CATEGORIES:
            item = QtWidgets.QListWidgetItem(cat)
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.CheckState.Checked)
            self.cat_list.addItem(item)

    def _filter_categories(self, text: str):
        text = text.lower()
        for i in range(self.cat_list.count()):
            it = self.cat_list.item(i)
            it.setHidden(text not in it.text().lower())

    def _select_all(self):
        for i in range(self.cat_list.count()):
            self.cat_list.item(i).setCheckState(QtCore.Qt.CheckState.Checked)

    def _deselect_all(self):
        for i in range(self.cat_list.count()):
            self.cat_list.item(i).setCheckState(QtCore.Qt.CheckState.Unchecked)

    def _browse(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Выбор папки", "")
        if folder:
            self.path_edit.setText(folder)
            self.status_path.setText(folder)

    def _selected_categories(self) -> List[str]:
        cats: List[str] = []
        for i in range(self.cat_list.count()):
            it = self.cat_list.item(i)
            if it.checkState() == QtCore.Qt.CheckState.Checked:
                cats.append(it.text())
        return cats

    def _get_files(self, folder: str, recursive: bool) -> List[str]:
        files: List[str] = []
        for root, dirs, filenames in os.walk(folder):
            for name in filenames:
                files.append(os.path.join(root, name))
            if recursive:
                for d in dirs:
                    files.append(os.path.join(root, d))
            if not recursive:
                break
        return files

    def _preview(self):
        folder = self.path_edit.text().strip()
        if not folder:
            QtWidgets.QMessageBox.information(self, self.t('done'), self.t('choose_folder'))
            return
        selected = self._selected_categories()
        if not selected:
            QtWidgets.QMessageBox.information(self, self.t('done'), self.t('choose_category'))
            return
        files = self._get_files(folder, self.recursive.isChecked())
        plan: List[str] = []
        for item_path in files:
            item = os.path.basename(item_path)
            if os.path.isdir(item_path):
                if 'Folders' in selected:
                    plan.append(self.t('moved_folder', item))
                continue
            ext = os.path.splitext(item)[1].lower()
            found = False
            for cat in selected:
                if cat == 'Folders':
                    continue
                keys = CATEGORIES.get(cat, [])
                if ext in keys or any(k in item.lower() for k in keys if not k.startswith('.')):
                    plan.append(self.t('moved', item, cat))
                    found = True
                    break
            if not found:
                plan.append(self.t('preview_stays', item))
        self.preview.setPlainText("\n".join(plan))

    def _append_log(self, text: str):
        self.log.appendPlainText(text)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

    def _start_sort(self):
        folder = self.path_edit.text().strip()
        if not folder:
            QtWidgets.QMessageBox.information(self, self.t('done'), self.t('choose_folder'))
            return
        selected = self._selected_categories()
        if not selected:
            QtWidgets.QMessageBox.information(self, self.t('done'), self.t('choose_category'))
            return

        self.log.clear()
        self.preview.clear()
        self.count_lbl.setText("")
        self.progress.setValue(0)
        self.status_main.setText("Sorting..." if self.lang == 'en' else "Сортировка...")

        self._thread = QtCore.QThread(self)
        self._worker = SortWorker(folder, selected, self.recursive.isChecked(), lang=self.lang)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progressChanged.connect(self.progress.setValue)
        self._worker.movedOne.connect(self._append_log)
        self._worker.finished.connect(self._sort_finished)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def _sort_finished(self, moved: int):
        if self._worker:
            self._last_moves = self._worker.last_moves
        self.count_lbl.setText(self.t('sorted_files', moved))
        self.status_main.setText(self.t('done'))
        QtWidgets.QMessageBox.information(self, self.t('done'), self.t('sorted_files', moved))

    def _open_folder(self):
        folder = self.path_edit.text().strip()
        if folder:
            try:
                os.startfile(folder)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, self.t('done'), self.t('error', folder, e))

    def _undo(self):
        if not self._last_moves:
            QtWidgets.QMessageBox.information(self, self.t('undo'), self.t('no_history'))
            return
        errors = 0
        for dest, src in reversed(self._last_moves):
            try:
                os.makedirs(os.path.dirname(src), exist_ok=True)
                shutil.move(dest, src)
            except Exception:
                errors += 1
        self._last_moves.clear()
        if errors == 0:
            QtWidgets.QMessageBox.information(self, self.t('undo'), self.t('undo_success'))
        else:
            QtWidgets.QMessageBox.warning(self, self.t('undo'), self.t('undo_partial', errors))


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = FileSorterQt()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

