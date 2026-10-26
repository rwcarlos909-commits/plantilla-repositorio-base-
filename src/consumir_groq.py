# consumir_groq.py
# Módulo de consumo del servicio Groq - Bloque 7 (versión completa)
# Alumno: Carlos | Bootcamp IA Generativa - Accenture/SkillNest

import json
import re
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
def armar_peticion(pregunta: str, system_instruction: str = "Eres un asistente útil y conciso.", forzar_json: bool = False):

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
        "messages": [
            {"role": "user", "content": pregunta.strip()
             },
            {"role": "system", "content": system_instruction
             }
        ]
    }

    if forzar_json:
        body["response_format"] = {"type": "json_object"}

    return url, headers, body


def parsear_respuesta_json(texto: str, claves_esperadas: list = None) -> dict:
    if not texto:
        raise ValueError("El texto a parsear está vacío.")

    # 1. Limpiar marcas ```json de markdown
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)

    # 2. Convertir a diccionario Python
    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError as error:
        raise ValueError("La respuesta del modelo no es un JSON válido.") from error

    # 3. Validar claves requeridas
    if claves_esperadas:
        for clave in claves_esperadas:
            if clave not in datos:
                raise ValueError(
                    f"Falta la clave requerida '{clave}' en la respuesta."
                )

    return datos


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
    print("==================================================")
    print(" PROBANDO SYSTEM PROMPT Y FORZADO JSON")
    print("==================================================")

    system_prompt = ("Eres un asistente técnico de la Región de Valparaíso. "
                     "Responde ÚNICAMENTE en formato JSON válido con las llaves "
                     "'estado', 'mensaje' y 'region'."
                     )
    pregunta_usuario = "Confirma en una frase corta que la conexión funciona."

    try:
        # 1. Armamos la petición forzando JSON y con system prompt
        url, headers, body = armar_peticion(
            pregunta=pregunta_usuario,
            system_instruction=system_prompt, forzar_json=True
        )

        # 2. Enviamos la petición
        respuesta = requests.post(url, headers=headers, json=body)
        respuesta.raise_for_status()

        datos_raw = respuesta.json()
        texto_raw = datos_raw["choices"][0]["message"]["content"]

        print("\n--- Respuesta Raw (Texto recibido de Groq) ---")
        print(texto_raw)

        # 3. Parseamos y validamos las llaves obligatorias
        dict_validado = parsear_respuesta_json(
            text_raw,
            clave_esperadas=["estado", "mensaje", "region"]
        )

        print("\n--- JSON Parseado y Validado con Éxito ---")
        print(f"Estado: {dict_validado.get('estado')}")
        print(f"Mensaje: {dict_validado.get('mensaje')}")
        print(f"Región: {dict_validado.get('region')}")

    except Exception as error:
        print(f"\nOcurrió un error en la prueba: {error}")
