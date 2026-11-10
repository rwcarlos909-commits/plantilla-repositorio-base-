# ==============================================================================
# BLOQUE 18 - HOJA 3: CADENA DE 3 PASOS REUTILIZABLE (MÓDULO OFICIAL)
# ==============================================================================

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()


def construir_cadena_tres_pasos(modelo):
    """ 
    Construye y devuelve la cadena multitarea de 3 pasos desacoplada del modelo. 
    Recibe cualquier instancia de modelo (real o mock) para facilitar pruebas. 
    """
    # Paso A: Plantilla de Extracción
    plantilla_paso1 = PromptTemplate.from_template(
        "Lee el siguiente texto y extrae únicamente sus 3 puntos clave principales:\n\n{texto_original}"
    )
    # Paso B: Plantilla de Simplificación
    plantilla_paso2 = PromptTemplate.from_template(
        "Toma estos puntos clave y reescríbelos en un lenguaje muy sencillo, "
        "sin modismos ni jerga técnica compleja:\n\n{puntos_clave}"
    )
    # Paso C: Plantilla de Formateo Markdown
    plantilla_paso3 = PromptTemplate.from_template(
        "Convierte el siguiente texto simplificado en una lista ordenada de viñetas Markdown "
        "con un tono profesional y limpio:\n\n{texto_simplificado}"
    )
    # Ensamblado de la tubería LCEL
    cadena = (
        plantilla_paso1
        | modelo
        | StrOutputParser()
        | (lambda puntos: {"puntos_clave": puntos})
        | plantilla_paso2
        | modelo
        | StrOutputParser()
        | (lambda simple: {"texto_simplificado": simple})
        | plantilla_paso3
        | modelo
        | StrOutputParser()
    )
    return cadena


# Instancia por defecto usando el modelo Groq configurado
modelo_groq = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
cadena_oficial = construir_cadena_tres_pasos(modelo_groq)
