# ============================================================================== 
# main.py - Punto de entrada principal del proyecto 
# Módulo 1  Unidad 1.3 - Integración con Groq API 
# Alumno: Jose Carlos Rojas| Bootcamp IA Generativa - Accenture/SkillNest 
# ============================================================================== 

import sys 
from pathlib import Path 

# 1. Asegurar que la raíz del proyecto esté en el path de ejecución 

BASE_DIR = Path(__file__).resolve().parent.parent 
if str(BASE_DIR) not in sys.path:  
    sys.path.insert(0, str(BASE_DIR)) 

# 2. Importar la función orquestadora desde el módulo refactorizado 
try: 
 from src.consumir_groq import obtener_dato_de_prueba 
except ImportError: 
 from consumir_groq import obtener_dato_de_prueba 

def main() -> None:
 """ 
Punto de entrada principal del repositorio. 
Utiliza el módulo consumir_groq para realizar la consulta inicial a la API. 
""" 
print("Iniciando aplicación principal con Groq API...\n") 
pregunta = ( 
"Confirma en una frase corta que la integración principal desde main.py funciona correctamente."
 ) 

try: 
        # Petición orquestada a través del módulo refactorizado   
     respuesta = obtener_dato_de_prueba(pregunta) 
     print("--- Respuesta de la API ---") 
     print(respuesta) 

except (ValueError, RuntimeError) as error: 
    print(f"No se pudo completar la operación: {error}") 
except Exception as exc: 
    print(f"Ocurrió un error inesperado en main.py: {exc}") 

if __name__ == "__main__":
   main() 

   