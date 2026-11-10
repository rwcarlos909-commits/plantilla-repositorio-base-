# ==============================================================================
# PRUEBAS UNITARIAS DE ORQUESTACIÓN Y MANEJO DE ERRORES (BLOQUE 20)
# ==============================================================================

from unittest.mock import MagicMock
from langchain_core.runnables import RunnableLambda
from enrutamiento import (
    construir_cadena_con_enrutamiento,
    construir_cadena_queja_segura,
    procesar_mensaje_seguro,
    construir_paso_clasificacion,
)


def test_cadena_queja_usa_fallback_ante_fallo_del_modelo():
    """ 
    Verifica que si la cadena de quejas sufre una falla de red, with_fallbacks active la respuesta de respaldo. 
    """
    def fallar_a_proposito(x):
        raise ConnectionError("Fallo de conexión a la API simulado")

    cadena_queja_falsa = RunnableLambda(fallar_a_proposito)
    cadena_queja_segura = construir_cadena_queja_segura(cadena_queja_falsa)

    resultado = cadena_queja_segura.invoke(
        {"mensaje": "Los datos demográficos de la comuna no cargan."}
    )
    assert "soporte" in resultado.lower() or "reporte" in resultado.lower()


def test_procesar_mensaje_seguro_no_propaga_excepciones():
    """ 
    Verifica que una falla en la clasificación (antes del enrutamiento) sea capturada por el try/except global de procesar_mensaje_seguro. 
    """
    clasificacion_falsa = MagicMock()
    clasificacion_falsa.side_effect = ConnectionError(
        "Fallo en clasificación simulado")

    cadena_falsa = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa
    )
    resultado = procesar_mensaje_seguro(
        cadena_falsa,
        "¿Cómo se vincula la malla del liceo con la demanda laboral?"
    )
    assert "no pudimos procesar" in resultado.lower()
