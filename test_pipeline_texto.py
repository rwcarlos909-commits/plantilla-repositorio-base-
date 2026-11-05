
# ==============================================================================
# BLOQUE 15 - HOJA 3: Suite de Pruebas Unitarias para el Pipeline de Texto
# Archivo: test_pipeline_texto.py (Ubicado en la raíz del proyecto)
# ==============================================================================

import pytest  # Framework automatizado para descubrir y ejecutar las pruebas
from collections import Counter  # Estructura para verificar diccionarios de frecuencia
from pipeline_texto import (  # Importamos las 4 funciones desarrolladas en pipeline_texto.py
    limpiar_texto,
    tokenizar,
    vectorizar,
    procesar_texto,
)

# ------------------------------------------------------------------------------
# SECCIÓN 1: Pruebas unitarias para `limpiar_texto`
# ------------------------------------------------------------------------------

def test_limpiar_texto_normaliza_y_remueve_puntuacion():
    """
    Objetivo: Verificar que limpiar_texto pase todo a minúsculas,
    elimine los signos de puntuación y colapse espacios sobrantes.
    """
    # Entrada de prueba con mayúsculas mezcladas, puntuación y espacios irregulares
    entrada = "  ¡Hola, MUNDO! Este es un  TEST...  "
    
    # Cadena exacta esperada tras la limpieza
    esperado = "hola mundo este es un test"
    
    # Assert: Compara el resultado real de la función contra el valor esperado
    assert limpiar_texto(entrada) == esperado

def test_limpiar_texto_tipo_invalido_lanza_type_error():
    """
    Objetivo: Validar la seguridad de tipos. Si se le ingresa un dato que no sea 'str'
    (por ejemplo, un entero), debe lanzar una excepción TypeError controlada.
    """
    # pytest.raises asegura que el bloque arroje TypeError; si no lo lanza, la prueba falla
    with pytest.raises(TypeError):
        limpiar_texto(12345)

# ------------------------------------------------------------------------------
# SECCIÓN 2: Pruebas unitarias para `tokenizar` y `vectorizar`
# ------------------------------------------------------------------------------

def test_tokenizar_separa_por_espacios():
    """
    Objetivo: Confirmar que tokenizar convierta una cadena limpia en
    una lista de palabras individuales (tokens) separadas por espacio.
    """
    texto_limpio = "hola mundo este es un test"
    
    # Verificamos que retorne la lista exacta de tokens en el mismo orden
    assert tokenizar(texto_limpio) == ["hola", "mundo", "este", "es", "un", "test"]

def test_vectorizar_cuenta_frecuencias():
    """
    Objetivo: Probar que la representación "bolsa de palabras" (Counter)
    cuente con precisión cuántas veces se repite cada token.
    """
    tokens = ["gato", "perro", "gato", "gato"]
    
    # Generamos el diccionario de frecuencias
    vector = vectorizar(tokens)
    
    # Comprobamos las repeticiones exactas por palabra
    assert vector["gato"] == 3
    assert vector["perro"] == 1

# ------------------------------------------------------------------------------
# SECCIÓN 3: Pruebas unitarias para la función integradora `procesar_texto`
# ------------------------------------------------------------------------------

def test_procesar_texto_normaliza_mayusculas_y_puntuacion():
    """
    Objetivo: Confirmar la integración de limpieza + tokenización en un solo paso [1].
    """
    resultado = procesar_texto("El Cielo, es AZUL!")
    
    # Verifica la lista limpia resultante lista para ser evaluada
    assert resultado == ["el", "cielo", "es", "azul"]

def test_procesar_texto_solo_puntuacion_devuelve_lista_vacia():
    """
    Caso borde: Si la cadena contiene únicamente signos de puntuación,
    al limpiarla queda vacía y debe retornar [] sin arrojarnos un fallo inesperado [2, 3].
    """
    resultado = procesar_texto("¡¡¡...!!!")
    
    # Garantiza que cadenas sin texto alfanumérico retornen una lista vacía segura
    assert resultado == []

