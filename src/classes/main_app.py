# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 09:13:29 2024

@author: GJ121KC
"""

import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

class IntegrityAIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Establecer fondo blanco para toda la ventana
        self.setStyleSheet("background-color: white;")

        self.setWindowTitle("IntegrityAI - Universidad Central")
        self.setGeometry(100, 100, 1180, 700)  # Aumentar el tamaño de la ventana para mejor visualización

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.initUI()

    def initUI(self):
        # Página principal
        main_page = QWidget()
        main_layout = QVBoxLayout(main_page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Widget principal con fondo blanco
        main_widget = QWidget(main_page)
        main_widget.setStyleSheet("background-color: white;")

        # Layout para las imágenes y el título
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 20, 20, 20)
        top_layout.setSpacing(10)

        # Imagen grande a la izquierda
        large_image_label = QLabel(self)
        large_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), '../../resources/Imagen.jpg'))
        large_image_label.setPixmap(large_pixmap)
        large_image_label.setScaledContents(True)
        large_image_label.setFixedSize(700, 700)  # Ajustar el tamaño de la imagen grande

        # Imagen pequeña y título a la derecha
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignCenter)

        small_image_label = QLabel(self)
        small_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), '../../resources/Logo.jfif'))
        small_image_label.setPixmap(small_pixmap)
        small_image_label.setScaledContents(True)
        small_image_label.setFixedSize(230, 180)  # Tamaño arbitrario para la imagen pequeña

        app_title = QLabel("IntegrityAI", self)
        app_title.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
        app_title.setAlignment(Qt.AlignCenter)

        right_layout.addWidget(small_image_label, alignment=Qt.AlignCenter)
        right_layout.addWidget(app_title, alignment=Qt.AlignCenter)

        # Botones debajo del título
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(10)

        self.new_project_button = QPushButton("Nuevo Proyecto")
        self.new_project_button.clicked.connect(self.show_new_project)
        self.new_project_button.setStyleSheet("background-color: green; color: white; font-size: 16px; padding: 10px 15px;")
        self.new_project_button.setFixedWidth(400)
        button_layout.addWidget(self.new_project_button, alignment=Qt.AlignCenter)

        self.load_project_button = QPushButton("Cargar Proyecto")
        self.load_project_button.clicked.connect(self.load_project)
        self.load_project_button.setStyleSheet("background-color: green; color: white; font-size: 16px; padding: 10px 20px;")
        self.load_project_button.setFixedWidth(400)
        button_layout.addWidget(self.load_project_button, alignment=Qt.AlignCenter)

        # Botón "Actualizar Tablas Maestras"
        self.update_master_tables_button = QPushButton("Actualizar Tablas Maestras")
        self.update_master_tables_button.clicked.connect(self.update_master_tables)
        self.update_master_tables_button.setStyleSheet("background-color: #32CD32; color: white; font-size: 16px; padding: 10px 15px;")  # Verde más claro
        self.update_master_tables_button.setFixedWidth(400)
        button_layout.addWidget(self.update_master_tables_button, alignment=Qt.AlignCenter)

        right_layout.addLayout(button_layout)

        top_layout.addWidget(large_image_label)
        top_layout.addLayout(right_layout)

        main_layout.addLayout(top_layout)
        main_widget.setLayout(main_layout)

        self.stack.addWidget(main_page)

    def show_new_project(self):
        try:
            # Ejecuta el archivo gui_elements.py usando ruta relativa
            subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), '..', 'utilities', 'gui_elements.py')], check=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al abrir 'Nuevo Proyecto': {str(e)}")

    def load_project(self):
        try:
            # Ejecuta el archivo Cargar.py usando ruta relativa
            subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), '..', 'utilities', 'Cargar.py')], check=True)
            # Cierra la aplicación actual
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al cargar el proyecto: {str(e)}")

    def clear_directory(self, directory, exceptions=None):
        if exceptions is None:
            exceptions = []
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) and filename not in exceptions:
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    def update_master_tables(self):
        try:
            # Limpiar las carpetas antes de la actualización usando rutas relativas
            current_dir = os.path.dirname(os.path.abspath(__file__))
            master_dir = os.path.join(current_dir, '..', 'resources', 'Master')
            self.clear_directory(os.path.join(master_dir, 'BR'))
            self.clear_directory(os.path.join(master_dir, 'DB'), exceptions=["M07.pdf", "M08.pdf"])
            
            # Ejecutar los scripts de actualización
            utilities_dir = os.path.join(current_dir, '..', 'utilities')
            subprocess.run([sys.executable, os.path.join(utilities_dir, 'download_database_base.py')], check=True)
            subprocess.run([sys.executable, os.path.join(utilities_dir, 'download_bandera_rojas_base.py')], check=True)
            
            # Mostrar mensaje de éxito
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Tablas Maestras Actualizadas con Exito")
            msg.setWindowTitle("Actualización Completa")
            msg.exec_()
        except subprocess.CalledProcessError as e:
            print(f"Error al actualizar las tablas maestras: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error al actualizar las tablas maestras: {e}")
            msg.setWindowTitle("Error")
            msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IntegrityAIApp()
    window.show()
    sys.exit(app.exec_())
