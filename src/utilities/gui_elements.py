from PyQt5.QtWidgets import QWidget, QVBoxLayout,QSizePolicy, QComboBox, QDateEdit, QLabel, QLineEdit, QRadioButton, QGroupBox, QPushButton, QFileDialog, QFrame, QButtonGroup, QMainWindow, QApplication, QTextEdit, QListWidget, QListWidgetItem, QCheckBox, QMessageBox, QProgressDialog, QProgressBar, QHBoxLayout
from PyQt5.QtWidgets import QStackedWidget, QDialog, QTableWidget, QTableWidgetItem, QHeaderView,QInputDialog
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QDate
import sys
import os
import pandas as pd
import webbrowser
import subprocess
import shutil
import etapa1
import etapa2
import etapa3
import etapa4
import etapa5
import etapa6
import etapa7
import etapa8
import etapa9
import etapa10



class BaseWindow(QWidget):
    def __init__(self, title=""):
        super().__init__()

        # Establecer fondo blanco
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 2300, 800)  # Aumentar la altura de la ventana

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignTop)

        # Layout para la imagen y el encabezado
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        # Imagen pequeña en la parte superior izquierda
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), '../../resources/Logo.jfif'))
        logo_label.setPixmap(logo_pixmap)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(120, 80)  # Tamaño arbitrario para la imagen pequeña

        # Encabezado
        header_title = QLabel("IntegrityAI - Creación de Nuevo Proyecto", self)
        header_title.setStyleSheet("font-size: 18px; font-weight: bold; color: green; background-color: white;")
        header_title.setAlignment(Qt.AlignRight)

        header_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        header_layout.addWidget(header_title, alignment=Qt.AlignBottom)

        main_layout.addLayout(header_layout)

        # Línea verde de separación
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: green;")
        separator.setFixedHeight(2)
        main_layout.addWidget(separator)

        # Módulo superior
        top_module = QVBoxLayout()
        top_module.setSpacing(10)

        project_name_layout = QHBoxLayout()
        project_name_layout.setSpacing(10)

        project_name_label = QLabel("Nombre del Proyecto:")
        project_name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
        self.project_name_entry = QLineEdit()
        self.project_name_entry.setMaximumSize(400, 20)
        self.generate_project_button = QPushButton("Generar Proyecto")
        self.generate_project_button.setMaximumSize(300, 20)
        self.generate_project_button.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        self.generate_project_button.clicked.connect(self.on_generate_project)

        project_name_layout.addWidget(project_name_label)
        project_name_layout.addWidget(self.project_name_entry)
        project_name_layout.addWidget(self.generate_project_button)
        project_name_layout.addStretch()  # Añadir estiramiento para empujar los widgets hacia la izquierda

        # Código del botón "INICIO"
        self.return_button = QPushButton("INICIO")
        self.return_button.setMaximumSize(400, 30)  # Ajustar el tamaño según sea necesario
        self.return_button.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        self.return_button.clicked.connect(self.return_to_main_menu)
        
        project_name_layout.addWidget(self.return_button, alignment=Qt.AlignRight)  # Alinear el botón a la derecha
        top_module.addLayout(project_name_layout)

        main_layout.addLayout(top_module)

        self.setLayout(main_layout)

    def return_to_main_menu(self):
        self.close()
        main_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../classes/main_app.py'))
        subprocess.run([sys.executable, main_app_path])

class NewProjectWindow(BaseWindow):
    def __init__(self):
        super().__init__("Generación de Nuevo Proyecto")

        # Añadir los widgets específicos de esta ventana
        self.initUI()

    def initUI(self):
        main_layout = self.layout()

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Inicialización de cota_inferior y cota_superior
        self.cota_inferior_date = QDateEdit(self)
        self.cota_inferior_date.setCalendarPopup(True)
        self.cota_inferior_date.setDate(QDate.currentDate())

        self.cota_superior_date = QDateEdit(self)
        self.cota_superior_date.setCalendarPopup(True)
        self.cota_superior_date.setDate(QDate.currentDate())

        # Módulo izquierdo
        left_module = QVBoxLayout()
        left_module_container = QFrame()
        left_module_container.setLayout(left_module)
        left_module_container.setStyleSheet("background-color: white; border: 1px solid green; padding: 10px;")
        left_module_container.setFixedWidth(int(self.width() * 0.25))  # Convertir a entero

        # Título para el módulo izquierdo
        left_title = QLabel("Seleccionar Datos Objetivo")
        left_title.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
        left_title.setAlignment(Qt.AlignCenter)
        left_module.addWidget(left_title)

        # Estilo común para las secciones del módulo izquierdo
        section_style = "background-color: #e0f7e0; font-size: 14px;"
        bold_font = QFont()
        bold_font.setBold(True)

        # Sección "Tipo de Proyecto"
        tipo_proyecto_group = QGroupBox("Tipo de Proyecto")
        tipo_proyecto_group.setFont(bold_font)
        tipo_proyecto_group.setStyleSheet(section_style)
        tipo_proyecto_layout = QVBoxLayout()
        tipo_proyecto_buttons_layout = QHBoxLayout()
        self.tipo_proyecto_button_group = QButtonGroup(self)
        self.forensic_radio = QRadioButton("Forensic")
        self.forensic_radio.setStyleSheet("font-size: 10px; background-color: green; color: white;")
        self.secopii_radio = QRadioButton("SECOPII")
        self.secopii_radio.setStyleSheet("font-size: 10px; background-color: green; color: white;")
        self.tipo_proyecto_button_group.addButton(self.forensic_radio)
        self.tipo_proyecto_button_group.addButton(self.secopii_radio)
        self.forensic_radio.toggled.connect(self.on_tipo_proyecto_changed)
        self.secopii_radio.toggled.connect(self.on_tipo_proyecto_changed)
        tipo_proyecto_buttons_layout.addWidget(self.forensic_radio)
        tipo_proyecto_buttons_layout.addWidget(self.secopii_radio)
        tipo_proyecto_layout.addLayout(tipo_proyecto_buttons_layout)

        tipo_proyecto_group.setLayout(tipo_proyecto_layout)

        left_module.addWidget(tipo_proyecto_group)

        # Sección adicional para "SECOPII"
        self.secopii_options_group = QGroupBox("Opciones SECOPII")
        self.secopii_options_group.setFont(bold_font)
        self.secopii_options_group.setStyleSheet(section_style)
        self.secopii_options_group.setVisible(False)  # Inicialmente oculto
        secopii_options_layout = QVBoxLayout()

        # Departamento
        departamento_label = QLabel("Departamento:")
        departamento_label.setStyleSheet("font-size: 12px; color: green;")
        self.departamento_combo = QComboBox()
        departamentos = ['Colombia','Amazonas', 'Antioquia', 'Arauca', 'Atlántico', 'Bolívar', 'Boyacá', 'Caldas', 'Caquetá', 'Casanare', 'Cauca', 'Cesar', 'Chocó', 'Cundinamarca', 'Córdoba', 'Distrito Capital de Bogotá', 'Guainía', 'Huila', 'La Guajira', 'Magdalena', 'Meta', 'Nariño', 'No Definido', 'Norte de Santander', 'Putumayo', 'Quindío', 'Risaralda', 'San Andrés, Providencia y Santa Catalina', 'Santander', 'Sucre', 'Tolima', 'Valle del Cauca', 'Vaupés', 'Vichada']
        self.departamento_combo.addItems(departamentos)

        # Código de Identificación
        codigo_identificacion_label = QLabel("Código de Identificación:")
        codigo_identificacion_label.setStyleSheet("font-size: 12px; color: green;")
        self.codigo_identificacion_entry = QLineEdit()

        # Cota Inferior y Cota Superior en un solo layout
        fechas_layout = QHBoxLayout()

        cota_inferior_label = QLabel("Cota Inferior:")
        cota_inferior_label.setStyleSheet("font-size: 12px; color: green;")
        fechas_layout.addWidget(cota_inferior_label)
        fechas_layout.addWidget(self.cota_inferior_date)

        cota_superior_label = QLabel("Cota Superior:")
        cota_superior_label.setStyleSheet("font-size: 12px; color: green;")
        fechas_layout.addWidget(cota_superior_label)
        fechas_layout.addWidget(self.cota_superior_date)

        # Añadir los widgets al layout vertical
        secopii_options_layout.addWidget(departamento_label)
        secopii_options_layout.addWidget(self.departamento_combo)
        secopii_options_layout.addWidget(codigo_identificacion_label)
        secopii_options_layout.addWidget(self.codigo_identificacion_entry)
        secopii_options_layout.addLayout(fechas_layout)

        self.secopii_options_group.setLayout(secopii_options_layout)
        left_module.addWidget(self.secopii_options_group)
        # Sección "Identificación del Tercero"
        identificacion_group = QGroupBox("Identificación del Tercero")
        identificacion_group.setFont(bold_font)
        identificacion_group.setStyleSheet(section_style)
        identificacion_layout = QVBoxLayout()
        identificacion_buttons_layout = QHBoxLayout()
        self.natural_radio = QRadioButton("Natural")
        self.natural_radio.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        self.juridica_radio = QRadioButton("Jurídica")
        self.juridica_radio.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        self.general_radio = QRadioButton("General")
        self.general_radio.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        identificacion_buttons_layout.addWidget(self.natural_radio)
        identificacion_buttons_layout.addWidget(self.juridica_radio)
        identificacion_buttons_layout.addWidget(self.general_radio)
        self.natural_radio.toggled.connect(self.on_identificacion_changed)
        self.juridica_radio.toggled.connect(self.on_identificacion_changed)
        self.general_radio.toggled.connect(self.on_identificacion_changed)
        identificacion_layout.addLayout(identificacion_buttons_layout)
        self.nombre_entry = QLineEdit()
        self.cc_nit_entry = QLineEdit()
        self.nombre_entry.setVisible(False)
        self.cc_nit_entry.setVisible(False)
        identificacion_layout.addWidget(self.nombre_entry)
        identificacion_layout.addWidget(self.cc_nit_entry)

        # Añadir el nuevo checkbox para "Realizar Búsqueda WEB"
        self.search_web_checkbox = QCheckBox("Realizar Búsqueda WEB")
        self.search_web_checkbox.setStyleSheet("font-size: 12px; color: black;")
        self.search_web_checkbox.setVisible(False)  # Inicialmente oculto
        identificacion_layout.addWidget(self.search_web_checkbox)

        identificacion_group.setLayout(identificacion_layout)
        left_module.addWidget(identificacion_group)

        # Sección "Información a Validar"
        info_validar_group = QGroupBox("Información a Validar")
        info_validar_group.setFont(bold_font)
        info_validar_group.setStyleSheet(section_style)
        info_validar_layout = QVBoxLayout()
        info_validar_buttons_layout = QHBoxLayout()
        self.select_file_button = QPushButton("Seleccionar Archivo")
        self.select_file_button.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        self.select_file_button.clicked.connect(self.select_file)
        self.select_folder_button = QPushButton("Seleccionar Carpeta")
        self.select_folder_button.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        self.select_folder_button.clicked.connect(self.select_folder)
        info_validar_buttons_layout.addWidget(self.select_file_button)
        info_validar_buttons_layout.addWidget(self.select_folder_button)
        info_validar_layout.addLayout(info_validar_buttons_layout)

        self.select_url_button = QPushButton("Ingresar URL")
        self.select_url_button.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        self.select_url_button.clicked.connect(self.select_url)
        info_validar_layout.addWidget(self.select_url_button)

        self.file_label = QLabel()
        self.file_label.setVisible(False)
        self.folder_label = QLabel()
        self.folder_label.setVisible(False)
        self.web_entry = QLineEdit()
        self.web_entry.setPlaceholderText("Ingrese la URL")
        self.web_entry.setVisible(False)

        info_validar_layout.addWidget(self.file_label)
        info_validar_layout.addWidget(self.folder_label)
        info_validar_layout.addWidget(self.web_entry)
        info_validar_group.setLayout(info_validar_layout)

        left_module.addWidget(info_validar_group)

        # Sección "Enfoque Forense"
        enfoque_forense_group = QGroupBox("Enfoque Forense")
        enfoque_forense_group.setFont(bold_font)
        enfoque_forense_group.setStyleSheet(section_style)
        enfoque_forense_layout = QVBoxLayout()
        self.enfoque_text_edit = QTextEdit()
        self.enfoque_text_edit.setPlaceholderText("Ingresar el detalle del enfoque, pruebas o validaciones que considere importantes realizar dentro de la base de datos.")
        enfoque_forense_layout.addWidget(self.enfoque_text_edit)
        enfoque_forense_group.setLayout(enfoque_forense_layout)

        left_module.addWidget(enfoque_forense_group)

        content_layout.addWidget(left_module_container)

        # Ruta relativa del archivo de Excel
        excel_path = os.path.join(os.path.dirname(__file__), '../../resources/inputs_opc/Banderas Rojas.xlsx')

        # Leer el archivo de Excel
        data = pd.read_excel(excel_path, header=None)

        # Obtener las opciones de la columna A y eliminar duplicados
        banderas_rojas_options = list(set(data.iloc[:, 0].tolist()))

        # Ruta relativa del archivo de Excel para subscripción
        subscripcion_excel_path = os.path.join(os.path.dirname(__file__), '../../resources/inputs_opc/ConPago.xlsx')

        # Leer el archivo de Excel para subscripción
        subscripcion_data = pd.read_excel(subscripcion_excel_path, header=None)

        # Obtener las opciones de la columna A para subscripción
        subscripcion_options = subscripcion_data.iloc[:, 0].tolist()

        # Ruta relativa del archivo de Excel para "Datos con Restricciones de Consulta"
        registro_excel_path = os.path.join(os.path.dirname(__file__), '../../resources/inputs_opc/Registro.xlsx')

        # Leer el archivo de Excel para "Datos con Restricciones de Consulta"
        registro_data = pd.read_excel(registro_excel_path, header=None)

        # Obtener las opciones de la columna A, las URLs de la columna B y los tipos de la columna C
        self.registro_options = registro_data.iloc[:, 0].tolist()
        self.registro_urls = registro_data.iloc[:, 1].tolist()
        self.registro_tipos = registro_data.iloc[:, 2].tolist()
        # Módulo derecho
        right_module = QVBoxLayout()
        right_module_container = QFrame()
        right_module_container.setLayout(right_module)
        right_module_container.setStyleSheet("background-color: white; border: 1px solid green; padding: 10px;")
        right_module_container.setFixedWidth(int(self.width() * 0.55))  # Convertir a entero

        # Título para el módulo derecho
        right_title = QLabel("Fuentes Externas Estándar")
        right_title.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
        right_title.setAlignment(Qt.AlignCenter)
        right_title.setFixedHeight(39)
        right_module.addWidget(right_title)

        # Layout para contener las secciones de Libre Consulta y Opcionales
        right_sections_layout = QHBoxLayout()  # Cambiado a QHBoxLayout para colocarlas al lado
        right_sections_layout.setSpacing(10)

        # Sección "Libre Consulta"
        libre_consulta_group = QGroupBox("Libre Consulta")
        libre_consulta_group.setFont(bold_font)
        libre_consulta_group.setStyleSheet("background-color: white; font-size: 14px;")
        libre_consulta_layout = QVBoxLayout()

        # Sección "Datos Libres"
        datos_libres_group = QGroupBox("Datos Libres")
        datos_libres_group.setStyleSheet(section_style)
        datos_libres_layout = QVBoxLayout()
        datos_libres_label = QLabel("Información de Bases de Datos Libres")
        datos_libres_label.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        datos_libres_layout.addWidget(datos_libres_label)

        # Leer el archivo de Excel para "Datos Libres"
        database_excel_path = os.path.join(os.path.dirname(__file__), '../../resources/inputs_opc/DataBase.xlsx')
        database_data = pd.read_excel(database_excel_path, header=None)

        # Obtener las opciones de la columna A y eliminar duplicados
        datos_libres_options = list(set(database_data.iloc[:, 0].tolist()))
        datos_libres_options.sort(reverse=True)

        # Crear una lista de opciones seleccionables para "Datos Libres"
        self.datos_libres_list = QListWidget()
        self.datos_libres_list.setSelectionMode(QListWidget.MultiSelection)

        for option in datos_libres_options:
            item = QListWidgetItem(option)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.datos_libres_list.addItem(item)

        datos_libres_layout.addWidget(self.datos_libres_list)
        datos_libres_group.setLayout(datos_libres_layout)
        libre_consulta_layout.addWidget(datos_libres_group)

        libre_consulta_group.setLayout(libre_consulta_layout)

        # Sección "Registro (Descarga Manual)"
        registro_group = QGroupBox("Datos con Restricciones de Consulta")
        registro_group.setFont(bold_font)
        registro_group.setStyleSheet("background-color: #f0fff0; font-size: 14px;")  # Color verde claro
        registro_layout = QVBoxLayout()

        # Layout horizontal para los botones de filtro
        filter_buttons_layout = QHBoxLayout()
        self.filter_natural_button = QPushButton("Plataformas Personas Naturales")
        self.filter_natural_button.setStyleSheet("font-size: 12px; background-color: #77DD77; color: black;")
        self.filter_natural_button.clicked.connect(self.filter_natural_options)

        self.filter_others_button = QPushButton("Plataformas Objetivo General")
        self.filter_others_button.setStyleSheet("font-size: 12px; background-color: #77DD77; color: black;")
        self.filter_others_button.clicked.connect(self.filter_other_options)

        filter_buttons_layout.addWidget(self.filter_natural_button)
        filter_buttons_layout.addWidget(self.filter_others_button)

        registro_layout.addLayout(filter_buttons_layout)

        # Crear una lista de opciones seleccionables que abren URLs
        self.registro_list = QListWidget()
        self.registro_list.itemClicked.connect(self.on_registro_item_clicked)

        registro_label = QLabel("Requiere Realizar Descarga Manual")
        registro_label.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        registro_layout.addWidget(registro_label)
        registro_layout.addWidget(self.registro_list)
        registro_group.setLayout(registro_layout)
        libre_consulta_layout.addWidget(registro_group)

        libre_consulta_group.setLayout(libre_consulta_layout)
        # Sección "Opcionales"
        opcionales_group = QGroupBox("Especializados")
        opcionales_group.setFont(bold_font)
        opcionales_group.setStyleSheet("background-color: white; font-size: 14px;")
        opcionales_layout = QVBoxLayout()

        # Sección "Subscripción de Pago"
        subscripcion_group = QGroupBox("Suscripción de Pago")
        subscripcion_group.setFont(bold_font)
        subscripcion_group.setStyleSheet("background-color: #e0f7e0; border: 1px solid green; padding: 11px; font-size: 14px;")
        subscripcion_layout = QVBoxLayout()

        # Crear una lista de opciones seleccionables con solicitud de usuario y contraseña
        self.subscripcion_list = QListWidget()
        self.subscripcion_list.setSelectionMode(QListWidget.MultiSelection)

        subscripcion_options.sort(reverse=True)

        for option in subscripcion_options:
            item = QListWidgetItem(option)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, option)  # Guardar la opción en los datos del ítem
            self.subscripcion_list.addItem(item)

        self.subscripcion_list.itemChanged.connect(self.on_subscripcion_item_changed)

        subscripcion_label = QLabel("Datos de Suscripción")
        subscripcion_label.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        subscripcion_layout.addWidget(subscripcion_label)
        subscripcion_layout.addWidget(self.subscripcion_list)
        subscripcion_group.setLayout(subscripcion_layout)

        # Ajustar tamaño de la sección de "Subscripción de Pago" según su contenido
        subscripcion_group.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Sección "Banderas Rojas"
        banderas_rojas_group = QGroupBox("Banderas Rojas")
        banderas_rojas_group.setFont(bold_font)
        banderas_rojas_group.setStyleSheet("background-color: #e0f7e0; border: 1px solid green; padding: 11px; font-size: 14px;")
        banderas_rojas_layout = QVBoxLayout()

        # Crear una lista de opciones seleccionables
        self.banderas_rojas_list = QListWidget()
        self.banderas_rojas_list.setSelectionMode(QListWidget.MultiSelection)

        banderas_rojas_options.sort(reverse=True)

        for option in banderas_rojas_options:
            item = QListWidgetItem(option)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.banderas_rojas_list.addItem(item)

        banderas_rojas_label = QLabel("Fuentes de Indicadores de Banderas Rojas")
        banderas_rojas_label.setStyleSheet("font-size: 12px; background-color: green; color: white;")
        banderas_rojas_layout.addWidget(banderas_rojas_label)
        banderas_rojas_layout.addWidget(self.banderas_rojas_list)
        banderas_rojas_group.setLayout(banderas_rojas_layout)

        # Ajustar tamaño de la sección de "Banderas Rojas" según su contenido
        banderas_rojas_group.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        opcionales_layout.addWidget(subscripcion_group)
        opcionales_layout.addWidget(banderas_rojas_group)
        opcionales_group.setLayout(opcionales_layout)

        # Añadir las secciones al layout derecho
        right_sections_layout.addWidget(libre_consulta_group, stretch=7)
        right_sections_layout.addWidget(registro_group, stretch=3)
        right_sections_layout.addWidget(opcionales_group, stretch=3)

        right_module.addLayout(right_sections_layout)
        content_layout.addWidget(right_module_container)
        main_layout.addLayout(content_layout)

    def filter_natural_options(self):
        self.registro_list.clear()
        for option, url, tipo in zip(self.registro_options, self.registro_urls, self.registro_tipos):
            if tipo == "Persona":
                item = QListWidgetItem(option)
                item.setData(Qt.UserRole, url)
                self.registro_list.addItem(item)

    def filter_other_options(self):
        self.registro_list.clear()
        for option, url, tipo in zip(self.registro_options, self.registro_urls, self.registro_tipos):
            if tipo != "Persona":
                item = QListWidgetItem(option)
                item.setData(Qt.UserRole, url)
                self.registro_list.addItem(item)

    # Método para manejar el evento de clic en los ítems de "Datos con Restricciones de Consulta"
    def on_registro_item_clicked(self, item):
        url = item.data(Qt.UserRole)
        webbrowser.open(url)

    # Método para manejar el evento de cambio en los ítems de subscripción
    def on_subscripcion_item_changed(self, item):
        if item.checkState() == Qt.Checked:
            # Mostrar un cuadro de diálogo para solicitar usuario y contraseña
            usuario, ok1 = QInputDialog.getText(self, "Usuario", f"Ingrese el Usuario para {item.data(Qt.UserRole)}:")
            if ok1:
                contraseña, ok2 = QInputDialog.getText(self, "Contraseña", f"Ingrese la Contraseña para {item.data(Qt.UserRole)}:", QLineEdit.Password)
                if not ok2:  # Aquí está la corrección
                    # Si la contraseña no se ingresa, desmarcar el ítem
                    item.setCheckState(Qt.Unchecked)
            else:
                # Si el usuario no se ingresa, desmarcar el ítem
                item.setCheckState(Qt.Unchecked)
    def on_tipo_proyecto_changed(self):
        if self.secopii_radio.isChecked():
            self.secopii_options_group.setVisible(True)  # Mostrar opciones adicionales
        else:
            self.secopii_options_group.setVisible(False)  # Ocultar opciones adicionales

    def on_identificacion_changed(self):
        if self.juridica_radio.isChecked() or self.natural_radio.isChecked():
            self.nombre_entry.setVisible(True)
            self.cc_nit_entry.setVisible(True)
            self.search_web_checkbox.setVisible(True)
            if self.juridica_radio.isChecked():
                self.nombre_entry.setPlaceholderText("Razón Social")
                self.cc_nit_entry.setPlaceholderText("NIT")
            elif self.natural_radio.isChecked():
                self.nombre_entry.setPlaceholderText("Ingrese el Nombre")
                self.cc_nit_entry.setPlaceholderText("Cédula de Ciudadanía")
        else:
            self.nombre_entry.setVisible(False)
            self.cc_nit_entry.setVisible(False)
            self.search_web_checkbox.setVisible(False)

    def select_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar un Archivo Específico", "", "Todos los Archivos (*);;Archivos de Texto (*.txt);;Archivos CSV (*.csv)", options=options)
        if file:
            self.file_label.setText(f"{file}")
            self.file_label.setVisible(True)
            self.folder_label.setVisible(False)
            self.web_entry.setVisible(False)

    def select_folder(self):
        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", "", options=options)
        if folder:
            self.folder_label.setText(f"{folder}")
            self.folder_label.setVisible(True)
            self.file_label.setVisible(False)
            self.web_entry.setVisible(False)

    def select_url(self):
        self.web_entry.setVisible(True)
        self.file_label.setVisible(False)
        self.folder_label.setVisible(False)

    def on_generate_project(self):
        project_name = self.project_name_entry.text().strip()
        if not project_name:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese un nombre para el proyecto.")
            return
    
        project_dir = os.path.join(os.path.dirname(__file__), '../../projects', project_name)
    
        if os.path.exists(project_dir):
            QMessageBox.warning(self, "Advertencia", "El proyecto ya existe.")
            return
    
        try:
            # Inicializar la barra de progreso
            progress_dialog = QProgressDialog("Generando Proyecto", "Cancelar", 0, 100, self)
            progress_dialog.setWindowTitle("Por favor espere")
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setAutoClose(True)
            progress_dialog.show()
    
            # Inicializar progreso
            current_progress = 0
            progress_dialog.setValue(current_progress)
    
            # Clonar el directorio de la plantilla
            template_dir = os.path.join(os.path.dirname(__file__), '../../template/NewProyect')
            shutil.copytree(template_dir, project_dir)
            current_progress += 5
            progress_dialog.setValue(current_progress)
    
            # Recopilación de datos de entrada
            input_data = {
                "Tipo de Proyecto - Forensic": self.forensic_radio.isChecked(),
                "Tipo de Proyecto - SECOPII": self.secopii_radio.isChecked(),
                "Departamento": self.departamento_combo.currentText() if self.secopii_radio.isChecked() else "",
                "Código de Identificación": self.codigo_identificacion_entry.text() if self.secopii_radio.isChecked() else "",
                "Cota Inferior": self.cota_inferior_date.text() if self.secopii_radio.isChecked() else "",
                "Cota Superior": self.cota_superior_date.text() if self.secopii_radio.isChecked() else "",
                "Identificación del Tercero - Natural": self.natural_radio.isChecked(),
                "Identificación del Tercero - Jurídica": self.juridica_radio.isChecked(),
                "Identificación del Tercero - General": self.general_radio.isChecked(),
                "Nombre o Razón Social": self.nombre_entry.text() if (self.juridica_radio.isChecked() or self.natural_radio.isChecked()) else "",
                "Cédula o NIT": self.cc_nit_entry.text() if (self.juridica_radio.isChecked() or self.natural_radio.isChecked()) else "",
                "Realizar Búsqueda WEB": self.search_web_checkbox.isChecked(),
                "Archivo Seleccionado": self.file_label.text() if self.file_label.isVisible() else "",
                "Carpeta Seleccionada": self.folder_label.text() if self.folder_label.isVisible() else "",
                "URL Ingresada": self.web_entry.text() if self.web_entry.isVisible() else "",
                "Enfoque Forense": self.enfoque_text_edit.toPlainText()
            }
    

            # Agregar datos libres
            for i in range(self.datos_libres_list.count()):
                item = self.datos_libres_list.item(i)
                input_data[f"Datos Libres - {item.text()}"] = item.checkState() == Qt.Checked
    
            # Agregar banderas rojas
            for i in range(self.banderas_rojas_list.count()):
                item = self.banderas_rojas_list.item(i)
                input_data[f"Banderas Rojas - {item.text()}"] = item.checkState() == Qt.Checked
    
            # Crear DataFrame y guardar en un archivo Excel
            df = pd.DataFrame([input_data])
            df.to_excel(os.path.join(project_dir, 'inputs.xlsx'), index=False)
            current_progress += 5
            progress_dialog.setValue(current_progress)
    
            # Ejecutar etapa1.py después de crear el proyecto
            if self.secopii_radio.isChecked():
       
                
                # Definir los parámetros a pasar
                output_path = os.path.join(project_dir, "DataSet", "temp")
                os.makedirs(output_path, exist_ok=True)  # Crear directorio si no existe
                
                departamento = self.departamento_combo.currentText()
                if departamento == "Colombia":
                    departamento = None  # No enviar como parámetro si es "Colombia"
                
                documento_proveedor = self.codigo_identificacion_entry.text()
                if not documento_proveedor:
                    documento_proveedor = None  # Ignorar si está vacío
                
                fecha_desde = self.cota_inferior_date.date().toString("yyyy-MM-dd")
                fecha_hasta = self.cota_superior_date.date().toString("yyyy-MM-dd")
                
                # Llamada a la función descargar_secop con los parámetros correctos
                descargar_secop(output_path, documento_proveedor=documento_proveedor, departamento=departamento, desde=fecha_desde, hasta=fecha_hasta)
                
                current_progress += 15
                progress_dialog.setValue(current_progress)
    
            # Ejecutar etapa2.py si "Realizar Búsqueda WEB" está marcado
            if self.search_web_checkbox.isChecked():
                target_name = self.nombre_entry.text()
                search_save_path = os.path.join(project_dir, 'DataSet', 'temp', 'URL')
                result = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'etapa2.py'), target_name, search_save_path], capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"etapa2.py failed: {result.stderr}")
            current_progress += 15
            progress_dialog.setValue(current_progress)
    
            # Ejecutar etapa3.py para procesar archivo seleccionado
            file_selected = self.file_label.text() if self.file_label.isVisible() else ""
            if file_selected:
                result = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'etapa3.py'), project_dir, file_selected], capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"etapa3.py failed: {result.stderr}")
            current_progress += 15
            progress_dialog.setValue(current_progress)
    
            # Ejecutar etapa4.py para procesar carpeta seleccionada
            folder_selected = self.folder_label.text() if self.folder_label.isVisible() else ""
            if folder_selected:
                result = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'etapa4.py'), project_dir, folder_selected], capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"etapa4.py failed: {result.stderr}")
            current_progress += 15
            progress_dialog.setValue(current_progress)
    
            # Ejecutar etapa5.py para descargar la URL ingresada
            url_ingresada = self.web_entry.text() if self.web_entry.isVisible() else ""
            if url_ingresada:
                result = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'etapa5.py'), project_dir, url_ingresada], capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"etapa5.py failed: {result.stderr}")
            current_progress += 15
            progress_dialog.setValue(current_progress)
    
            # Ejecutar etapa6.py para copiar archivos de entrenamiento según los datos libres seleccionados
            excel_path = os.path.join(os.path.dirname(__file__), '../../resources/inputs_opc/DataBase.xlsx')
            result = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'etapa6.py'), project_dir, str(input_data), excel_path], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"etapa6.py failed: {result.stderr}")
            current_progress += 15
            progress_dialog.setValue(current_progress)
    
            # Ejecutar etapa7.py para copiar archivos de entrenamiento según las banderas rojas seleccionadas
            excel_path = os.path.join(os.path.dirname(__file__), '../../resources/inputs_opc/Banderas Rojas.xlsx')
            result = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'etapa7.py'), project_dir, str(input_data), excel_path], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"etapa7.py failed: {result.stderr}")
            current_progress += 15
            progress_dialog.setValue(current_progress)
    
            # Ejecutar etapa8.py para realizar la búsqueda de la API RedFlagEU si hay un nombre o razón social ingresado
            nombre_razon_social = self.nombre_entry.text() if (self.juridica_radio.isChecked() or self.natural_radio.isChecked()) else ""
            if nombre_razon_social:
                result = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'etapa8.py'), project_dir, nombre_razon_social], capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"etapa8.py failed: {result.stderr}")
            current_progress += 15
            progress_dialog.setValue(current_progress)
    
            # Ejecutar etapa9.py para normalizar archivos en la carpeta temp
            result = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'etapa9.py'), project_dir], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"etapa9.py failed: {result.stderr}")
            current_progress += 10
            progress_dialog.setValue(current_progress)
  
            # Ejecutar la etapa 10
            import etapa10
            etapa10.execute(project_name, self.secopii_radio.isChecked())    
  
            # Finalizar la barra de progreso
            progress_dialog.setValue(100)
            progress_dialog.close()
            QMessageBox.information(self, "Éxito", "El proyecto ha sido creado y todas las etapas se han ejecutado correctamente.")
    
        except Exception as e:
            progress_dialog.close()
            QMessageBox.critical(self, "Error", f"Error al crear el proyecto: {str(e)}")
    
    def return_to_main_menu(self):
        self.close()
        main_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../classes/main_app.py'))
        subprocess.run([sys.executable, main_app_path])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewProjectWindow()
    window.show()
    sys.exit(app.exec_())
