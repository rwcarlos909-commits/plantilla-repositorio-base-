import re
from collections import Counter


def limpiar_texto(texto: str) -> str:
    """Normaliza el texto: minúsculas y sin puntuación."""
    if not isinstance(texto, str):
        tipo = type(texto).__name__
        raise TypeError(f"limpiar_texto espera str, no {tipo}")
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def tokenizar(texto_limpio: str) -> list[str]:
    """Convierte texto limpio en una lista de tokens."""
    return texto_limpio.split()


def vectorizar(tokens: list[str]) -> Counter:
    """Cuenta cuántas veces aparece cada token."""
    return Counter(tokens)

# ---NUEVA FUNCIÓN HOJA 2 --- 
def procesar_texto(texto: str) -> list[str]: 
    """Integra la limpieza y tokenización en un solo paso.""" 
    texto_limpio = limpiar_texto(texto) 
    return tokenizar(texto_limpio)

# --- PRUEBA DE EJECUCIÓN HOJA 1 ---
if __name__ == "__main__":
    texto_prueba = "eNTONCES DEBE ESTAR CERCA DEL LUGAR, ¡cerca¡donde cayo el Ovni.. donde cayo el ovni?. Ahi cerca de la casa del julio¡¡¡."
    texto_limpio = limpiar_texto(texto_prueba)
    tokens = tokenizar(texto_limpio)
    conteo = vectorizar(tokens)
    print("--- PRUEBA HOJA 1 ---")
    print("1. Texto limpio:", texto_limpio)
    print("2. Tokens:", tokens)
    print("3. Vector de conteo:", conteo)

# 2. PRUEBA HOJA 2 (Demostración de la métrica) 
print("\n--- PRUEBA HOJA 2 ---") 
referencia = "El cielo es azul." 
respuesta = "el cielo es azul" 

# Medición sobre Texto Crudo 
tokens_ref_crudo = referencia.split()
tokens_resp_crudo = respuesta.split()
comunes_crudo = set(tokens_ref_crudo) & set(tokens_resp_crudo)
pct_crudo = len(comunes_crudo) / len(set(tokens_ref_crudo)) if tokens_ref_crudo else 0.0

# Medición sobre Texto Procesado (con pipeline)
tokens_ref_proc = limpiar_texto(referencia)
tokens_resp_proc = limpiar_texto(respuesta)
comunes_proc = set(tokens_ref_proc) & set(tokens_resp_proc)
pct_proc = len(comunes_proc) / len(set(tokens_ref_proc)) if tokens_ref_proc else 0.0

print(f"Coincidencia sobre Texto Crudo: {pct_crudo:.0%}")
print(f"Coincidencia sobre Texto Procesado: {pct_proc:.0%}")