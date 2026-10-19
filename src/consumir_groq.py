import os

import requests
from dotenv import load_dotenv


load_dotenv()


def consultar_groq(pregunta: str) -> str:
    """Envía una pregunta a Groq y retorna el texto generado por la IA."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "Error: No se encontró la variable GROQ_API_KEY en el archivo .env"
        )

    url = "https://api.groq.com/openai/v1/chat/completions"
    modelo = "openai/gpt-oss-120b"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": modelo,
        "messages": [{"role": "user", "content": pregunta}],
    }
    respuesta = requests.post(url, headers=headers, json=body, timeout=30)
    try:
        respuesta.raise_for_status()
    except requests.HTTPError as error:
        try:
            detalle = respuesta.json()
        except requests.exceptions.JSONDecodeError:
            detalle = respuesta.text

        if isinstance(detalle, dict):
            error_api = detalle.get("error")
            if isinstance(error_api, dict):
                detalle = error_api.get("message", detalle)
            elif error_api is not None:
                detalle = error_api

        raise RuntimeError(
            f"Error HTTP {respuesta.status_code} de Groq: {detalle}"
        ) from error

    datos = respuesta.json()
    if not isinstance(datos, dict):
        raise RuntimeError("Groq devolvió una respuesta JSON inesperada.")

    error_api = datos.get("error")
    if error_api is not None:
        if isinstance(error_api, dict):
            mensaje_error = error_api.get("message", str(error_api))
        else:
            mensaje_error = str(error_api)
        raise RuntimeError(f"Error de Groq: {mensaje_error}")

    opciones = datos.get("choices")
    if not isinstance(opciones, list) or not opciones:
        raise RuntimeError(
            "La respuesta de Groq no contiene opciones de respuesta."
        )

    mensaje = opciones[0].get("message") if isinstance(opciones[0], dict) else None
    if not isinstance(mensaje, dict) or not isinstance(
        mensaje.get("content"), str
    ):
        raise RuntimeError("La respuesta de Groq no contiene texto generado.")

    return mensaje["content"]


if __name__ == "__main__":
    mensaje_prueba = (
        "Hola, confirma en una frase corta que la conexión con Groq funciona."
    )

    print("Enviando petición autenticada a Groq...")

    try:
        resultado = consultar_groq(mensaje_prueba)
        print("\n--- Respuesta de la API ---")
        print(resultado)
    except Exception as error:
        print(f"\nOcurrió un error: {error}")
