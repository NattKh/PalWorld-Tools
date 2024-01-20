import sys
import os
import requests
import zipfile, tempfile, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QMessageBox
import json
import helper  # Import the helper module

class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.gameFolderPath = None
        self.addedFiles = []  # List to keep track of added files
        self.initUI()
        self.handle_errors(self.load_startup_config)
        
    def handle_errors(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            self.infoLabel.setText(f'Error: {e}')
    def load_startup_config(self):
        patch_data = self.load_patch_data()
        if patch_data:
            self.gameFolderPath = patch_data['folder_path']
            self.addedFiles = patch_data['added_files']
            self.folderPathLabel.setText(f'Selected Folder: {self.gameFolderPath}')
            self.patchGameBtn.setEnabled(True)
            self.unpatchBtn.setEnabled(True)
        else:
            self.folderPathLabel.setText('No folder selected')
            self.patchGameBtn.setEnabled(False)
            self.unpatchBtn.setEnabled(False)
    
    def initUI(self):
        self.setWindowTitle('PalWorlds Mod Patcher')
        layout = QVBoxLayout()

        self.infoLabel = QLabel('INFO: Pal World default Game path: Steam\steamapps\common\Palworld\Pal\Binaries\Win64')
        layout.addWidget(self.infoLabel)
        self.infoLabel2 = QLabel('WARNING: This will download "UE4SS DevKit" and apply the custom patch made to the game.')
        layout.addWidget(self.infoLabel2)
        self.infoLabel3 = QLabel('INFO: Unpatch will only work with Admin folder permission to delete the files added by the patch, for manual deletion check json file for added files.')
        layout.addWidget(self.infoLabel3)

        self.infoLabel6 = QLabel('STEP 1. Select PalWorld Game Path, STEP 2. Patch Game, STEP 3. Modify Mods.txt, STEP 4. Restart Game')
        layout.addWidget(self.infoLabel6)
        self.folderPathLabel = QLabel('No folder selected please ')
        layout.addWidget(self.folderPathLabel)

        self.selectFolderBtn = QPushButton('Select PalWorld Game Path', self)
        self.selectFolderBtn.clicked.connect(self.select_folder)
        layout.addWidget(self.selectFolderBtn)

        self.patchGameBtn = QPushButton('Patch Game', self)
        self.patchGameBtn.clicked.connect(self.patch_game)
        self.patchGameBtn.setEnabled(False)  # Disable this button initially
        layout.addWidget(self.patchGameBtn)
        
        self.unpatchBtn = QPushButton('Unpatch Everything', self)
        self.unpatchBtn.clicked.connect(self.unpatch_game)
        self.unpatchBtn.setEnabled(False)  # Disable this button initially
        layout.addWidget(self.unpatchBtn)


        # Button for managing mods
        self.infoLabel4 = QLabel('INFO: Enable/Disable Below - 0 = Disable, 1 = Enable.')
        layout.addWidget(self.infoLabel4)
        self.infoLabel5 = QLabel('INFO: Restart Game for it to take effect.')
        layout.addWidget(self.infoLabel5)
        self.manageModsBtn = QPushButton('Manage Mods.txt', self)
        self.manageModsBtn.clicked.connect(self.manage_mods)
        layout.addWidget(self.manageModsBtn)

        self.setLayout(layout)
        self.show()
        
    def manage_mods(self):
        self.handle_errors(self._manage_mods)

    def _manage_mods(self):
        result = helper.manage_mods(self.gameFolderPath)
        QMessageBox.information(self, "Manage Mods", result)


    def select_folder(self):
        self.gameFolderPath = QFileDialog.getExistingDirectory(self, "Select Game Directory")
        if self.gameFolderPath:
            self.folderPathLabel.setText(f'Selected Folder: {self.gameFolderPath}')
            self.patchGameBtn.setEnabled(True)
            self.unpatchBtn.setEnabled(True)
            self.save_patch_data()
        else:
            self.folderPathLabel.setText('No folder selected')
            self.patchGameBtn.setEnabled(False)
            self.unpatchBtn.setEnabled(False)

    def patch_game(self):
        if self.gameFolderPath:
            self.handle_errors(self._perform_patching)

    def _perform_patching(self):
        self.infoLabel.setText('Downloading...')
        zip_url = 'https://github.com/UE4SS-RE/RE-UE4SS/releases/download/v2.5.2/zDEV-UE4SS_Xinput_v2.5.2.zip'
        zip_path = os.path.join(tempfile.gettempdir(), 'downloaded.zip')
        self.download_file(zip_url, zip_path)
        self.infoLabel.setText('Unzipping tool...')

        with tempfile.TemporaryDirectory() as temp_dir:
            self.unzip_file(zip_path, temp_dir)
            self.copy_contents(temp_dir, self.gameFolderPath)

        # Delete existing Mods folder and UE4SS-settings.ini file if they exist
        mods_folder_path = os.path.join(self.gameFolderPath, 'Mods')
        settings_ini_path = os.path.join(self.gameFolderPath, 'UE4SS-settings.ini')
        if os.path.exists(mods_folder_path):
            shutil.rmtree(mods_folder_path)
        if os.path.exists(settings_ini_path):
            os.remove(settings_ini_path)

        self.infoLabel.setText('Applying mods...')
        self.apply_mods(self.gameFolderPath)
        self.save_patch_data()
        self.infoLabel.setText('Process completed!')


    def copy_contents(self, src, dst):
        # Identify the correct folder to copy from
        src_folder = os.path.join(src, 'DEV-UE4SS_Xinput_v2.5.2')
        if not os.path.exists(src_folder):
            raise FileNotFoundError(f"Expected folder not found in the zip: {src_folder}")

        for item in os.listdir(src_folder):
            s = os.path.join(src_folder, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
                if not item.lower().endswith('.zip'):  # Don't add ZIP files to addedFiles
                    self.addedFiles.append(os.path.relpath(d, dst))


    def download_file(self, url, path):
        response = requests.get(url)
        with open(path, 'wb') as file:
            file.write(response.content)

    def unzip_file(self, zip_path, extract_to, exclude_from_added_files=False):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            if not exclude_from_added_files:
                self.addedFiles.extend(zip_ref.namelist())

    def apply_mods(self, target_folder):
        mods_zip_path = 'Patch.zip'  #Patch file
        self.unzip_file(mods_zip_path, target_folder, exclude_from_added_files=True)


    def unpatch_game(self):
        self.handle_errors(self._unpatch_game)

    def _unpatch_game(self):
        patch_data = self.load_patch_data()
        if patch_data:
            folder_path = patch_data['folder_path']
            for file in patch_data['added_files']:
                try:
                    file_path = os.path.join(folder_path, file)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    self.infoLabel.setText(f'Error deleting file {file_path}: {e}')
                    return
            self.infoLabel.setText('All patched files have been removed.')
        else:
            self.infoLabel.setText('No patch data found.')



    def save_patch_data(self):
        patch_data = {
            'folder_path': self.gameFolderPath,
            'added_files': self.addedFiles
        }
        with open('patch_data.json', 'w') as file:
            json.dump(patch_data, file)

    def load_patch_data(self):
        try:
            with open('patch_data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Downloader()
    sys.exit(app.exec_())
