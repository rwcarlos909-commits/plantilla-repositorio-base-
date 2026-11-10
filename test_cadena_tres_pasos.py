# ==============================================================================
# PRUEBAS UNITARIAS PARA LA CADENA DE 3 PASOS (SIN USAR LA API REAL)
# ==============================================================================

from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from cadena_tres_pasos import construir_cadena_tres_pasos


def test_cadena_tres_pasos_conecta_correctamente():
    """ 
    Verifica que la cadena ejecute exactamente 3 llamadas ordenadas al modelo y pase los datos correctamente de un paso al siguiente. 
    """
    # 1. Creamos un modelo de juguete (MagicMock)
    modelo_falso = MagicMock()
    # 2. Definimos las 3 respuestas simuladas que entregará en cada invocación
    modelo_falso.side_effect = [
        # Salida Paso 1
        AIMessage(content="1. Punto clave A\n2. Punto clave B\n3. Punto clave C"),
        # Salida Paso 2
        AIMessage(content="Texto simplificado para todo público"),
        # Salida Paso 3
        AIMessage(content="- Viñeta 1\n- Viñeta 2\n- Viñeta 3")
    ]
    # 3. Construimos la cadena inyectando el modelo falso
    cadena_test = construir_cadena_tres_pasos(modelo_falso)
    # 4. Invocamos la cadena
    resultado = cadena_test.invoke(
        {"texto_original": "Texto extenso de prueba para el test"})
    # 5. ASERSIONES: Comprobamos que el flujo funcionó exactamente 3 veces
    assert modelo_falso.call_count == 3, "El modelo debió haber sido llamado exactamente 3 veces"
    assert "- Viñeta 1" in resultado, "El resultado final debe contener la estructura formateada del paso 3"
