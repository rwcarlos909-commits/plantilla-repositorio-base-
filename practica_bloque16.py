# ==============================================================================
# BLOQUE 16 - HOJA 1: Métricas Cuantitativas de Evaluación (Local / Práctica)
# Archivo: practica_bloque16.py
# # ==============================================================================

from collections import Counter
# Reutilizamos el pipeline del Bloque 15
from pipeline_texto import procesar_texto


def contar_coincidencias(tokens_ref: list[str], tokens_resp: list[str]) -> int:
    """ Calcula la suma de coincidencias mínimas por frecuencia entre la referencia y la respuesta.
    Usa Counter para considerar las repeticiones reales de cada palabra. """

    conteo_ref = Counter(tokens_ref)
    conteo_resp = Counter(tokens_resp)

    coincidencias = 0
    for token, freq_ref in conteo_ref.items():
        freq_resp = conteo_resp.get(token, 0)
        # Tomamos el mínimo entre lo que pedía la referencia y lo que dio el modelo
        coincidencias += min(freq_ref, freq_resp)

    return coincidencias


def calcular_precision_cobertura_f1(tokens_ref: list[str], tokens_resp: list[str]) -> dict:
    """ Calcula las tres métricas fundamentales de evaluación cuantitativa: - Precisión: ¿Qué porcentaje de lo que dijo la IA era relevante (estaba en la referencia)?
    - Cobertura (Recall): ¿Qué porcentaje de la referencia logró incluir la IA? - F1-Score: Promedio armónico entre Precisión y Cobertura. """

    # 1. Caso borde: Si la respuesta o la referencia están vacías
    if not tokens_ref or not tokens_resp:
        return {"precision": 0.0, "cobertura": 0.0, "f1_score": 0.0}

    # 2. Contar coincidencias mútua con frecuencias
    coincidencias = contar_coincidencias(tokens_ref, tokens_resp)

    # 3. Cálculo de métricas
    precision = coincidencias / len(tokens_resp)
    cobertura = coincidencias / len(tokens_ref)

    # 4. Cálculo del F1-Score con protección de división por cero
    if precision + cobertura == 0:
        f1_score = 0.0
    else:
        f1_score = 2 * (precision * cobertura) / (precision + cobertura)

        return {"precision": round(precision, 4),
                "cobertura": round(cobertura, 4),
                "f1_score": round(f1_score, 4)
                }


# --- DEMOSTRACIÓN EN VIVO (PRÁCTICA LOCAL) ---
if __name__ == "__main__":
    # Caso 1: Respuesta exacta
    ref1 = "El sol sale por el este."
    resp1 = "El sol sale por el este"

    # Caso 2: Respuesta con relleno/alucinación (Baja precisión)
    ref2 = "El sol sale por el este."
    resp2 = "El sol sale por el este todas las mañanas de verano de forma brillante"

    # Caso 3: Respuesta incompleta (Baja cobertura)
    ref3 = "El sol sale por el este todas las mañanas."
    resp3 = "El sol sale"

    print("--- DEMOSTRACIÓN HOJA 1 (BLOQUE 16) ---\n")

    for i, (ref, resp) in enumerate([(ref1, resp1), (ref2, resp2), (ref3, resp3)], 1):
        t_ref = procesar_texto(ref)
        t_resp = procesar_texto(resp)
        metricas = calcular_precision_cobertura_f1(t_ref, t_resp)

        print(f"--- Caso {i} ---")
        print(f"Referencia: '{ref}'")
        print(f"Respuesta: '{resp}'")
        print(
            f"Precisión: {metricas['precision']:.0%} | Cobertura: {metricas['cobertura']:.0%} | F1: {metricas['f1_score']:.2f}\\n")


# ==============================================================================
# BLOQUE 16 - HOJAS 1 Y 2: Métricas Cuantitativas sobre Salidas Reales
# Archivo: practica\_bloque16.py (Ubicado en la raíz del proyecto)
# ==============================================================================

# Intentamos importar consultar_modelo desde tu cliente modular (src/cliente\_modular.py)

try:
    from src.cliente_modular import consultar_modelo
except ImportError:
    # Alternativa si el cliente está en la raíz del proyecto
    from cliente import consultar_modelo

# ------------------------------------------------------------------------------
# 1. FUNCIÓN: Contar coincidencias con frecuencias (Bag of Words)
# ------------------------------------------------------------------------------


def contar_coincidencias(tokens_ref: list[str], tokens_resp: list[str]) -> int:
    """Calcula la suma de coincidencias mínimas entre la referencia y la respuesta."""
    conteo_ref = Counter(tokens_ref)
    conteo_resp = Counter(tokens_resp)
    coincidencias = 0
    for token, freq_ref in conteo_ref.items():
        freq_resp = conteo_resp.get(token, 0)
        coincidencias += min(freq_ref, freq_resp)
    return coincidencias

# ------------------------------------------------------------------------------
# 2. FUNCIÓN: Calcular Precisión, Cobertura y F1-Score
# ------------------------------------------------------------------------------


def calcular_precision_cobertura_f1(tokens_ref: list[str], tokens_resp: list[str]) -> dict:
    """Calcula las métricas de Precisión, Cobertura (Recall) y F1-Score."""
    if not tokens_ref or not tokens_resp:
        return {"precision": 0.0, "cobertura": 0.0, "f1_score": 0.0}

    coincidencias = contar_coincidencias(tokens_ref, tokens_resp)

    precision = coincidencias / len(tokens_resp)
    cobertura = coincidencias / len(tokens_ref)

    if precision + cobertura == 0:
        f1_score = 0.0
    else:
        f1_score = 2 * (precision * cobertura) / (precision + cobertura)
    return {
        "precision": round(precision, 4),
        "cobertura": round(cobertura, 4),
        "f1_score": round(f1_score, 4)
    }


# ------------------------------------------------------------------------------
# 3. DEMOSTRACIÓN EN VIVO (PRÁCTICAS LOCALES DE LA HOJA 1)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("==================================================")
    print(" DEMOSTRACIÓN DE MÉTRICAS CUANTITATIVAS (HOJA 1)")
    print("==================================================\n")

    ref1, resp1 = "El sol sale por el este.", "El sol sale por el este"
    ref2, resp2 = "El sol sale por el este.", "El sol sale por el este todas las mañanas de verano de forma brillante"
    ref3, resp3 = "El sol sale por el este todas las mañanas.", "El sol sale"

    casos = [
        ("Caso 1: Respuesta Exacta", ref1, resp1),
        ("Caso 2: Respuesta con Relleno", ref2, resp2),
        ("Caso 3: Respuesta Incompleta", ref3, resp3)
    ]

    for titulo, ref, resp in casos:
        tokens_ref = procesar_texto(ref)
        tokens_resp = procesar_texto(resp)
        metricas = calcular_precision_cobertura_f1(tokens_ref, tokens_resp)
        print(f"--- {titulo} ---")
        print(f"• Referencia: '{ref}'")
        print(f"• Respuesta: '{resp}'")
        print(
            f" --> Precisión: {metricas['precision']:.0%} | Cobertura: {metricas['cobertura']:.0%} | F1: {metricas['f1_score']:.2f}\n")

# --------------------------------------------------------------------------
# 4. EVALUACIÓN DE SALIDA REAL DEL MODELO (HOJA 2)
# --------------------------------------------------------------------------

print("==================================================")
print(" EVALUACIÓN DE SALIDA REAL DE LA IA (HOJA 2)")
print("==================================================\n")

# 1. Definimos la pregunta y la Referencia de Oro (Respuesta ideal esperada)
pregunta = "¿Cuáles son los tres colores primarios tradicionales?"
referencia_oro = "Los tres colores primarios tradicionales son rojo, amarillo y azul."

print(f"Pregunta enviada a la IA: '{pregunta}'")
print(f"Referencia de Oro esperada: '{referencia_oro}'\n")

# 2. Consultamos al modelo en vivo
try:
    respuesta_ia = consultar_modelo(pregunta)
    print(f"Respuesta real de la IA:\n\"{respuesta_ia}\"\n")

    # 3. Pasamos ambas cadenas por el pipeline de texto
    tokens_ref_oro = procesar_texto(referencia_oro)
    tokens_resp_ia = procesar_texto(respuesta_ia)

    # 4. Calculamos métricas cuantitativas
    metricas_ia = calcular_precision_cobertura_f1(
        tokens_ref_oro, tokens_resp_ia)

    print("--- RESULTADOS DE EVALUACIÓN CUANTITATIVA ---")
    print(f"• Precisión: {metricas_ia['precision']:.0%}")
    print(f"• Cobertura: {metricas_ia['cobertura']:.0%}")
    print(f"• F1-Score: {metricas_ia['f1_score']:.2f}")

except Exception as e:
    print(f"⚠️ No se pudo consultar la API: {e}")
    print("Verifica que tu API Key esté configurada en el entorno.")
