import time
import os
import requests
from dotenv import load_dotenv

# Cargamos las variables de entorno (.env)
load_dotenv()


def enviar_peticion(url, headers, cuerpo):
    """Envía la petición HTTP y clasifica errores temporales vs permanentes."""
    try:
        respuesta = requests.post(
            url, json=cuerpo, headers=headers, timeout=10)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        raise TimeoutError(
            "No se pudo contactar al proveedor. Puede ser momentáneo.")

    # 401 / 403: Error permanente de autenticación
    if respuesta.status_code in (401, 403):
        raise ValueError(
            "Credencial inválida o sin permiso. Revisa tu API key.")

    # 429 / 5xx: Error temporal (Rate limit o caída del servidor)
    if respuesta.status_code == 429 or respuesta.status_code >= 500:
        raise TimeoutError(
            "El proveedor no pudo procesar la petición. Hay que esperar y reintentar.")
    respuesta.raise_for_status()
    return respuesta.json()


def con_reintento(funcion_peticion, reintentos=2, espera=1):
    """Ejecuta una petición y la reintenta solo si ocurre un error temporal (TimeoutError)."""
    for intento in range(reintentos + 1):
        try:
            return funcion_peticion()
        except TimeoutError as e:
            if intento < reintentos:
                time.sleep(espera)
            else:
                raise TimeoutError(
                    f"Se agotaron los {reintentos} reintentos sin éxito: {e}")
        except ValueError:
            # Los errores de autenticación (401/403) no se reintentan
            raise


def consultar_modelo(prompt_usuario, system_prompt="Eres un asistente util.", reintentos=2):
    """Interfaz publica para consultar la API de Groq con reintentos automaticos."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "No se encontro la variable GROQ_API_KEY en el entorno.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    cuerpo = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_usuario}
        ]
    }
# Definimos la llamada a ejecutar dentro de con_reintento

    def peticion():
        return enviar_peticion(url, headers, cuerpo)

    try:
        # Ejecutamos con reintento ante errores temporales
        resultado = con_reintento(peticion, reintentos=reintentos)
    except TimeoutError:
        raise RuntimeError(
            "No se pudo obtener respuesta del proveedor tras varios intentos. Intenta más tarde.")

# Extraemos y retornamos únicamente el texto de la respuesta
    return resultado["choices"][0]["message"]["content"]


# --- PRUEBA DE EJECUCIÓN DIRECTA ---
if __name__ == "__main__":
    print("Enviando consulta al cliente modular...")
    try:
        respuesta = consultar_modelo(
            "En una sola frase, ¿que es la resiliencia en software?")
        print("\nRespuesta recibida exitosamente:")
        print(respuesta)
    except Exception as e:
        print(f"\nError capturado: {e}")
