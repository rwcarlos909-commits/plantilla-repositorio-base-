# ==============================================================================
# PRUEBAS UNITARIAS PARA EL ENRUTAMIENTO CONDICIONAL (TEXTOS DEL PROYECTO)
# ==============================================================================

from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from enrutamiento import (
    construir_cadena_con_enrutamiento, construir_paso_clasificacion,
)


def test_enrutamiento_va_a_cadena_queja():
    """Verifica que una queja sobre la plataforma ejecute la ruta de queja."""
    clasificacion_falsa = MagicMock()
    clasificacion_falsa.return_value = "queja"
    cadena_queja_falsa = MagicMock()
    cadena_queja_falsa.return_value = "Respuesta empática sobre falla en datos demográficos"

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa,
        cadena_queja=cadena_queja_falsa,
    )

    resultado = cadena.invoke(
        {"mensaje": "Los datos demográficos de la comuna no cargan."})
    assert cadena_queja_falsa.called
    assert resultado == "Respuesta empática sobre falla en datos demográficos"


def test_enrutamiento_va_a_cadena_pregunta():
    """Verifica que una consulta sobre mallas ejecute la ruta de pregunta."""
    clasificacion_falsa = MagicMock()
    clasificacion_falsa.return_value = "pregunta"
    cadena_pregunta_falsa = MagicMock()
    cadena_pregunta_falsa.return_value = "Respuesta técnica sobre mallas curriculares"
    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa,
        cadena_pregunta=cadena_pregunta_falsa,
    )
    resultado = cadena.invoke(
        {"mensaje": "¿Cómo se vincula la malla del liceo con la demanda laboral?"})
    assert cadena_pregunta_falsa.called
    assert resultado == "Respuesta técnica sobre mallas curriculares"


def test_enrutamiento_usa_default_ante_categoria_desconocida():
    """Verifica que ante una categoría no reconocida caiga en la ruta por defecto."""
    clasificacion_falsa = MagicMock()
    clasificacion_falsa.return_value = "consulta_ambigua"
    cadena_pregunta_falsa = MagicMock()
    cadena_pregunta_falsa.return_value = "Respuesta por defecto"
    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa,
        cadena_pregunta=cadena_pregunta_falsa,
    )
    resultado = cadena.invoke(
        {"mensaje": "Información general sobre sectores rurales."})
    assert cadena_pregunta_falsa.called
    assert resultado == "Respuesta por defecto"


def test_clasificacion_normaliza_antes_de_comparar():
    """Verifica que .strip().lower() limpie la salida antes de enrutar."""
    modelo_falso = MagicMock()
    modelo_falso.return_value = AIMessage(content=" Sugerencia \n")
    resultado = construir_paso_clasificacion(modelo_falso).invoke(
        {"mensaje": "Agregar filtro por sector rural."})
    assert resultado == "sugerencia"
