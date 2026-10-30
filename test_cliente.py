from unittest.mock import Mock, patch 
import pytest 
from src.cliente_modular import ( 
    con_reintento, 
    consultar_modelo, 
    enviar_peticion, 
    registrar_costo, 
) 
import src.cliente_modular as cliente

# Fixture para reiniciar el costo acumulado antes de cada prueba 
@pytest.fixture(autouse=True) 
def reiniciar_costo(): 
    cliente.costo_total_sesion = 0.0 
    yield 

# --- PRUEBAS DE ENVIAR_PETICION --- 

def test_enviar_peticion_credencial_invalida(): 
    """Confirma que 401/403 lanza ValueError (no se reintenta).""" 
    respuesta_falsa = Mock(status_code=401) 
    with patch("src.cliente_modular.requests.post", return_value=respuesta_falsa): 
        with pytest.raises(ValueError): 
            enviar_peticion("https://fake.url", {}, {}) 
            

def test_enviar_peticion_limite_de_uso(): 
    """Confirma que 429 lanza TimeoutError (sí se reintenta).""" 
    respuesta_falsa = Mock(status_code=429) 
    with patch("src.cliente_modular.requests.post", return_value=respuesta_falsa): 
        with pytest.raises(TimeoutError): 
            enviar_peticion("https://fake.url", {}, {}) 

def test_enviar_peticion_exito(): 
    """Confirma el flujo exitoso (status 200).""" 
    respuesta_falsa = Mock(status_code=200) 
    respuesta_falsa.json.return_value = {"choices": [{"message": {"content": "OK"}}]} 
    with patch("src.cliente_modular.requests.post", return_value=respuesta_falsa): 
        resultado = enviar_peticion("https://fake.url", {}, {}) 
        assert "choices" in resultado 

# --- PRUEBAS DE CON_REINTENTO --- 

def test_con_reintento_reintenta_en_timeout(): 
    """Verifica que con_reintento insiste ante TimeoutError.""" 
    intentos = {"conteo": 0} 

    def funcion_falla_dos_veces(): 
        intentos["conteo"] += 1 
        if intentos["conteo"] < 3: 
            raise TimeoutError("Error temporal") 
        return "exito" 

    with patch("src.cliente_modular.time.sleep"): 
        # Evitamos esperas reales 
        resultado = con_reintento(funcion_falla_dos_veces, reintentos=3) 
        assert resultado == "exito" 
        assert intentos["conteo"] == 3 

def test_con_reintento_falla_despues_de_maximos(): 
    """Verifica que lanza TimeoutError tras agotar los reintentos.""" 

    def siempre_falla(): 
        raise TimeoutError("Límite superado") 

    with patch("src.cliente_modular.time.sleep"): 
        with pytest.raises(TimeoutError): 
            con_reintento(siempre_falla, reintentos=2) 

# --- PRUEBAS DE REGISTRAR_COSTO --- 

def test_registrar_costo_acumula_correctamente(): 
    """Confirma el cálculo exacto de costo acumulado.""" 
    respuesta_simulada = {"usage": {"total_tokens": 1000}} 
    costo = registrar_costo(respuesta_simulada) 
    assert costo == cliente.COSTO_POR_1000_TOKENS 
    assert cliente.costo_total_sesion == cliente.COSTO_POR_1000_TOKENS 

# --- PRUEBAS DE CONSULTAR_MODELO --- 

def test_consultar_modelo_propaga_error_final(): 
    """Verifica que el fallo tras reintentos se convierte en RuntimeError.""" 
    with patch("src.cliente_modular.con_reintento", side_effect=TimeoutError): 
        with pytest.raises(RuntimeError): 
            consultar_modelo("Pregunta de prueba")