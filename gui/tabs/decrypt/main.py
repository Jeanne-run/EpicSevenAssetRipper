from PyQt6.QtWidgets            import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QProgressBar, QCheckBox, QFileDialog
from PyQt6.QtCore               import pyqtSlot, Qt

from app.strings                import translate
from app.pack                   import DataPack
from app.full_decrypt           import decrypt_and_write, extract_all
from gui.components.button      import Button
from gui.util.thread_process    import QtThreadedProcess


class CreateTab(QWidget):
    order = 0
    _delete_encrypted_pack_after_decrypt = False
    _delete_decrypted_pack_after_extract = False

    encrypted_pack: DataPack = None
    decrypted_pack_destination: str = None

    pack_4_extraction: DataPack = None
    exctraction_path: str = None

    def __init__(self, parent: QWidget | QApplication):
        super().__init__(parent)
        self.name = f"{translate('decrypt')}/{translate('extract')}"
        vertical = QVBoxLayout()
        vertical.setSpacing(20)
        self.setLayout(vertical)
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row1.setSpacing(5)
        row2.setSpacing(5)
        vertical.addLayout(row1)
        vertical.addLayout(row2)
        vertical.addLayout(row3)
        vertical.addStretch()

        # Row 1
        select_encrypted = Button(self, text=translate('select_encrypted_pack'), pointer=True)
        select_encrypted.clicked.connect(self.select_encrypted_pack)
        row1.addWidget(select_encrypted)
        row1.setStretchFactor(select_encrypted, 2)

        decrypt_btn = Button(self, text=translate('output_path'), pointer=True)
        decrypt_btn.clicked.connect(self.select_decrypt_output)
        row1.addWidget(decrypt_btn)
        row1.setStretchFactor(decrypt_btn, 2)

        decrypt_btn = Button(self, text=translate('decrypt'), disabled=True, pointer=True)
        row1.addWidget(decrypt_btn)
        row1.setStretchFactor(decrypt_btn, 1)
        decrypt_btn.clicked.connect(self.start_decrypting)
        self.decrypt_btn = decrypt_btn


        self.decrypt_progressbar = QProgressBar(self)
        self.decrypt_progressbar.setObjectName("full_decrypt_progress_bar")
        row1.addWidget(self.decrypt_progressbar)
        row1.setStretchFactor(self.decrypt_progressbar, 5)



        # Row2
        select_decrypted = Button(self, text=translate('select_decrypted_pack'), pointer=True)
        select_decrypted.clicked.connect(self.select_decrypted_pack)
        row2.addWidget(select_decrypted)
        row2.setStretchFactor(select_decrypted, 2)

        extr_path_btn = Button(self, text=translate('output_path'), pointer=True)
        extr_path_btn.clicked.connect(self.select_extract_output_folder)
        row2.addWidget(extr_path_btn)
        row2.setStretchFactor(extr_path_btn, 2)

        extract_btn = Button(self, text=translate('extract'), disabled=True, pointer=True)
        extract_btn.clicked.connect(self.start_extracting)
        row2.addWidget(extract_btn)
        row2.setStretchFactor(extract_btn, 1)
        self.extract_btn = extract_btn


        self.extraction_progressbar = QProgressBar(self)
        self.extraction_progressbar.setObjectName("full_extract_progress_bar")
        row2.addWidget(self.extraction_progressbar)
        row2.setStretchFactor(self.extraction_progressbar, 5)



        # TODO
        self.checkbox_delete_pack_after = QCheckBox("Delete data.pack after decryption", self)
        self.checkbox_delete_pack_after.setChecked(self._delete_encrypted_pack_after_decrypt)
        self.checkbox_delete_pack_after.checkStateChanged.connect(self.changed_delete_encrypted_pack)
        row3.addWidget(self.checkbox_delete_pack_after)
        self.checkbox_delete_pack_after.setHidden(True)

        # TODO
        self.delete_after_extract = QCheckBox("Delete decrypted data.pack after extraction", self)
        self.delete_after_extract.setChecked(self._delete_decrypted_pack_after_extract)
        self.delete_after_extract.checkStateChanged.connect(self.changed_delete_decrypted_pack)
        row3.addWidget(self.delete_after_extract)
        self.delete_after_extract.setHidden(True)

    def update_btn_state(self):
        if self.encrypted_pack and self.decrypted_pack_destination:
            self.decrypt_btn.setEnabled(True)

        if self.pack_4_extraction and self.exctraction_path:
            self.extract_btn.setEnabled(True)

    @pyqtSlot()
    def select_encrypted_pack(self):
        fname, ext = QFileDialog.getOpenFileName(
            self,
            translate('select_encrypted_pack'),
            "",
            "Epic Seven data pack (*.pack)"
        )
        if fname:
            try:
                pack = DataPack(fname)
                if pack._is_encrypted != True:
                    raise Exception('Not encrypted!')
                self.encrypted_pack = pack
            except:
                pass

            self.update_btn_state()

    @pyqtSlot()
    def select_decrypt_output(self):
        fname, ext = QFileDialog.getSaveFileName(
            self,
            translate('output_path'),
            "",
            "Pack (*.pack *.zip *.tar);;", # ;; to allow all files
        )
        if fname:
            self.decrypted_pack_destination = fname
            self.update_btn_state()

    @pyqtSlot()
    def select_decrypted_pack(self):
        fname, ext = QFileDialog.getOpenFileName(
            self,
            translate('select_decrypted_pack'),
            "",
            "Epic Seven data pack (*.pack)",
        )
        if fname:
            try:
                self.pack_4_extraction = DataPack( fname )
            except Exception:
                pass
            
            self.update_btn_state()

    @pyqtSlot()
    def select_extract_output_folder(self):
        fname = QFileDialog.getExistingDirectory(
            self,
            translate('output_path'),
            "",
        )
        if fname:
            self.exctraction_path = fname
            self.update_btn_state()

    def changed_delete_encrypted_pack(self, event: Qt.CheckState):
        self._delete_encrypted_pack_after_decrypt = event.value == Qt.CheckState.Checked.value

    def changed_delete_decrypted_pack(self, event: Qt.CheckState):
        self._delete_decrypted_pack_after_extract = event.value == Qt.CheckState.Checked.value

    def start_decrypting(self):
        self.decrypt_progressbar.setValue(0)

        worker = QtThreadedProcess(self.encrypted_pack, decrypt_and_write, self.encrypted_pack, self.decrypted_pack_destination)
        QApplication.instance().property('MainWindow').closed.connect(worker.stop) # Stop running as soon as the main window is closed
        worker.onprogress = lambda a: self.decrypt_progressbar.setValue(a[0])
        worker.run()

    def start_extracting(self):
        self.extraction_progressbar.setValue(0)

        worker = QtThreadedProcess(self.encrypted_pack, extract_all, self.pack_4_extraction, self.exctraction_path)
        QApplication.instance().property('MainWindow').closed.connect(worker.stop) # Stop running as soon as the main window is closed
        worker.onprogress = lambda a: self.extraction_progressbar.setValue(a[0])
        worker.run()