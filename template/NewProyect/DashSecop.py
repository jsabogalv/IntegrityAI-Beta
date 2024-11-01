import numpy as np
import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QApplication, QLineEdit, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import ijson
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QComboBox, QScrollArea, QTabWidget, QListWidget, QListWidgetItem, QAbstractItemView, QSlider
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from fuzzywuzzy import fuzz

# Define the relative paths
base_path = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_path, "inputs.xlsx")
json_path = os.path.join(base_path, "DataSet", "temp", "SECOP.json")
logo_path = os.path.join(base_path, "..", "..", "resources", "Logo.jfif")


# Load JSON data using ijson for streaming reading
def load_json_with_ijson(file_path):
    items = []
    with open(file_path, 'r', encoding='utf-8') as file:
        parser = ijson.items(file, 'item')
        for item in parser:
            items.append(item)
    return items

# Preprocess the Excel data
def preprocess_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, header=None)

    # Transpose the DataFrame so that rows become columns
    df = df.T

    # Set the first row as the column headers (Parameter) and the second row as the first data row (Value)
    df.columns = ["Parámetro", "Valor"]
    
    # Remove any rows where 'Parámetro' or 'Valor' are NaN or False
    df = df.dropna()  # Remove rows with NaN values
    df = df[df['Valor'] != False]  # Remove rows where 'Valor' is False
    
    # Remove any empty rows or columns that may have been introduced by the transpose operation
    df.dropna(how='all', inplace=True)
    
    return df

# Load and preprocess the Excel data
df_excel = preprocess_excel(input_path)

# Load the JSON data
data = load_json_with_ijson(json_path)
df = pd.DataFrame(data)

# Verification of loaded records
print(f"Total de registros cargados: {len(df)}")

# Columnas de importes que necesitan corrección de formato
COLUMNAS_IMPORTE = [
    "recursos_propios_alcald_as_gobernaciones_y_resguardos_ind_genas_",
    "recursos_de_credito", "recursos_propios", "valor_del_contrato",
    "valor_de_pago_adelantado", "valor_facturado", "valor_pendiente_de_pago",
    "valor_pagado", "valor_amortizado", "valor_pendiente_de",
    "valor_pendiente_de_ejecucion"
]

# Preprocess JSON data: convert non-numeric and null values to 0 only in amount columns
def preprocesar_datos(df, columnas_importe):
    for column in columnas_importe:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
    return df

df = preprocesar_datos(df, COLUMNAS_IMPORTE)

def obtener_valores_unicos(df, campo):
    return sorted(df[campo].dropna().astype(str).unique().tolist())

# Tipos de gráficos disponibles
TIPOS_GRAFICO = ["Línea", "Barras", "Dispersión", "Área", "Histograma", "Torta", "Tabla"]

# Opciones para la pestaña "General"
X_FIELDS_GENERAL = [
    "nombre_entidad", "nit_entidad", "departamento", "ciudad", "localizaci_n",
    "orden", "sector", "rama", "entidad_centralizada", "tipodocproveedor",
    "documento_proveedor", "proveedor_adjudicado", "codigo_entidad", "codigo_proveedor",
    "proceso_de_compra", "id_contrato", "referencia_del_contrato", "codigo_de_categoria_principal",
    "estado_contrato", "tipo_de_contrato", "modalidad_de_contratacion", "justificacion_modalidad_de",
    "domicilio_representante_legal", "duraci_n_del_contrato", "tipo_de_cuenta", "n_mero_de_cuenta"
]

Y_FIELDS_GENERAL = [
    "recursos_propios_alcald_as_gobernaciones_y_resguardos_ind_genas_",
    "recursos_de_credito", "recursos_propios", "valor_del_contrato",
    "valor_de_pago_adelantado", "valor_facturado", "valor_pendiente_de_pago",
    "valor_pagado", "valor_amortizado", "valor_pendiente_de",
    "valor_pendiente_de_ejecucion"
]

# Opciones de agregación para los valores
AGG_OPTIONS = ["Total", "Promedio", "Máximo", "Mínimo"]

# Opciones de fechas para la pestaña de "Fechas"
FECHA_FIELDS = [
    "fecha_de_firma",
    "fecha_de_inicio_del_contrato",
    "fecha_de_fin_del_contrato",
    "fecha_de_inicio_de_ejecucion",
    "fecha_de_fin_de_ejecucion"
]

# Opciones de campos de texto para la pestaña de "Texto"
TEXT_FIELDS = [
    "descripcion_del_proceso",
    "documento_proveedor",
    "proveedor_adjudicado",
    "nombre_representante_legal",
    "domicilio_representante_legal",
    "identificaci_n_representante_legal",
    "objeto_del_contrato"
]

class DashProyecto(QWidget):
    def __init__(self):
        super().__init__()

        # Obtener el nombre de la carpeta actual
        current_folder_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

        # Establecer fondo blanco
        self.setStyleSheet("background-color: white;")
        
        # Establecer el título con el nombre de la carpeta
        self.setWindowTitle(f"PROYECTO SECOPII - {current_folder_name.upper()}")
        
        self.setGeometry(100, 100, 2300, 800)  # Ajuste de tamaño basado en gui_elements.py

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignTop)

        # Inicializar df_final con los datos del Excel
        self.df_final = df_excel

        # Layout para la parte superior
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        # Imagen pequeña en la parte superior izquierda
        logo_label = QLabel(self)
        logo_path = r"E:\IntegrityAI\resources\Logo.jfif"  # Usa una ruta absoluta o relativa válida
        logo_pixmap = QPixmap(logo_path)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(120, 80)  # Tamaño según gui_elements.py

        # Encabezado
        header_title = QLabel((f"PROYECTO SECOPII - {current_folder_name.upper()}"), self)

        header_title.setStyleSheet("font-size: 18px; font-weight: bold; color: green; background-color: white;")
        header_title.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        header_layout.addWidget(header_title, alignment=Qt.AlignCenter)

        main_layout.addLayout(header_layout)

        # Línea verde de separación
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: green;")
        separator.setFixedHeight(2)
        main_layout.addWidget(separator)

        # Layout para la parte inferior con 3 módulos (izquierda 20%, centro 55%, derecha 25%)
        lower_layout = QHBoxLayout()
        lower_layout.setSpacing(10)

        # Módulo izquierdo 20%
        left_module = QVBoxLayout()
        left_module.setSpacing(10)

        # Botón para reiniciar los filtros
        reset_button = QPushButton("Reiniciar Filtros", self)
        reset_button.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold;")
        reset_button.clicked.connect(self.reiniciar_filtros)
        left_module.addWidget(reset_button)

        # Sección de Filtros
        left_label = QLabel("Filtros", self)
        left_label.setStyleSheet("background-color: #b2ebf2; color: black; font-size: 12px; font-weight: bold;")
        left_label.setAlignment(Qt.AlignCenter)
        left_module.addWidget(left_label)

        # Crear un área de desplazamiento para los filtros
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignTop)
        scroll_layout.setSpacing(10)

        # Lista de campos para los filtros
        campos = [
            "nombre_entidad", "nit_entidad", "departamento", "ciudad", "localizaci_n",
            "orden", "sector", "rama", "entidad_centralizada", "tipodocproveedor",
            "documento_proveedor", "proveedor_adjudicado", "codigo_entidad", "codigo_proveedor",
            "proceso_de_compra", "id_contrato", "referencia_del_contrato", "codigo_de_categoria_principal",
            "estado_contrato", "tipo_de_contrato", "modalidad_de_contratacion", "justificacion_modalidad_de",
            "domicilio_representante_legal", "duraci_n_del_contrato", "tipo_de_cuenta", "n_mero_de_cuenta"
        ]

        self.filtros = {}

        # Crear QListWidgets para selección múltiple con barra de búsqueda y filtrado entre sí
        for campo in campos:
            filter_layout = QVBoxLayout()

            search_bar = QLineEdit(self)
            search_bar.setPlaceholderText(f"Buscar en {campo.replace('_', ' ').capitalize()}")
            search_bar.textChanged.connect(lambda text, c=campo: self.filtrar_lista(text, c))
            filter_layout.addWidget(search_bar)

            list_widget = QListWidget(self)
            list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
            valores_unicos = obtener_valores_unicos(df, campo)
            for value in valores_unicos:
                item = QListWidgetItem(value)
                list_widget.addItem(item)
            list_widget.setFixedWidth(270)  # Ajustar el tamaño de los filtros
            list_widget.itemSelectionChanged.connect(self.aplicar_filtros)
            filter_layout.addWidget(list_widget)

            scroll_layout.addWidget(QLabel(campo.replace("_", " ").capitalize()))
            scroll_layout.addLayout(filter_layout)
            self.filtros[campo] = (list_widget, search_bar)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        left_module.addWidget(scroll_area)

        left_container = QFrame()
        left_container.setLayout(left_module)
        left_container.setStyleSheet("background-color: #b2dfdb;")  # Color verde claro
        lower_layout.addWidget(left_container, 20)  # Proporción del ancho: 20%

        # Módulo central 55%
        center_module = QVBoxLayout()
        center_module.setSpacing(10)

        # Parte superior del módulo central (Gráfica con pestañas)
        self.tab_widget = QTabWidget(self)
        center_module.addWidget(self.tab_widget, 2)  # La gráfica ahora ocupa 2 partes del espacio total

        # Recuadro de resumen
        self.resumen_label = QLabel(f"Cantidad de registros: {len(df)}", self)
        self.resumen_label.setStyleSheet("background-color: #e0f7fa; color: black; font-size: 14px; font-weight: bold;")
        center_module.addWidget(self.resumen_label)

        # Crear tres pestañas con gráficos dinámicos y controles de eje
        for i, tab_name in enumerate(["General", "Fechas", "Texto"]):
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)

            # Combobox para seleccionar los ejes X e Y y el tipo de gráfica
            axes_layout = QHBoxLayout()

            if tab_name == "General":
                x_axis_combo = QComboBox(self)
                x_axis_combo.addItem("Selecciona eje X")
                x_axis_combo.addItems(X_FIELDS_GENERAL)
                y_axis_combo = QComboBox(self)
                y_axis_combo.addItem("Selecciona eje Y")
                y_axis_combo.addItems(Y_FIELDS_GENERAL)
                
                # Definir `graph_type_combo` y `agg_type_combo` para "General"
                graph_type_combo = QComboBox(self)
                graph_type_combo.addItems(TIPOS_GRAFICO)

                agg_type_combo = QComboBox(self)
                agg_type_combo.addItems(AGG_OPTIONS)
                
                # Botón para actualizar el gráfico
                update_button = QPushButton("Actualizar Visualización", self)
                update_button.clicked.connect(lambda _, idx=i, x_combo=x_axis_combo, y_combo=y_axis_combo, g_combo=graph_type_combo, a_combo=agg_type_combo: self.update_visualization(idx, x_combo, y_combo, g_combo, a_combo))

                axes_layout.addWidget(QLabel("Eje X:"))
                axes_layout.addWidget(x_axis_combo)
                axes_layout.addWidget(QLabel("Eje Y:"))
                axes_layout.addWidget(y_axis_combo)
                axes_layout.addWidget(QLabel("Tipo de Visualización:"))
                axes_layout.addWidget(graph_type_combo)
                axes_layout.addWidget(QLabel("Tipo de Agregación:"))
                axes_layout.addWidget(agg_type_combo)
                axes_layout.addWidget(update_button)

            elif tab_name == "Fechas":
                base_date_combo = QComboBox(self)
                base_date_combo.addItem("Fecha base")
                base_date_combo.addItems(FECHA_FIELDS)

                compare_date_combo = QComboBox(self)
                compare_date_combo.addItem("Fecha comparar")
                compare_date_combo.addItems(FECHA_FIELDS)

                # Botón para actualizar el gráfico
                update_button = QPushButton("Actualizar Visualización", self)
                update_button.clicked.connect(lambda _, idx=i, b_combo=base_date_combo, c_combo=compare_date_combo: self.update_date_comparison(idx, b_combo, c_combo))

                axes_layout.addWidget(QLabel("Fecha base:"))
                axes_layout.addWidget(base_date_combo)
                axes_layout.addWidget(QLabel("Fecha comparar:"))
                axes_layout.addWidget(compare_date_combo)
                axes_layout.addWidget(update_button)

            elif tab_name == "Texto":
                text_field_combo = QComboBox(self)
                text_field_combo.addItem("Campo a Validar")
                text_field_combo.addItems(TEXT_FIELDS)

                similarity_slider = QSlider(Qt.Horizontal)
                similarity_slider.setMinimum(1)
                similarity_slider.setMaximum(100)
                similarity_slider.setValue(80)  # Valor predeterminado
                similarity_slider.setTickInterval(10)
                similarity_slider.setTickPosition(QSlider.TicksBelow)

                similarity_label = QLabel(f"Similitud: {similarity_slider.value()}%")
                similarity_slider.valueChanged.connect(lambda: similarity_label.setText(f"Similitud: {similarity_slider.value()}%"))

                # Botón para realizar la búsqueda difusa
                search_button = QPushButton("Buscar Similitudes", self)
                search_button.clicked.connect(lambda _, idx=i, t_combo=text_field_combo, slider=similarity_slider: self.update_text_comparison(idx, t_combo, slider))

                axes_layout.addWidget(QLabel("Campo a Validar:"))
                axes_layout.addWidget(text_field_combo)
                axes_layout.addWidget(similarity_label)
                axes_layout.addWidget(similarity_slider)
                axes_layout.addWidget(search_button)

            tab_layout.addLayout(axes_layout)

            # Espacio para el gráfico o la tabla
            self.canvas_or_table = QWidget(self)  # Placeholder para gráfico o tabla
            tab_layout.addWidget(self.canvas_or_table)

            self.tab_widget.addTab(tab, tab_name)

        center_container = QFrame()
        center_container.setLayout(center_module)
        center_container.setStyleSheet("background-color: white;")
        lower_layout.addWidget(center_container, 55)  # Proporción del ancho: 55%

        # Módulo derecho 25%
        right_module = QVBoxLayout()
        right_module.setSpacing(10)

        right_label = QLabel("Lista de Hiperparámetros", self)
        right_label.setStyleSheet("background-color: #b2ebf2; color: black; font-size: 12px; font-weight: bold;")
        right_label.setAlignment(Qt.AlignCenter)
        right_module.addWidget(right_label)

        # Crear la tabla para "base"
        self.base_table = QTableWidget(self)
        self.base_table.setRowCount(len(self.df_final))
        self.base_table.setColumnCount(3)  # Añadimos una columna para la numeración
        self.base_table.setHorizontalHeaderLabels(["#", "Parámetro", "Valor"])
        self.base_table.horizontalHeader().setStretchLastSection(True)
        self.base_table.verticalHeader().setVisible(False)  # Ocultar encabezados de fila
        self.base_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Hacer que la tabla sea de solo lectura
        self.base_table.setStyleSheet(" color: black; font-size: 12px;")

        # Llenar la tabla con los datos del DataFrame procesado y añadir numeración
        for i in range(len(self.df_final)):
            self.base_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))  # Numeración
            self.base_table.setItem(i, 1, QTableWidgetItem(str(self.df_final.iloc[i, 0])))
            self.base_table.setItem(i, 2, QTableWidgetItem(str(self.df_final.iloc[i, 1])))

        # Ajustar el ancho de las columnas según el contenido
        self.base_table.resizeColumnsToContents()

        # Conectar la señal de selección a la función de actualización
        self.base_table.currentCellChanged.connect(self.update_text_edit)

        right_module.addWidget(self.base_table, 75)  # Ajustar para ocupar el 75% del espacio disponible

        # Cuadro de texto para mostrar el valor seleccionado
        self.nuevos_parametros_text = QTextEdit(self)
        self.nuevos_parametros_text.setReadOnly(True)
        self.nuevos_parametros_text.setStyleSheet("background-color: #00796b; color: white; font-size: 12px;")

        right_module.addWidget(self.nuevos_parametros_text, 20)  # Ajustar para ocupar el 25% del espacio disponible

        right_container = QFrame()
        right_container.setLayout(right_module)
        right_container.setStyleSheet("background-color: #b2dfdb;")  # Mismo color que el módulo izquierdo
        lower_layout.addWidget(right_container, 20)  # Proporción del ancho: 25%

        main_layout.addLayout(lower_layout)
        self.filtered_df = df  # Inicializa los datos filtrados con todos los datos


    def aplicar_filtros(self):
        # Filtra el DataFrame según los criterios seleccionados
        filtered_df = df.copy()  # Restablece los datos filtrados a todos los datos

        for campo, (list_widget, _) in self.filtros.items():
            selected_items = list_widget.selectedItems()
            if selected_items:
                selected_values = [item.text() for item in selected_items]
                filtered_df = filtered_df[filtered_df[campo].astype(str).isin(selected_values)]

        self.filtered_df = filtered_df  # Actualiza los datos filtrados

        # Actualizar el resumen de registros
        self.resumen_label.setText(f"Cantidad de registros: {len(self.filtered_df)}")

    def filtrar_lista(self, text, campo):
        # Filtra los elementos de la lista basándose en la barra de búsqueda
        list_widget, _ = self.filtros[campo]
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def reiniciar_filtros(self):
        # Restablece todos los filtros a su estado original
        self.filtered_df = df.copy()  # Restablece los datos filtrados a todos los datos
        for campo, (list_widget, search_bar) in self.filtros.items():
            list_widget.clear()
            valores_unicos = obtener_valores_unicos(df, campo)
            for value in valores_unicos:
                item = QListWidgetItem(value)
                list_widget.addItem(item)
            search_bar.clear()
        self.resumen_label.setText(f"Cantidad de registros: {len(self.filtered_df)}")

              
    def update_visualization(self, tab_index, x_axis_combo, y_axis_combo, graph_type_combo, agg_type_combo):
        # Obtener los valores seleccionados
        x_field = x_axis_combo.currentText()
        y_field = y_axis_combo.currentText()
        visualization_type = graph_type_combo.currentText()
        aggregation_type = agg_type_combo.currentText()
    
        if y_field == "Selecciona eje Y":
            print(f"Error: No se seleccionó el campo necesario para {y_field}")
            return  # No se seleccionaron los campos necesarios
    
        # Aplicar agregación
        if aggregation_type == "Total":
            grouped_data = self.filtered_df.groupby(x_field)[y_field].sum().reset_index()
        elif aggregation_type == "Promedio":
            grouped_data = self.filtered_df.groupby(x_field)[y_field].mean().reset_index()
        elif aggregation_type == "Máximo":
            grouped_data = self.filtered_df.groupby(x_field)[y_field].max().reset_index()
        elif aggregation_type == "Mínimo":
            grouped_data = self.filtered_df.groupby(x_field)[y_field].min().reset_index()
    
        # Limpiar gráficos anteriores
        for i in reversed(range(self.tab_widget.widget(tab_index).layout().count())):
            widget_to_remove = self.tab_widget.widget(tab_index).layout().itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.deleteLater()
    
        if visualization_type == "Tabla":
            self.create_pivot_table_view(tab_index, x_field, y_field, grouped_data)
        else:
            self.create_graph_view(tab_index, x_field, y_field, visualization_type, grouped_data)
    
    def update_date_comparison(self, tab_index, base_date_combo, compare_date_combo):
        base_date_field = base_date_combo.currentText()
        compare_date_field = compare_date_combo.currentText()
    
        if base_date_field == "Fecha base" or compare_date_field == "Fecha comparar":
            print("Error: No se seleccionaron los campos necesarios para la comparación de fechas")
            return
    
        # Calcular la diferencia en días
        def calculate_days_diff(row):
            # Verificar si las columnas existen en el DataFrame
            if base_date_field not in row or compare_date_field not in row:
                return 1111
    
            base_date = pd.to_datetime(row[base_date_field], errors='coerce')
            compare_date = pd.to_datetime(row[compare_date_field], errors='coerce')
    
            if pd.isna(base_date) or pd.isna(compare_date):
                return 1111
            return (compare_date - base_date).days
    
        self.filtered_df['days_diff'] = self.filtered_df.apply(calculate_days_diff, axis=1)
    
        # Agrupar por la cantidad de días y contar las ocurrencias
        grouped_data = self.filtered_df.groupby('days_diff').size().reset_index(name='count')
    
        # Limpiar gráficos anteriores
        for i in reversed(range(self.tab_widget.widget(tab_index).layout().count())):
            widget_to_remove = self.tab_widget.widget(tab_index).layout().itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.deleteLater()
    
        # Crear el gráfico de dispersión
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(grouped_data['days_diff'], grouped_data['count'], label='Días vs Cantidad')
        ax.set_xlabel("Diferencia en Días")
        ax.set_ylabel("Cantidad")
        ax.set_title(f"Diferencia de días entre {base_date_field} y {compare_date_field}")
        ax.legend()
    
        plt.close(fig)  # Cerrar el gráfico anterior para evitar múltiples gráficos
    
        # Reemplazar el gráfico anterior
        canvas = FigureCanvas(fig)
        self.tab_widget.widget(tab_index).layout().addWidget(canvas)
    
        # Mostrar la tabla de resultados
        self.create_pivot_table_view(tab_index, 'days_diff', 'count', grouped_data)
    
        self.update()  # Forzar la actualización de la interfaz
    
    
    

    def update_text_comparison(self, tab_index, text_field_combo, similarity_slider):
        text_field = text_field_combo.currentText()
        threshold = similarity_slider.value()
    
        if text_field == "Campo a Validar":
            print("Error: No se seleccionó el campo de texto a validar")
            return
    
        # Filtrar los datos que no contengan "No Definido", vacíos o en blanco
        valid_data = self.filtered_df[self.filtered_df[text_field].notna()]  # Eliminar NaN
        valid_data = valid_data[~valid_data[text_field].str.contains("No Definido", na=False)]
        valid_data = valid_data[~valid_data[text_field].str.strip().eq("")]  # Eliminar valores en blanco
    
        # Realizar la búsqueda difusa
        def fuzzy_match(row, other_row, field, threshold):
            # Evitar la comparación si ambos tienen el mismo valor en 'documento_proveedor'
            if row['documento_proveedor'] == other_row['documento_proveedor']:
                return False, 0
    
            score = fuzz.token_sort_ratio(row[field], other_row[field])
            return score >= threshold, score
    
        results = []
        text_data = valid_data[[text_field, 'id_contrato', 'documento_proveedor']].dropna().reset_index(drop=True)
    
        for i in range(len(text_data)):
            for j in range(i + 1, len(text_data)):
                match, score = fuzzy_match(text_data.iloc[i], text_data.iloc[j], text_field, threshold)
                if match:
                    results.append((text_data.iloc[i]['id_contrato'], text_data.iloc[i]['documento_proveedor'], text_data.iloc[i][text_field], score, text_data.iloc[j][text_field], text_data.iloc[j]['documento_proveedor'], text_data.iloc[j]['id_contrato']))
    
        # Limpiar gráficos anteriores
        for i in reversed(range(self.tab_widget.widget(tab_index).layout().count())):
            widget_to_remove = self.tab_widget.widget(tab_index).layout().itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.deleteLater()
    
        # Crear la tabla de resultados
        table = QTableWidget(self)
        table.setRowCount(len(results))
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["ID Contrato 1", "Documento Proveedor 1", "Texto 1", "Similitud (%)", "Texto 2", "Documento Proveedor 2", "ID Contrato 2"])
    
        for i, (id1, doc1, text1, score, text2, doc2, id2) in enumerate(results):
            table.setItem(i, 0, QTableWidgetItem(id1))
            table.setItem(i, 1, QTableWidgetItem(doc1))
            table.setItem(i, 2, QTableWidgetItem(text1))
            table.setItem(i, 3, QTableWidgetItem(f"{score}%"))
            table.setItem(i, 4, QTableWidgetItem(text2))
            table.setItem(i, 5, QTableWidgetItem(doc2))
            table.setItem(i, 6, QTableWidgetItem(id2))
    
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)  # Ocultar encabezados de fila
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Hacer que la tabla sea de solo lectura
    
        # Reemplazar el gráfico con la tabla
        self.tab_widget.widget(tab_index).layout().addWidget(table)
        self.update()  # Forzar la actualización de la interfaz
    
    def create_pivot_table_view(self, tab_index, x_field, y_field, grouped_data):
        # Crear una tabla dinámica con los valores agrupados
        pivot_table = grouped_data

        table = QTableWidget(self)
        table.setRowCount(len(pivot_table))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels([x_field, y_field])

        for i in range(len(pivot_table)):
            table.setItem(i, 0, QTableWidgetItem(str(pivot_table.iloc[i, 0])))
            table.setItem(i, 1, QTableWidgetItem(str(pivot_table.iloc[i, 1])))

        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)  # Ocultar encabezados de fila
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Hacer que la tabla sea de solo lectura

        # Reemplazar el gráfico con la tabla
        self.tab_widget.widget(tab_index).layout().addWidget(table)
        self.update()  # Forzar la actualización de la interfaz

    def create_graph_view(self, tab_index, x_field, y_field, graph_type, grouped_data):
        # Crear el gráfico con los datos agrupados
        x_data = grouped_data[x_field].tolist()
        y_data = grouped_data[y_field].tolist()
    
        # Definir el tamaño de la figura
        fig_size = (10, 6) if graph_type != "Torta" else (14, 8)
        fig, ax = plt.subplots(figsize=fig_size)
    
        if graph_type == "Línea":
            line, = ax.plot(x_data, y_data, label=f'{x_field} vs {y_field}')
            data_points = line
        elif graph_type == "Barras":
            bars = ax.bar(x_data, y_data, label=f'{x_field} vs {y_field}')
            data_points = bars
        elif graph_type == "Dispersión":
            scatter = ax.scatter(x_data, y_data, label=f'{x_field} vs {y_field}')
            data_points = scatter
        elif graph_type == "Área":
            ax.fill_between(x_data, y_data, label=f'{x_field} vs {y_field}')
            data_points = None
        elif graph_type == "Histograma":
            ax.hist(y_data, bins=10, label=f'{y_field}', color='blue', edgecolor='black')
            data_points = None
        elif graph_type == "Torta":
            wedges, texts, autotexts = ax.pie(y_data, labels=x_data, autopct='%1.1f%%')
            data_points = wedges
    
        # Etiquetas del eje X en vertical
        if graph_type not in ["Torta", "Histograma"]:
            ax.set_xticks(range(len(x_data)))
            ax.set_xticklabels(x_data, rotation=90)
        ax.legend()
    
        # Añadir etiquetas interactivas para algunos gráficos
        annot = ax.annotate("", xy=(0,0), xytext=(10,10),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)
    
        def update_annot(ind, data_points, x_data, y_data):
            if graph_type in ["Línea", "Dispersión"]:
                pos = data_points.get_offsets()[ind["ind"][0]]
                annot.xy = pos
                text = f"{x_field}: {x_data[ind['ind'][0]]}\n{y_field}: {y_data[ind['ind'][0]]}"
            elif graph_type == "Barras":
                bar = data_points[ind['ind'][0]]
                annot.xy = (bar.get_x() + bar.get_width() / 2, bar.get_height())
                text = f'{x_field}: {x_data[ind["ind"][0]]}\n{y_field}: {bar.get_height():.2f}'
            elif graph_type == "Torta":
                wedge = data_points[ind['ind'][0]]
                center = wedge.center
                annot.xy = center
                text = f'{x_field}: {x_data[ind["ind"][0]]}\n{y_field}: {y_data[ind["ind"][0]]:.2f}'
    
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(0.4)
    
        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                if graph_type in ["Línea", "Dispersión"]:
                    cont, ind = data_points.contains(event)
                    if cont:
                        update_annot(ind, data_points, x_data, y_data)
                        annot.set_visible(True)
                        fig.canvas.draw_idle()
                    else:
                        if vis:
                            annot.set_visible(False)
                            fig.canvas.draw_idle()
                elif graph_type == "Barras":
                    for i, bar in enumerate(data_points):
                        if bar.contains(event)[0]:
                            update_annot({"ind": [i]}, data_points, x_data, y_data)
                            annot.set_visible(True)
                            fig.canvas.draw_idle()
                        else:
                            if vis:
                                annot.set_visible(False)
                                fig.canvas.draw_idle()
                elif graph_type == "Torta":
                    for i, wedge in enumerate(data_points):
                        if wedge.contains(event)[0]:
                            annot.xy = wedge.get_center()
                            update_annot({"ind": [i]}, data_points, x_data, y_data)
                            annot.set_visible(True)
                            fig.canvas.draw_idle()
                        else:
                            if vis:
                                annot.set_visible(False)
                                fig.canvas.draw_idle()
    
        fig.canvas.mpl_connect("motion_notify_event", hover)
    
        canvas = FigureCanvas(fig)  # Definir el canvas aquí
    
        plt.close(fig)  # Cerrar la figura después de definir el canvas
    
        # Reemplazar el gráfico anterior
        self.tab_widget.widget(tab_index).layout().addWidget(canvas)
        self.update()  # Forzar la actualización de la interfaz

    def update_text_edit(self, current_row, current_column, previous_row, previous_column):
        if current_row >= 0:  # Asegurarse de que una fila está seleccionada
            parameter = self.base_table.item(current_row, 1).text()
            value = self.base_table.item(current_row, 2).text()
            self.nuevos_parametros_text.setText(f"Parámetro: {parameter}\nValor: {value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashProyecto()
    window.showMaximized()  # Muestra la ventana maximizada para usar todo el espacio disponible
    sys.exit(app.exec_())