import openai
import pandas as pd
import os
import glob

class ChatGPTConnector:
    def __init__(self):
        # Clave API fija
        openai.api_key = "TU CLAVE AQUI"
        self.model = "gpt-4"
        self.context = []  # Aquí almacenaremos el contexto de la conversación

        # Variables fijas para los paths de los archivos .parquet
        self.validation_path = "E:\\IntegrityAI\\Projects\\MUESTRA\\DataSet\\Entrenamiento"
        self.database_data_path = "E:\\IntegrityAI\\Projects\\MUESTRA\\DataSet\\Validar"

    def load_data(self):
        """
        Carga todos los archivos .parquet encontrados en las rutas especificadas.
        """
        # Cargar archivos .parquet de la ruta de validación
        validation_files = glob.glob(os.path.join(self.validation_path, "*.parquet"))
        if not validation_files:
            raise FileNotFoundError(f"No se encontraron archivos .parquet en {self.validation_path}")
        self.validation_data = pd.concat([pd.read_parquet(f) for f in validation_files], ignore_index=True)

        # Cargar archivos .parquet de la ruta de la base de datos
        database_files = glob.glob(os.path.join(self.database_data_path, "*.parquet"))
        if not database_files:
            raise FileNotFoundError(f"No se encontraron archivos .parquet en {self.database_data_path}")
        self.database_data = pd.concat([pd.read_parquet(f) for f in database_files], ignore_index=True)

    def analyze_data(self, user_prompt, chunk_size=1000):
        """
        Envía los datos cargados a ChatGPT de forma segmentada para que sean analizados en busca de banderas rojas.
        """
        def process_chunk(df, chunk_size):
            """Divide un DataFrame en chunks y los convierte en string."""
            for start in range(0, len(df), chunk_size):
                yield df.iloc[start:start + chunk_size].to_string()

        # Procesar los datos de validación en chunks
        for chunk in process_chunk(self.validation_data, chunk_size):
            prompt = self.create_prompt(chunk, user_prompt)
            self.send_to_chatgpt(prompt)

        # Procesar las bases de datos en chunks
        for chunk in process_chunk(self.database_data, chunk_size):
            prompt = self.create_prompt(chunk, user_prompt)
            self.send_to_chatgpt(prompt)

        # Retornar la última respuesta de ChatGPT
        return self.context[-1]['content']

    def create_prompt(self, data_chunk, user_prompt):
        """
        Crea el prompt con el chunk de datos y los parámetros del usuario.
        """
        return (
            "Eres un experto en auditoría forense especializado en la identificación de "
            "irregularidades financieras y operativas que podrían indicar corrupción, colusión, "
            "fraude u otros comportamientos ilícitos dentro de organizaciones y contratos públicos y privados. "
            "Se te proporciona un conjunto de datos derivados de operaciones financieras, transacciones, contratos, "
            "o cualquier otro documento relevante para una auditoría. Tu tarea es analizar estos datos minuciosamente, "
            "identificar patrones anómalos, transacciones sospechosas, inconsistencias, y cualquier indicio de comportamiento "
            "poco ético o ilegal. Considera las siguientes áreas de riesgo al realizar tu análisis:\n"
            "\n"
            "1. **Contratos y Adquisiciones**: Busca indicios de contratos inflados, adjudicaciones sin competencia, "
            "modificaciones injustificadas, o proveedores recurrentes con patrones inusuales.\n"
            "2. **Pagos y Transacciones**: Identifica pagos duplicados, pagos a entidades no verificadas, "
            "pagos fuera de los términos contractuales, o transacciones que no siguen el flujo normal.\n"
            "3. **Relaciones con Proveedores y Terceros**: Analiza posibles conflictos de interés, "
            "relaciones no declaradas entre empleados y proveedores, o cambios inesperados en las relaciones contractuales.\n"
            "4. **Desempeño y Entrega de Servicios**: Evalúa si el desempeño reportado coincide con los términos del contrato "
            "y si hay evidencia de que los servicios o productos fueron entregados según lo acordado.\n"
            "5. **Análisis de Datos Históricos**: Compara los datos actuales con periodos anteriores o datos de referencia para "
            "detectar desviaciones significativas o patrones sospechosos.\n"
            "\n"
            "A continuación se presentan los datos segmentados que deben ser analizados. "
            "Por favor, proporciona un análisis detallado y señala cualquier área que requiera una investigación más profunda:\n\n"
            f"**Datos Segmentados**:\n{data_chunk}\n\n"
            f"**Parámetros del Usuario**: {user_prompt}\n"
        )

    def send_to_chatgpt(self, prompt):
        """
        Envía el prompt a ChatGPT y guarda la respuesta en el contexto.
        """
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "system", "content": "Eres un especialista en auditoría forense."},
                      {"role": "user", "content": prompt}]
        )

        # Guardar la respuesta en el contexto
        self.context.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

    def chat_with_gpt(self, user_input):
        """
        Mantiene una conversación con ChatGPT utilizando el contexto previamente cargado.
        """
        # Añadir el nuevo input del usuario al contexto
        self.context.append({"role": "user", "content": user_input})

        # Enviar el contexto completo a ChatGPT
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.context
        )

        # Añadir la respuesta de ChatGPT al contexto
        self.context.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

        # Retornar la respuesta
        return response['choices'][0]['message']['content']

# Ejemplo de uso
if __name__ == "__main__":
    connector = ChatGPTConnector()

    # Cargar los archivos .parquet
    connector.load_data()

    # Realizar el análisis inicial con los datos cargados, segmentados en chunks de 1000 filas
    user_prompt = "Quiero que busques banderas rojas relacionadas con pagos duplicados y contratos sin competencia."
    result = connector.analyze_data(user_prompt, chunk_size=1000)
    print("Resultado del análisis:", result)

    # Continuar la conversación sin recargar los archivos
    user_input = "¿Qué otras banderas rojas relacionadas con proveedores recurrentes puedo encontrar?"
    response = connector.chat_with_gpt(user_input)
    print("ChatGPT:", response)

    # Otro ejemplo de continuación de la conversación
    user_input = "¿Hay algún riesgo adicional en las transacciones de alto valor que deberían ser revisadas?"
    response = connector.chat_with_gpt(user_input)
    print("ChatGPT:", response)
