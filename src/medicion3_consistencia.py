# ==============================================================================
# Medición de Consistencia de Prompts (Bloque 10)
# ==============================================================================


from src.banco import SYSTEM_ASISTENTE_VALPARAISO
from src.consumir_groq import armar_peticion, parsear_respuesta_json
import os
import sys
import requests
# Permitir importar módulos desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def probar_consistencia(intentos: int = 4):
    print("==================================================")
    print(" PROBANDO CONSISTENCIA DE PROMPT (BLOQUE 10)")
    print("==================================================")

    pregunta_prueba = "¿Dónde puedo estudiar un curso de mecánica o soldadura presencial cerca de San Felipe o Los Andes?"
    exitos = 0
    llaves_requeridas = ["recomendacion", "comuna_o_zona", "categoria"]

    for i in range(1, intentos + 1):
        print(f"\n--- Intento {i}/{intentos} ---")
        try:
            # 1\. Armar petición usando el prompt del banco
            url, headers, body = armar_peticion(
                pregunta=pregunta_prueba,
                system_instruction=SYSTEM_ASISTENTE_VALPARAISO,
                forzar_json=True
            )

            # 2. Enviar a Groq
            respuesta = requests.post(url, headers=headers, json=body)
            respuesta.raise_for_status()
            texto_raw = respuesta.json()["choices"][0]["message"]["content"]
            print(f"Respuesta recibida: {texto_raw}")

            # 3. Validar JSON y llaves
            datos_dict = parsear_respuesta_json(
                texto_raw, claves_esperadas=llaves_requeridas)
            print("Status: VALIDACIÓN EXITOSA")
            exitos += 1

        except Exception as error:
            print(f"Status: FALLÓ (Error: {error})")

    # Resumen
    tasa_exito = (exitos / intentos) * 100
    print("\n==================================================")
    print(" RESUMEN DE CONSISTENCIA")
    print("==================================================")
    print(f" Pruebas Exitosas: {exitos}/{intentos}")
    print(f" Tasa de Consistencia: {tasa_exito:.1f}%")
    print("==================================================")


if __name__ == "__main__":
    probar_consistencia()
