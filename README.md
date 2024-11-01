# IntegrityAI - Forensic Auditing with NLP and Data Analysis

## English

### Overview

IntegrityAI is a tool designed to support forensic auditing processes in the public sector by implementing advanced data analysis techniques and Natural Language Processing (NLP) tools. Developed using the TDSP (Team Data Science Process) methodology, IntegrityAI centralizes various public and private data sources, enabling efficient identification of potential "red flags" in public procurement processes. The tool aims to improve accuracy and efficiency in detecting anomalous behavior, ultimately promoting transparency in public management.

### Key Features

- **Centralized Data Access**: Access multiple data sources in one place, including databases, APIs, and web scraping tools.
- **Red Flags Identification**: Detects potential fraud indicators in public sector contracts, focusing on corruption, collusion, and other fraudulent activities.
- **Data Analysis and Visualization**: Provides graphical interfaces and analytical tools for comprehensive data examination, including time comparisons and keyword searches.
- **NLP and Embedding Integration**: Incorporates NLP models to interpret and analyze textual data, answering questions based on stored datasets.
- **Customizable Dashboard**: Tailored interface for data filtering, report generation, and specific forensic analyses within the SECOP II database.

### Requirements

- **Python 3.9** and packages such as `pandas`, `matplotlib`, and NLP libraries (e.g., `GPT4All`, `Nomic`).
- **APIs**: Integrates external APIs (e.g., Google Custom Search, Socrata) for enhanced data retrieval and analysis.
- **Recommended Hardware**: Intel Core i9 processor, 64GB RAM, Radeon RX 600 (8GB VRAM).

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/jsabogalv/IntegrityAI-Beta.git
   ```

2. **Install the necessary Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys** for Google Custom Search, Socrata, and Nomic as environment variables.

### Usage

1. **Launch the tool** from the command line:
   ```bash
   python main_app.py
   ```

2. Follow the prompts to create or load a project. Use the intuitive dashboard to filter and analyze data.

3. Access specific datasets for detailed analysis and generate reports directly from the application interface.

### Documentation

Refer to the [User Manual] in "/README/Manual Usuario Final v1.2.pdf" for detailed setup, usage instructions, and troubleshooting tips.


### Authors and Acknowledgments

- **Author**: Jeison Stiven Sabogal Varela, as part of a Master's Thesis at Universidad Central, Colombia.
- **Acknowledgments**: Special thanks to Carlos Issac Zainea Maya for direction and guidance.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Español

### Descripción General

IntegrityAI es una herramienta diseñada para apoyar los procesos de auditoría forense en el sector público mediante la implementación de técnicas avanzadas de análisis de datos y herramientas de procesamiento de lenguaje natural (PLN). Desarrollada utilizando la metodología TDSP (Proceso de Ciencia de Datos en Equipo), IntegrityAI centraliza diversas fuentes de datos públicas y privadas, permitiendo la identificación eficiente de posibles "banderas rojas" en los procesos de contratación pública. La herramienta busca mejorar la precisión y eficiencia en la detección de comportamientos anómalos, promoviendo la transparencia en la gestión pública.

### Funcionalidades Clave

- **Acceso Centralizado a Datos**: Acceso a múltiples fuentes de datos en un solo lugar, incluidas bases de datos, APIs y herramientas de web scraping.
- **Identificación de Banderas Rojas**: Detecta posibles indicadores de fraude en contratos del sector público, enfocándose en corrupción, colusión y otras actividades fraudulentas.
- **Análisis y Visualización de Datos**: Proporciona interfaces gráficas y herramientas analíticas para un examen exhaustivo de los datos, incluidas comparaciones temporales y búsquedas por palabras clave.
- **Integración de NLP y Embeddings**: Incorpora modelos de NLP para interpretar y analizar datos textuales, respondiendo preguntas basadas en conjuntos de datos almacenados.
- **Dashboard Personalizable**: Interfaz adaptada para el filtrado de datos, generación de reportes y análisis forense específico en la base de datos SECOP II.

### Requisitos

- **Python 3.9** y paquetes como `pandas`, `matplotlib` y librerías de NLP (p. ej., `GPT4All`, `Nomic`).
- **APIs**: Integración de APIs externas (p. ej., Google Custom Search, Socrata) para una recuperación y análisis de datos mejorados.
- **Hardware Recomendado**: Procesador Intel Core i9, 64GB RAM, Radeon RX 600 (8GB VRAM).

### Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/jsabogalv/IntegrityAI-Beta.git
   ```

2. **Instalar los paquetes de Python necesarios**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar las claves API** para Google Custom Search, Socrata y Nomic en las variables de entorno.

### Uso

1. **Ejecute la herramienta** desde la línea de comandos:
   ```bash
   python main_app.py
   ```

2. Siga las indicaciones para crear o cargar un proyecto. Utilice el dashboard intuitivo para filtrar y analizar datos.

3. Acceda a conjuntos de datos específicos para un análisis detallado y genere informes directamente desde la interfaz de la aplicación.

### Documentación

Consulte el [Manual de Usuario] en "/README/Manual Usuario Final v1.2.pdf" para obtener instrucciones detalladas sobre la configuración, uso y resolución de problemas.

### Autores y Agradecimientos

- **Autor**: Jeison Stiven Sabogal Varela, como parte de una tesis de maestría en la Universidad Central, Colombia.
- **Agradecimientos**: Agradecimientos especiales a Carlos Issac Zainea Maya por su dirección y orientación.

### Licencia

Este proyecto está bajo la Licencia MIT. Consulte el archivo LICENSE para más detalles.
