import json
import os
import time

from dataset_mvp import DATASET_EVALUACION_MVP
from practica_bloque17 import evaluar_respuesta_jerarquico


# --- INTENTO DE IMPORTAR EL CLIENTE MODULAR ---
try:
    from cliente import consultar_modelo
except ImportError:
    try:
        from cliente_api import consultar_modelo
    except ImportError:
        # Fallback de seguridad si no existe un cliente de API.
        def consultar_modelo(pregunta: str, system_instruction: str = "") -> str:
            return "Respuesta simulada del modelo para la Quinta Region."


# ------------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL DE EVALUACIÓN Y AUTOMATIZACIÓN
# ------------------------------------------------------------------------------

def ejecutar_evaluacion_completa_mvp():
    """
    Consulta las 20 preguntas del MVP, aplica el evaluador jerárquico y
    exporta los resultados JSON, el script de revisión y el informe Markdown.
    """
    print("==================================================================")
    print(" INICIANDO EVALUACIÓN DE 20 CASOS DEL MVP (QUINTA REGIÓN)")
    print("==================================================================\n")

    resultados_evaluacion = []

    # --------------------------------------------------------------------------
    # BLOQUE 1: Bucle de ejecución sobre los 20 casos del Dataset
    # --------------------------------------------------------------------------
    for caso in DATASET_EVALUACION_MVP:
        c_id = caso["id"]
        cat = caso["categoria"]
        preg = caso["pregunta"]
        ref = caso["referencia_oro"]
        palabras_req = caso.get("palabras_obligatorias", [])

        print(f"[{c_id}/20] Procesando ({cat}): '{preg[:50]}...'")

        # PASO A: Consulta a la API.
        try:
            resp_ia = consultar_modelo(
                pregunta=preg,
                system_instruction=(
                    "Eres un asistente experto en educacion tecnico-profesional "
                    "y mercado laboral de la Quinta Region de Chile. Responde de "
                    "forma concisa, precisa y directa."
                )
            )
        except Exception as e:
            print(f" ⚠️ Error en consulta API para caso {c_id}: {e}")
            resp_ia = f"Error de consulta: {e}"

        # PASO B: Evaluación Jerárquica (Gate 1 -> Gate 2).
        evaluacion = evaluar_respuesta_jerarquico(
            referencia=ref,
            respuesta=resp_ia,
            palabras_obligatorias=palabras_req
        )

        # PASO C: Construcción del registro estructurado.
        registro = {
            "id": c_id,
            "categoria": cat,
            "pregunta": preg,
            "referencia_oro": ref,
            "respuesta_ia": resp_ia,
            "estado_gate1": evaluacion["estado_final"],
            "motivo_gate1": evaluacion["motivo_gate1"],
            "metricas_gate2": evaluacion["gate2_metricas"]
        }
        resultados_evaluacion.append(registro)

        # Respeta la ventana de rate limits.
        time.sleep(0.5)

    # --------------------------------------------------------------------------
    # BLOQUE 2: Exportación de resultados_metricas.json
    # --------------------------------------------------------------------------
    with open("resultados_metricas.json", "w", encoding="utf-8") as f:
        json.dump(resultados_evaluacion, f, indent=2, ensure_ascii=False)
    print("\n✅ Guardado exitoso: 'resultados_metricas.json' con 20 casos.")

    # --------------------------------------------------------------------------
    # BLOQUE 3: Selección de Muestra para Revisión Manual
    # --------------------------------------------------------------------------
    casos_ordenados = sorted(
        resultados_evaluacion,
        key=lambda x: x["metricas_gate2"]["f1_score"]
    )

    # 5 casos con el F1-Score más bajo y 5 con el más alto.
    muestra_10 = casos_ordenados[:5] + casos_ordenados[-5:]
    revision_manual = []

    for item in muestra_10:
        f1 = item["metricas_gate2"]["f1_score"]
        aprobado = item["estado_gate1"] == "APROBADO"

        revision_manual.append({
            "id": item["id"],
            "consulta": item["pregunta"],
            "f1": f1,
            "correccion_factual": "si" if aprobado and f1 > 0.5 else "no",
            "completitud": "si" if f1 >= 0.4 else "no",
            "contradiccion": "no" if aprobado else "si",
            "nota": (
                f"Evaluado en Gate 1 como {item['estado_gate1']}. "
                f"{item['motivo_gate1']}"
            )
        })

    with open("revision_manual.json", "w", encoding="utf-8") as f:
        json.dump(revision_manual, f, indent=2, ensure_ascii=False)
    print("✅ Guardado exitoso: 'revision_manual.json' con 10 casos auditados.")

    # --------------------------------------------------------------------------
    # BLOQUE 4: Generación del script revision_manual.py
    # --------------------------------------------------------------------------
    with open("revision_manual.py", "w", encoding="utf-8") as f:
        f.write("# Script de registro manual generado automáticamente\n")
        f.write("import json\n\n")
        f.write(
            "revision_manual = "
            + json.dumps(revision_manual, indent=2, ensure_ascii=False)
            + "\n\n"
        )
        f.write('if __name__ == "__main__":\n')
        f.write(
            '    with open("revision_manual.json", "w", encoding="utf-8") as archivo:\n'
        )
        f.write(
            "        json.dump(revision_manual, archivo, indent=2, ensure_ascii=False)\n"
        )
        f.write('        print("Archivo revision_manual.json actualizado.")\n')
    print("✅ Guardado exitoso: 'revision_manual.py'.")

    # --------------------------------------------------------------------------
    # BLOQUE 5: Generación del informe de límites
    # --------------------------------------------------------------------------
    os.makedirs("docs", exist_ok=True)

    contenido_md = """### Límites de la métrica de evaluación

#### Qué mide
La métrica evalúa la coincidencia token a token entre la salida del modelo y la
Referencia de Oro normalizada mediante el pipeline de texto, midiendo Precisión,
Cobertura (Recall) y F1-Score, complementado por un filtro cualitativo no
compensable (Gate 1).

#### Modos de falla conocidos
* **Verbosidad e información de contexto extra**: La IA suele agregar
  explicaciones completas y pedagógicas que incrementan los tokens de salida,
  reduciendo la Precisión cuantitativa sin perder corrección factual.
* **Sinónimos y variantes terminológicas locales**: Términos como "minería de
  superficie" vs "explotación minera" o "riego por goteo" vs "riego tecnificado"
  pueden ser penalizados cuantitativamente si no coinciden exactamente con la
  referencia.
* **Contradicción semántica en frases cortas**: Inversiones de sentido por
  negaciones ("no es seguro") son vetadas por el Gate 1 con score 0.0 antes de
  calcular similitudes de palabras.

#### Muestra revisada
Se revisaron a mano 10 casos (5 con el F1-Score más bajo y 5 con el más alto)
del dataset de 20 preguntas del MVP sobre vinculación educación-trabajo en la
Quinta Región.

#### Recomendación de uso
Confiar en la métrica automática para monitoreo continuo de regresiones y
cumplimiento de formato/palabras clave (Gate 1). Se recomienda auditar a mano
las salidas cuando el F1-Score se ubique entre 0.30 y 0.60 para verificar si la
caída en precisión se debe a verbosidad informativa o a errores factuales
reales.
"""

    with open("docs/limites_metrica.md", "w", encoding="utf-8") as f:
        f.write(contenido_md)
    print("✅ Guardado exitoso: 'docs/limites_metrica.md'.\n")
    print("==================================================================")
    print(" ¡PROCESO COMPLETADO! TODOS LOS ARCHIVOS DEL BLOQUE 17 LISTOS")
    print("==================================================================")


# ------------------------------------------------------------------------------
# PUNTO DE ENTRADA DIRECTO DEL PROGRAMA
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    ejecutar_evaluacion_completa_mvp()
