# ==============================================================================
# BLOQUE 23: SUITE DE PRUEBAS UNITARIAS PARA AGENTE Y HERRAMIENTAS (PYTEST)
# ==============================================================================

import pytest
from pydantic import ValidationError
from agente_memoria import (
    consultar_malla_curricular_avanzada,
    calcular_brecha_empleabilidad_avanzada,
    EsquemaBrechaEmpleabilidad
)

# ------------------------------------------------------------------------------
# 1. Pruebas Unitarias de Herramientas (@tool)
# ------------------------------------------------------------------------------


def test_consultar_malla_mecanica_retorna_datos_correctos():
    """Verifica que la consulta de la malla de mecánica retorne los módulos esperados."""
    resultado = consultar_malla_curricular_avanzada.invoke(
        {"especialidad": "mecanica"})
    assert "Mantenimiento de Maquinaria Agrícola" in resultado
    assert "50h" in resultado
    assert "Soldadura Estructural" in resultado


def test_consultar_malla_desconocida_maneja_respuesta_limpia():
    """Verifica que especialidades no registradas entreguen un mensaje controlado."""
    resultado = consultar_malla_curricular_avanzada.invoke(
        {"especialidad": "aeronautica"})
    assert "No se encontró registro curricular" in resultado


def test_calcular_brecha_empleabilidad_calculo_correcto():
    """Verifica que el cálculo de cobertura porcentual sea exacto."""
    resultado = calcular_brecha_empleabilidad_avanzada.invoke(
        {"egresados": 50, "puestos_disponibles": 80})
    assert "Cobertura de demanda=160.0%" in resultado
    assert "Diferencia neta=30 puestos" in resultado

# ------------------------------------------------------------------------------
# 2. Pruebas de Validación de Esquema con Pydantic (ArgsSchema)
# ------------------------------------------------------------------------------


def test_esquema_brecha_rechaza_egresados_cero_o_negativos():
    """Verifica que Pydantic impida instanciar datos con egresados <= 0 (gt=0)."""
    with pytest.raises(ValidationError):
        EsquemaBrechaEmpleabilidad(egresados=0, puestos_disponibles=50)
