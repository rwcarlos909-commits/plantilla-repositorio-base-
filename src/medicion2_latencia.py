# ==============================================================================
# medicion_latencia.py - Comparación de Latencia y Costo entre 2 Modelos en Groq
# Módulo 1 / Unidad 1.4 - Bloque 9 (Página 2)
# Alumno: Carlos | Bootcamp IA Generativa - Accenture/SkillNest
# ==============================================================================

from consumir_groq import armar_peticion, enviar_peticion, extraer_texto
import sys
import time
from pathlib import Path

# Configuración de ruta de importación
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def medir_modelo(
    nombre_modelo: str,
    pregunta: str,
    p_entrada: float,
    p_salida: float,
) -> dict:
    print("\n==================================================")
    print(f" PROBANDO MODELO: {nombre_modelo}")
    print("==================================================")

    url, headers, body = armar_peticion(pregunta)
    body["model"] = nombre_modelo
    latencias = []
    respuesta_json = None

    for i in range(4):
        inicio = time.perf_counter()
        respuesta_json = enviar_peticion(url, headers, body)
        fin = time.perf_counter()

        duracion = fin - inicio
        latencias.append(duracion)
        print(f" Intento {i + 1}: {duracion:.2f} segundos")

    latencia_promedio = sum(latencias) / len(latencias)
    print(
        f"\n -> Latencia Promedio ({nombre_modelo}): {latencia_promedio:.2f} s")

    # Extraer métricas de tokens si la respuesta las contiene
    usage = respuesta_json.get("usage", {})
    tokens_in = usage.get("prompt_tokens", 850)
    tokens_out = usage.get("completion_tokens", 320)

    costo_total = (tokens_in * p_entrada) + (tokens_out * p_salida)
    print(f" -> Tokens Entrada: {tokens_in} | Tokens Salida: {tokens_out}")
    print(f" -> Costo estimado request: ${costo_total:.6f} USD")

    return {
        "modelo": nombre_modelo,
        "latencia_promedio": latencia_promedio,
        "costo": costo_total,
        "respuesta": extraer_texto(respuesta_json),
    }


def main():
    pregunta = (
        "¿Cuál es la capital de Alemania y cuál es su importancia económica en Europa?"
    )

    # Modelo A: modelo = "openai/gpt-oss-120b" (Avanzado / Mayor capacidad)
    res_A = medir_modelo(
        nombre_modelo="openai/gpt-oss-120b",
        pregunta=pregunta,
        p_entrada=0.00000015,
        p_salida=0.00000060,
    )

    # Modelo B: OpenAI GPT-OSS 20B (Compacto, económico y ultra rápido)
    res_B = medir_modelo(
        nombre_modelo="openai/gpt-oss-20b",
        pregunta=pregunta,
        p_entrada=0.000000075,
        p_salida=0.00000030,
    )

    print("\n==================================================")
    print(" RESUMEN COMPARATIVO FINAL")
    print("==================================================")
    print(
        f"Modelo A ({res_A['modelo']}): {res_A['latencia_promedio']:.2f}s | "
        f"Costo: ${res_A['costo']:.6f} USD"
    )
    print(
        f"Modelo B ({res_B['modelo']}): {res_B['latencia_promedio']:.2f}s | "
        f"Costo: ${res_B['costo']:.6f} USD"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error durante la medición: {error}")
