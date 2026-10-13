
"""Módulo principal para probar la conexión con la API de Gemini."""

import os
from dotenv import load_dotenv
from google import genai

# 1\. Cargar las variables del archivo .env
load_dotenv()
# 2\. Leer la API Key desde el archivo .env
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
if not api_key:
    print("❌ Error: No se encontró la API Key en el archivo .env")
else:
    print("🔑 ¡API Key cargada correctamente desde .env!")
    # 3\. Inicializar el cliente oficial de Gemini
    client = genai.Client(api_key=api_key)
    # 4\. Probar la generación de contenido
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Hola, confirma si la conexión fue exitosa para el Gate 1."
    )
    print("\n📩 Respuesta de Gemini:")
    print(response.text)
