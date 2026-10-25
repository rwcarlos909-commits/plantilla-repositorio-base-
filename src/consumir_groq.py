# consumir_groq.py
# Módulo de consumo del servicio Groq - Bloque 7 (versión completa)
# Alumno: Carlos | Bootcamp IA Generativa - Accenture/SkillNest


import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN INICIAL
# Path(__file__) obtiene la ruta de ESTE archivo (consumir_groq.py)
# .parent.parent sube dos niveles para llegar a la raíz del proyecto
# Así el .env se encuentra sin importar desde dónde ejecutes el script
# ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# ─────────────────────────────────────────────────────────────
# FUNCIÓN 1: armar_peticion(pregunta)
#
# Responsabilidad única:
#   - Validar que la pregunta no esté vacía (ANTES de gastar tokens)
#   - Obtener y validar la API key del archivo .env
#   - Preparar la URL, headers y body para la petición
# ─────────────────────────────────────────────────────────────
def armar_peticion(pregunta: str) -> tuple:
    # VALIDACIÓN DE ENTRADA
    # Si la pregunta llega vacía o solo con espacios, detenemos
    # el proceso aquí, antes de hacer cualquier llamada a la API
    if not pregunta or not pregunta.strip():
        raise ValueError("La pregunta no puede estar vacía.")

    # VALIDACIÓN DE API KEY
    # Buscamos la key del .env
    api_key = os.getenv("GROQ_API_KEY")
    # Si no existe o es un placeholder ("tu_llave_aqui"), también fallamos
    if not api_key or api_key.startswith("tu_"):
        raise ValueError(
            "No se encontró una API key válida. "
            "Configura GROQ_API_KEY en el archivo .env"
        )

    url = "https://api.groq.com/openai/v1/chat/completions"
    modelo = "openai/gpt-oss-120b"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": modelo,
        "messages": [{"role": "user", "content": pregunta.strip()}],
    }

    return url, headers, body


# ─────────────────────────────────────────────────────────────
# FUNCIÓN 2: enviar_peticion(url, headers, body)
# Responsabilidad única:
#   - Enviar la pregunta al modelo de Groq
#   - Manejar errores HTTP y de red
#   - Manejar errores de decodificación JSON
#   - No aplicar un Exception generico, para no ocultar errores inesperados
#   - Respuesta de requests.post() es un objeto Response, que tiene .json() y .text
# ─────────────────────────────────────────────────────────────
def enviar_peticion(url: str, headers: dict, body: dict) -> dict:
    try:
        # Enviamos la petición POST al endpoint de Groq
        respuesta = requests.post(url, headers=headers, json=body, timeout=30)

    except requests.exceptions.Timeout as error:
        # El servicio tardó demasiado en responder
        raise RuntimeError(
            f"El servicio de Groq tardó demasiado en responder. "
            f"Intenta de nuevo en unos segundos. Detalle: {error}"
        ) from error

    except requests.exceptions.ConnectionError as error:
        # Error de red: sin internet o el servicio está caído
        raise RuntimeError(
            f"No se pudo conectar con el servicio de Groq. "
            f"Verifica tu conexión a internet. Detalle: {error}"
        ) from error

    try:
        respuesta.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError(
            f"Error HTTP {respuesta.status_code} de Groq: {respuesta.text}"
        ) from error
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError as error:
        raise RuntimeError(
            "Error al decodificar la respuesta JSON de Groq") from error


# ─────────────────────────────────────────────────────────────
# FUNCIÓN 3: extraer_texto(datos)
# Responsabilidad única:
#   - Extraer SOLO el texto generado
#   - Manejar el caso de respuesta vacía o con formato inesperado
#   - NO sabe nada sobre cómo se obtuvo esa respuesta
# ─────────────────────────────────────────────────────────────
def extraer_texto(datos: dict) -> str:
    try:
        texto = datos["choices"][0]["message"]["content"]

    except (KeyError, IndexError) as error:
        raise RuntimeError(
            "La respuesta de Groq no trae el texto generado en el lugar esperado") from error

    # Verificamos que el texto no esté vacío
    if not texto or not texto.strip():
        raise RuntimeError(
            "El modelo devolvió una respuesta vacía."
        )
    return texto

# ─────────────────────────────────────────────────────────────
#   FUNCION: 4 calcular_costo(datos, precio_entrada, precio_salida)
# ─────────────────────────────────────────────────────────────


def calcular_costo(datos: dict, precio_entrada: float, precio_salida: float) -> float:
    uso = datos["usage"]
    tokens_entrada = uso["prompt_tokens"]
    tokens_salida = uso["completion_tokens"]
    return tokens_entrada * precio_entrada + tokens_salida * precio_salida

# ─────────────────────────────────────────────────────────────
# FUNCION 5: obtener_dato_de_prueba(pregunta)
#   - Responsabilidad única:
#   - Orquestar las tres funciones anteriores para obtener el dato de prueba
#   - Cda funcion maneja un error
# ─────────────────────────────────────────────────────────────


def obtener_dato_de_prueba(pregunta: str) -> str:

    url, headers, body = armar_peticion(pregunta)

    respuesta = enviar_peticion(url, headers, body)

    # Paso 3: Extraer y retornar el texto generado
    return extraer_texto(respuesta)


# ─────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# Este bloque solo se ejecuta cuando corres el archivo
# directamente: python src/consumir_groq.py
# NO se ejecuta cuando otro módulo importa estas funciones
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        resultado = obtener_dato_de_prueba(
            "Confirma en una frase corta que esta conexión funciona correctamente."
        )
        print(resultado)

    except (ValueError, RuntimeError) as error:
        # Capturamos solo los errores que nosotros mismos lanzamos
        # (ValueError de validación, RuntimeError de comunicación)
        print(f"No se pudo completar la operación: {error}")
