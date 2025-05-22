import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox, QProgressBar, QProgressDialog)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QItemSelectionModel
from PyQt5.QtGui import QIcon, QColor, QBrush, QPixmap
import shutil
import mdf_version_checker
import backup_version_checker

# Çeviri sözlüğü
translations = {
    "tr": {
        "title": "SQL DATA Version Checker",
        "scan": "Tara",
        "select_folder": "Klasör Seç",
        "test_all": "Tüm Listeyi Test Et",
        "move": "Taşı",
        "delete": "Sil",
        "success": "Başarılı",
        "fail": "Başarısız",
        "all": "Tümü",
        "select_all": "Tümünü Seç",
        "unselect_all": "Seçimi Kaldır",
        "filter_success": "Başarılı",
        "filter_fail": "Başarısız",
        "filter_all": "Tümü",
        "file_path": " Dosya Yolu",
        "test_result": "Test Sonucu",
        "sql_version": "SQL Sürümü",
        "progress_moving": "Dosyalar taşınıyor...",
        "progress_title": "Taşıma İşlemi",
        "move_error": "Taşıma Hatası",
        "move_exists": "zaten var, atlanıyor.",
        "move_failed": "taşınamadı:",
        "delete": "Sil",
        "delete_confirm": "Seçili {count} dosya silinsin mi?",
        "delete_error": "Silme Hatası",
        "delete_failed": "silinemedi:",
        "select_target": "Hedef Klasör Seç",
        "select_folder": "Klasör Seç",
        "no_files": "Dosya bulunamadı",
        "invalid_backup": "Geçersiz yedek dosyası (TAPE imzası yok)",
        "unknown_version": "Bilinmeyen Sürüm (Geçerli SQL Server yedeği)",
        "ok": "Tamam",
        "cancel": "İptal"
    },
    "en": {
        "title": "SQL DATA Version Checker",
        "scan": "Scan",
        "select_folder": "Select Folder",
        "test_all": "Test All",
        "move": "Move",
        "delete": "Delete",
        "success": "Success",
        "fail": "Failed",
        "all": "All",
        "select_all": "Select All",
        "unselect_all": "Unselect All",
        "filter_success": "Success",
        "filter_fail": "Failed",
        "filter_all": "All",
        "file_path": " File Path",
        "test_result": "Test Result",
        "sql_version": "SQL Version",
        "progress_moving": "Moving files...",
        "progress_title": "Move Operation",
        "move_error": "Move Error",
        "move_exists": "already exists, skipping.",
        "move_failed": "could not be moved:",
        "delete": "Delete",
        "delete_confirm": "Delete {count} selected files?",
        "delete_error": "Delete Error",
        "delete_failed": "could not be deleted:",
        "select_target": "Select Target Folder",
        "select_folder": "Select Folder",
        "no_files": "File not found",
        "invalid_backup": "Invalid backup file (no TAPE signature)",
        "unknown_version": "Unknown Version (Valid SQL Server backup)",
        "ok": "OK",
        "cancel": "Cancel"
    }
}

class TestThread(QThread):
    result_signal = pyqtSignal(int, str, str)
    progress_signal = pyqtSignal(int, int)

    def __init__(self, files):
        super().__init__()
        self.files = files

    def run(self):
        total = len(self.files)
        for idx, path in enumerate(self.files):
            try:
                version_code, version_name = self.check_version(path)
                if version_name:
                    self.result_signal.emit(idx, 'Başarılı', version_name)
                else:
                    self.result_signal.emit(idx, 'Başarısız', '-')
            except Exception:
                self.result_signal.emit(idx, 'Başarısız', '-')
            self.progress_signal.emit(idx + 1, total)

    def check_version(self, file_path):
        # mdf_version_checker.py içindeki mantığı tekrar kullan
        import struct
        VERSION_OFFSET = mdf_version_checker.VERSION_OFFSET
        SQL_SERVER_VERSIONS = mdf_version_checker.SQL_SERVER_VERSIONS
        with open(file_path, 'rb') as f:
            f.seek(VERSION_OFFSET)
            version_bytes = f.read(2)
            if len(version_bytes) < 2:
                return None, None
            version_code = struct.unpack('<H', version_bytes)[0]
            version_name = SQL_SERVER_VERSIONS.get(version_code)
            return version_code, version_name

class MultiTypeTestThread(QThread):
    result_signal = pyqtSignal(int, str, str)
    progress_signal = pyqtSignal(int, int)
    def __init__(self, files, base_folder):
        super().__init__()
        self.files = files
        self.base_folder = base_folder
    def run(self):
        total = len(self.files)
        for idx, path in enumerate(self.files):
            ext = path.lower().split('.')[-1]
            if ext == 'mdf':
                try:
                    import mdf_version_checker
                    import struct
                    VERSION_OFFSET = mdf_version_checker.VERSION_OFFSET
                    SQL_SERVER_VERSIONS = mdf_version_checker.SQL_SERVER_VERSIONS
                    with open(path, 'rb') as f:
                        f.seek(VERSION_OFFSET)
                        version_bytes = f.read(2)
                        if len(version_bytes) < 2:
                            self.result_signal.emit(idx, 'Başarısız', '-')
                        else:
                            version_code = struct.unpack('<H', version_bytes)[0]
                            version_name = SQL_SERVER_VERSIONS.get(version_code)
                            if version_name:
                                self.result_signal.emit(idx, 'Başarılı', version_name)
                            else:
                                self.result_signal.emit(idx, 'Başarısız', '-')
                except Exception:
                    self.result_signal.emit(idx, 'Başarısız', '-')
            elif ext in ('bak', 'bck'):
                try:
                    result, version = backup_version_checker.get_backup_version(path)
                    self.result_signal.emit(idx, result, version)
                except Exception:
                    self.result_signal.emit(idx, 'Başarısız', '-')
            else:
                self.result_signal.emit(idx, 'Başarısız', '-')
            self.progress_signal.emit(idx + 1, total)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_folder = ''
        self.test_thread = None
        self.all_rows = []
        self.current_lang = 'tr'
        self.init_ui()

    def tr(self, key, **kwargs):
        val = translations[self.current_lang].get(key, key)
        if kwargs:
            return val.format(**kwargs)
        return val

    def set_language(self, lang):
        self.current_lang = lang
        self.update_ui_texts()

    def update_ui_texts(self):
        self.setWindowTitle(self.tr('title'))
        self.scan_btn.setText(self.tr('scan'))
        self.folder_btn.setToolTip(self.tr('select_folder'))
        self.test_btn.setText(self.tr('test_all'))
        self.btn_move.setText(self.tr('move'))
        self.btn_delete.setText(self.tr('delete'))
        self.btn_all.setText(self.tr('filter_all'))
        self.btn_success.setText(self.tr('filter_success'))
        self.btn_fail.setText(self.tr('filter_fail'))
        self.btn_select_all.setText(self.tr('select_all'))
        self.btn_unselect_all.setText(self.tr('unselect_all'))
        self.table.setHorizontalHeaderLabels([
            self.tr('file_path'), self.tr('test_result'), self.tr('sql_version')
        ])

    def init_ui(self):
        main_layout = QVBoxLayout()
        # Dil seçici bayraklar
        lang_layout = QHBoxLayout()
        lang_layout.addStretch()
        self.tr_flag = QLabel()
        self.tr_flag.setPixmap(QPixmap(os.path.join('icons', 'tr_flag.png')).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.tr_flag.mousePressEvent = lambda e: self.set_language('tr')
        self.en_flag = QLabel()
        self.en_flag.setPixmap(QPixmap(os.path.join('icons', 'en_flag.png')).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.en_flag.mousePressEvent = lambda e: self.set_language('en')
        lang_layout.addWidget(self.tr_flag)
        lang_layout.addWidget(self.en_flag)
        main_layout.addLayout(lang_layout)
        header_layout = QHBoxLayout()

        # Dashboard icon
        dashboard_icon = QSvgWidget(os.path.join('icons', 'home.svg'))
        dashboard_icon.setFixedSize(32, 32)
        header_layout.addWidget(dashboard_icon)
        header_layout.addWidget(QLabel('<b>SQL MDF Version Checker</b>'))
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

        # Folder select
        folder_layout = QHBoxLayout()
        self.folder_line = QLineEdit()
        self.folder_line.setReadOnly(True)
        self.folder_btn = QPushButton()
        self.folder_btn.setToolTip(self.tr('select_folder'))
        self.folder_btn.setIcon(self.svg_icon('folder.svg'))
        self.folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_line)
        folder_layout.addWidget(self.folder_btn)
        main_layout.addLayout(folder_layout)

        # Scan button
        self.scan_btn = QPushButton(self.tr('scan'))
        self.scan_btn.setIcon(self.svg_icon('search.svg'))
        self.scan_btn.clicked.connect(self.scan_folder)
        main_layout.addWidget(self.scan_btn)

        # Filtre ve toplu seçim butonları
        filter_layout = QHBoxLayout()
        self.btn_all = QPushButton(self.tr('filter_all'))
        self.btn_all.setIcon(self.svg_icon('filter.svg'))
        self.btn_all.clicked.connect(self.show_all)
        self.btn_success = QPushButton(self.tr('filter_success'))
        self.btn_success.setIcon(self.svg_icon('check.svg'))
        self.btn_success.clicked.connect(self.show_success)
        self.btn_fail = QPushButton(self.tr('filter_fail'))
        self.btn_fail.setIcon(self.svg_icon('x.svg'))
        self.btn_fail.clicked.connect(self.show_fail)
        filter_layout.addWidget(self.btn_all)
        filter_layout.addWidget(self.btn_success)
        filter_layout.addWidget(self.btn_fail)
        filter_layout.addStretch()
        self.btn_select_all = QPushButton(self.tr('select_all'))
        self.btn_select_all.setIcon(self.svg_icon('plus-square.svg'))
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_unselect_all = QPushButton(self.tr('unselect_all'))
        self.btn_unselect_all.setIcon(self.svg_icon('minus-square.svg'))
        self.btn_unselect_all.clicked.connect(self.unselect_all)
        filter_layout.addWidget(self.btn_select_all)
        filter_layout.addWidget(self.btn_unselect_all)
        main_layout.addLayout(filter_layout)

        # Table for results
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels([self.tr('file_path'), self.tr('test_result'), self.tr('sql_version')])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        main_layout.addWidget(self.table)

        # Test All button
        self.test_btn = QPushButton(self.tr('test_all'))
        self.test_btn.setIcon(self.svg_icon('play.svg'))
        self.test_btn.clicked.connect(self.test_all)
        main_layout.addWidget(self.test_btn)

        # Toplu işlem butonları
        batch_layout = QHBoxLayout()
        self.btn_move = QPushButton(self.tr('move'))
        self.btn_move.setIcon(self.svg_icon('move.svg'))
        self.btn_move.clicked.connect(self.move_selected)
        self.btn_delete = QPushButton(self.tr('delete'))
        self.btn_delete.setIcon(self.svg_icon('trash-2.svg'))
        self.btn_delete.clicked.connect(self.delete_selected)
        batch_layout.addWidget(self.btn_move)
        batch_layout.addWidget(self.btn_delete)
        batch_layout.addStretch()
        main_layout.addLayout(batch_layout)

        # En alt bilgi satırı
        bottom_layout = QHBoxLayout()
        copyright_label = QLabel('2025 GOLD DATA Tüm hakları saklıdır.')
        copyright_label.setStyleSheet('color: #888; font-size: 10pt;')
        copyright_label.setAlignment(Qt.AlignRight)
        bottom_layout.addWidget(copyright_label, stretch=0, alignment=Qt.AlignRight)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def svg_icon(self, name):
        svg_path = os.path.join('icons', name)
        return QIcon(svg_path)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr('select_folder'))
        if folder:
            self.selected_folder = folder
            self.folder_line.setText(folder)

    def scan_folder(self):
        if not self.selected_folder:
            return
        mdf_files = []
        for root, _, files in os.walk(self.selected_folder):
            for file in files:
                ext = file.lower().split('.')[-1]
                if ext in ('mdf', 'bak', 'bck'):
                    mdf_files.append(os.path.join(root, file))
        self.table.setRowCount(0)
        self.all_rows = []
        for path in mdf_files:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(path))
            self.table.setItem(row, 1, QTableWidgetItem(''))
            self.table.setItem(row, 2, QTableWidgetItem(''))
            self.all_rows.append([path, '', ''])

    def test_all(self):
        files = [self.table.item(row, 0).text() for row in range(self.table.rowCount())]
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.progress.setMaximum(len(files))
        self.test_thread = MultiTypeTestThread(files, self.selected_folder)
        self.test_thread.result_signal.connect(self.update_result)
        self.test_thread.progress_signal.connect(self.update_progress)
        self.test_thread.finished.connect(self.hide_progress)
        self.test_thread.start()

    def update_result(self, row, result, version):
        # Test Sonucu sütununa ikon+renkli yazı ekle
        if result == 'Başarılı':
            icon = QIcon(os.path.join('icons', 'check.svg'))
            item = QTableWidgetItem(icon, ' Başarılı')
            item.setForeground(QBrush(QColor(0, 150, 0)))
        elif result == 'Başarısız':
            icon = QIcon(os.path.join('icons', 'x.svg'))
            item = QTableWidgetItem(icon, ' Başarısız')
            item.setForeground(QBrush(QColor(200, 0, 0)))
        else:
            item = QTableWidgetItem(result)
        self.table.setItem(row, 1, item)
        self.table.setItem(row, 2, QTableWidgetItem(version))
        if row < len(self.all_rows):
            self.all_rows[row][1] = result
            self.all_rows[row][2] = version

    def update_progress(self, current, total):
        self.progress.setValue(current)
        self.progress.setMaximum(total)

    def hide_progress(self):
        self.progress.setVisible(False)

    # Filtreleme fonksiyonları
    def show_all(self):
        self.table.setRowCount(0)
        for row in self.all_rows:
            self._add_row(row)
    def show_success(self):
        self.table.setRowCount(0)
        for row in self.all_rows:
            if row[1] == 'Başarılı':
                self._add_row(row)
    def show_fail(self):
        self.table.setRowCount(0)
        for row in self.all_rows:
            if row[1] == 'Başarısız':
                self._add_row(row)
    def _add_row(self, rowdata):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(rowdata[0]))
        # Test Sonucu sütununa ikon+renkli yazı ekle
        if rowdata[1] == 'Başarılı':
            icon = QIcon(os.path.join('icons', 'check.svg'))
            item = QTableWidgetItem(icon, ' Başarılı')
            item.setForeground(QBrush(QColor(0, 150, 0)))
        elif rowdata[1] == 'Başarısız':
            icon = QIcon(os.path.join('icons', 'x.svg'))
            item = QTableWidgetItem(icon, ' Başarısız')
            item.setForeground(QBrush(QColor(200, 0, 0)))
        else:
            item = QTableWidgetItem(rowdata[1])
        self.table.setItem(row, 1, item)
        self.table.setItem(row, 2, QTableWidgetItem(rowdata[2]))

    # Toplu seçim
    def select_all(self):
        # Sadece ekranda görünen (filtrelenmiş) satırları seç, mavi seçim rengiyle
        self.table.clearSelection()
        for row in range(self.table.rowCount()):
            self.table.selectionModel().select(
                self.table.model().index(row, 0),
                QItemSelectionModel.Select | QItemSelectionModel.Rows
            )
    def unselect_all(self):
        self.table.clearSelection()

    # Toplu işlem (şimdilik print)
    def move_selected(self):
        selected = self.table.selectionModel().selectedRows()
        files = [self.table.item(idx.row(), 0).text() for idx in selected]
        if not files:
            return
        target = QFileDialog.getExistingDirectory(self, self.tr('select_target'))
        if not target:
            return
        progress = QProgressDialog(self.tr('progress_moving'), self.tr('cancel'), 0, len(files), self)
        progress.setWindowTitle(self.tr('progress_title'))
        progress.setWindowModality(Qt.WindowModal)
        progress.setValue(0)
        for i, f in enumerate(files):
            if progress.wasCanceled():
                break
            try:
                rel_path = os.path.relpath(f, self.selected_folder)
                dest_path = os.path.join(target, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                if os.path.exists(dest_path):
                    QMessageBox.warning(self, self.tr('move_error'), f'{dest_path} {self.tr("move_exists")}')
                    continue
                shutil.move(f, dest_path)
            except Exception as e:
                QMessageBox.warning(self, self.tr('move_error'), f'{f} {self.tr("move_failed")} {e}')
            progress.setValue(i + 1)
        progress.close()
        self.scan_folder()

    def delete_selected(self):
        selected = self.table.selectionModel().selectedRows()
        files = [self.table.item(idx.row(), 0).text() for idx in selected]
        if not files:
            return
        reply = QMessageBox.question(self, 'Silme Onayı', f'Seçili {len(files)} dosya silinsin mi?', QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        for f in files:
            try:
                os.remove(f)
            except Exception as e:
                QMessageBox.warning(self, 'Silme Hatası', f'{f} silinemedi: {e}')
        self.scan_folder() 