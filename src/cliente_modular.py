import time
import random
import os
import requests
from dotenv import load_dotenv

# Cargamos las variables de entorno (.env)
load_dotenv()

# --- VARIABLES GLOBALES DE COSTOS --- 
COSTO_POR_1000_TOKENS = 0.0006 # Tarifa real aprox. USD por 1,000 tokens para gpt-oss-120b 
costo_total_sesion = 0.0


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


def con_reintento(funcion_peticion, reintentos=3, espera_base=2.0, espera_maxima=30.0): 
   """ 
   Ejecuta una petición con reintento y backoff exponencial + jitter ante fallas temporales. 
   """ 
   for intento in range(1, reintentos + 1): 
       try: 
           return funcion_peticion() 
       except TimeoutError as e: 
           if intento == reintentos: 
               raise TimeoutError(f"Se agotaron los {reintentos} reintentos sin éxito: {e}") 
           
           # Calculamos la espera exponencial con tope máximo 
           espera = min(espera_base * (2 ** (intento - 1)), espera_maxima) 
           # Agregamos jitter (hasta un 10% adicional de variación aleatoria) 
           espera_con_jitter = espera + random.uniform(0, espera * 0.1) 
           print(f"[!] Intento {intento} de {reintentos} falló. Reintentando en {espera_con_jitter:.1f}s...") 
           time.sleep(espera_con_jitter) 
       except ValueError: 
           # Errores permanentes de autenticación no se reintentan
           raise 



def registrar_costo(respuesta: dict) -> float: 
    """Extrae los tokens de la respuesta, calcula el costo y acumula el total de la sesión.""" 
    global costo_total_sesion 
    # Soportamos la estructura de uso de Groq ('usage') y Gemini ('usageMetadata') 
    uso = respuesta.get("usage", {}) or respuesta.get("usageMetadata", {}) 
    total_tokens = uso.get("total_tokens", 0) or uso.get("totalTokenCount", 0) 
    
    costo_estimado = (total_tokens / 1000) * COSTO_POR_1000_TOKENS 
    costo_total_sesion += costo_estimado 
    
    print( 
        f"[💰 Costo] Operación: {total_tokens} tokens | " 
        f"Costo est.: ${costo_estimado:.5f} | " 
        f"Acumulado sesión: ${costo_total_sesion:.5f}" 
    ) 
    return costo_estimado  

def consultar_modelo(prompt_usuario, system_prompt="Eres un asistente util.", reintentos=3): 
    """Interfaz pública para consultar la API con reintentos y registro de costos.""" 
    api_key = os.getenv("GROQ_API_KEY") 
    if not api_key: raise ValueError("No se encontró la variable GROQ_API_KEY en el entorno.") 
    
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
    
    def peticion(): 
        return enviar_peticion(url, headers, cuerpo) 

    try: 
        resultado = con_reintento(peticion, reintentos=reintentos) 
    except TimeoutError: 
        raise RuntimeError("El servicio no respondió tras varios intentos. Intenta más tarde.") 
    
    # Registramos el costo de la operación exitosa 
    registrar_costo(resultado) 
    
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
