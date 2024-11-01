import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import subprocess

class ProjectExplorer(QWidget):
    def __init__(self, base_path):
        super().__init__()

        self.base_path = base_path
        self.setWindowTitle("Explorador de Proyectos")
        self.setGeometry(100, 100, 1000, 800)  # Ajuste del tamaño de la ventana
        self.setStyleSheet("background-color: white;")  # Establecer fondo blanco

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Layout para la imagen y el encabezado
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        # Imagen pequeña en la parte superior izquierda
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), '../../resources/Logo.jfif'))
        logo_label.setPixmap(logo_pixmap)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(120, 80)  # Tamaño ajustado de la imagen pequeña

        # Encabezado
        header_title = QLabel("Explorador de Proyectos", self)
        header_title.setStyleSheet("font-size: 18px; font-weight: bold; color: green; background-color: white;")
        header_title.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        header_layout.addWidget(header_title, alignment=Qt.AlignVCenter)

        main_layout.addLayout(header_layout)

        # Línea verde de separación
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: green;")
        separator.setFixedHeight(2)
        main_layout.addWidget(separator)

        # Crear la tabla
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Nombre de Carpeta", "Acción"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        # Llenar la tabla con las carpetas
        self.load_folders()

        self.setLayout(main_layout)

    def load_folders(self):
        if os.path.exists(self.base_path):
            folders = [f for f in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, f))]
            self.table.setRowCount(len(folders))

            for i, folder_name in enumerate(folders):
                folder_path = os.path.join(self.base_path, folder_name)

                # Columna de nombre de carpeta
                folder_item = QTableWidgetItem(folder_name)
                folder_item.setFlags(Qt.ItemIsEnabled)  # Deshabilitar edición
                self.table.setItem(i, 0, folder_item)

                # Columna del botón de acción
                open_button = QPushButton("Abrir")
                open_button.setStyleSheet("font-size: 12px; background-color: green; color: white;")
                open_button.clicked.connect(lambda checked, path=folder_path: self.open_folder_or_run_script(path))
                self.table.setCellWidget(i, 1, open_button)

    def open_folder_or_run_script(self, folder_path):
        dashsecop_path = os.path.join(folder_path, 'DashSecop.py')

        if os.path.exists(dashsecop_path):
            subprocess.run([sys.executable, dashsecop_path])
        else:
            os.startfile(folder_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Projects'))
    window = ProjectExplorer(base_path)
    window.show()
    sys.exit(app.exec_())
