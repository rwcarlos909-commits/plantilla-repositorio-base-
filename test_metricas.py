# ==============================================================================
# BLOQUE 16 - HOJA 3: Suite de Pruebas Unitarias para Métricas Cuantitativas
# Archivo: test_metricas.py (Ubicado en la raíz del proyecto)
# ==============================================================================

import pytest
from practica_bloque16 import (
    contar_coincidencias, calcular_precision_cobertura_f1,
)

# ------------------------------------------------------------------------------
# 1. PRUEBAS PARA `contar_coincidencias`
# ------------------------------------------------------------------------------


def test_contar_coincidencias_frecuencia_minima():
    """ 
    Verifica que el uso de Counter tome la frecuencia MÍNIMA entre la referencia y la respuesta, 
    evitando inflar coincidencias con palabras repetidas. 
    """
    ref = ["el", "sol", "sale", "el"]
    resp = ["el", "sol"]

    # 'el' aparece 2 veces en ref y 1 en resp -> min(2, 1) = 1
    # 'sol' aparece 1 vez en ref y 1 en resp -> min(1, 1) = 1
    # Total de coincidencias esperadas = 2
    assert contar_coincidencias(ref, resp) == 2


def test_contar_coincidencias_sin_palabras_comunes_devuelve_cero():
    """Confirma que si no hay ninguna palabra compartida, devuelva 0."""
    ref = ["el", "sol"]
    resp = ["la", "luna"]
    assert contar_coincidencias(ref, resp) == 0

# ------------------------------------------------------------------------------
# 2. PRUEBAS PARA `calcular_precision_cobertura_f1`
# ------------------------------------------------------------------------------


def test_metricas_respuesta_exacta_devuelve_uno():
    """Confirma que listas idénticas entreguen 100% (1.0) en Precisión, Cobertura y F1."""
    tokens = ["el", "cielo", "es", "azul"]
    metricas = calcular_precision_cobertura_f1(tokens, tokens)

    assert metricas["precision"] == 1.0
    assert metricas["cobertura"] == 1.0
    assert metricas["f1_score"] == 1.0


def test_metricas_respuesta_con_relleno_reduce_precision():
    """Verifica que agregar texto sobrante reduzca la Precisión pero mantenga la Cobertura."""
    ref = ["el", "sol", "sale"]
    resp = ["el", "sol", "sale", "todas", "las", "mañanas"]
    metricas = calcular_precision_cobertura_f1(ref, resp)
    assert metricas["cobertura"] == 1.0  # Cubrió todo el origen
    assert metricas["precision"] < 1.0  # Cae por las 3 palabras de relleno


def test_metricas_respuesta_incompleta_reduce_cobertura():
    """Verifica que omitir palabras reduzca la Cobertura pero mantenga la Precisión."""
    ref = ["el", "sol", "sale", "por", "el", "este"]
    resp = ["el", "sol"]
    metricas = calcular_precision_cobertura_f1(ref, resp)
    assert metricas["precision"] == 1.0  # Todo lo que dijo es correcto
    assert metricas["cobertura"] < 1.0  # Cae por faltar información


def test_metricas_listas_vacias_devuelven_cero():
    """Caso borde: verifica la protección contra división por cero si alguna lista está vacía."""
    metricas = calcular_precision_cobertura_f1([], ["hola"])
    assert metricas["precision"] == 0.0
    assert metricas["cobertura"] == 0.0
    assert metricas["f1_score"] == 0.0
