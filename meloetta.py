import os
import subprocess
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon

class Download(QThread):
    progress_updated = pyqtSignal(int)
    download_finished = pyqtSignal()

    def __init__(self, playlist_url):
        super().__init__()
        self.playlist_url = playlist_url

    def run(self):
        self.download_playlist(self.playlist_url)
        self.download_finished.emit()

    def download_playlist(self, playlist_url):       
        # Cria uma pasta para salvar os arquivos de áudio
        output_folder = "Musics"
        os.makedirs(output_folder, exist_ok=True)

        # Utiliza o comando no cmd
        command = f"spotdl download {playlist_url} --output {output_folder}"
        subprocess.call(command, shell=True)

        print("Download Encerrado!")

class Meloetta(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meloetta")
        self.setGeometry(200, 200, 400, 120)

        self.playlist_label = QLabel("Link da Playlist:", self)
        self.playlist_label.setGeometry(20, 20, 110, 30)

        self.playlist_input = QLineEdit(self)
        self.playlist_input.setGeometry(130, 20, 250, 30)

        self.download_button = QPushButton("DOWNLOAD", self)
        self.download_button.setGeometry(20, 70, 100, 30)
        self.download_button.clicked.connect(self.start_download)
        

        self.elapsed_time_label = QLabel("Tempo decorrido: 00:00:00", self)
        self.elapsed_time_label.setGeometry(130, 70, 200, 30)

        self.download_thread = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_elapsed_time)
        self.elapsed_time = 0

        self.setStyleSheet("font-weight: bold; font-family: Calibri; letter-spacing: 1px;")

        # Cria um novo estilo para o QLabel
        label_style = """
            QLabel {
                font-size: 14px;
                color: white;
            }
        """
        self.playlist_label.setStyleSheet(label_style)
        self.elapsed_time_label.setStyleSheet(label_style)

        # Cria um novo estilo para o QPushButton
        button_style = """
            QPushButton {
                font-size: 9px;
            }
        """
        self.download_button.setStyleSheet(button_style)

        self.set_style_based_on_date()  # Aplica o estilo com base na data atual

    def set_style_based_on_date(self):
        current_date = datetime.date.today()

        autumn_start_date = datetime.date(current_date.year, 3, 20)  # Dia 20 de março
        autumn_end_date = datetime.date(current_date.year, 6, 21)  # Dia 20 de junho

        if autumn_start_date <= current_date <= autumn_end_date:
            self.apply_autumn_style()  # Aplica o estilo de outono
        else:
            self.apply_default_style()  # Aplica o estilo padrão

    def apply_default_style(self):
        # Estilo Padrão
        palette = self.palette()

        # Icon
        icon = QIcon("srcs/meloetta.ico")
        self.setWindowIcon(icon)

        # Cores do fundo
        bg_color = QColor("#121011")

        # Configuração do fundo
        palette.setColor(QPalette.Window, bg_color)
        self.setPalette(palette)

        # Configuração da caixa de texto
        self.playlist_input.setStyleSheet(f"background-color: #F2F3F7; border: 3px solid #6AA8AC;")

        # Configuração do botão
        self.download_button.setStyleSheet(f"background-color: #B7D8CD; border: 1px solid #000;")

    def apply_autumn_style(self):
        # Estilo de Outono
        palette = self.palette()

        # Icon
        icon = QIcon("srcs/pirouette.ico")
        self.setWindowIcon(icon)

        # Cores do fundo
        bg_color = QColor("#121011")

        # Configuração do fundo
        palette.setColor(QPalette.Window, bg_color)
        self.setPalette(palette)

        # Configuração da caixa de texto
        self.playlist_input.setStyleSheet(f"background-color: #EDE6E6; border: 3px solid #F18F6D;")

        # Configuração do botão
        self.download_button.setStyleSheet(f"background-color: #F18F6D; border: 1px solid #000;")

    def start_download(self):
        if not self.download_thread:
            playlist_url = self.playlist_input.text().strip()
            if playlist_url:
                self.download_thread = Download(playlist_url)
                self.download_thread.download_finished.connect(self.download_finished)
                self.elapsed_time = 0
                self.timer.start(1000)  # Atualiza o tempo a cada 1 segundo
                self.download_thread.start()

    def update_elapsed_time(self):
        self.elapsed_time += 1
        elapsed_str = self.format_time(self.elapsed_time)
        self.elapsed_time_label.setText(f"Tempo decorrido: {elapsed_str}")

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    def download_finished(self):
        self.timer.stop()
        self.download_thread = None
        QMessageBox.information(self, "Download Concluído!", "O download da playlist foi concluído.")

app = QApplication([])
Meloetta = Meloetta()
Meloetta.show()
app.exec_()
