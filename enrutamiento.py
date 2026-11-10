# ==============================================================================
# BLOQUE 19: ENRUTAMIENTO CONDICIONAL MODULAR (DOMINIO DEL PROYECTO)
# ==============================================================================

from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()


# ------------------------------------------------------------------------------
# 1. Modelo de Lenguaje
# ------------------------------------------------------------------------------

modelo = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# ------------------------------------------------------------------------------
# 2. Clasificación
# ------------------------------------------------------------------------------

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente mensaje de soporte o consulta en una sola "
    "palabra: pregunta, queja o sugerencia. Responde solo con esa palabra.\n\n{mensaje}"
)


def construir_paso_clasificacion(modelo_llm):
    return (
        plantilla_clasificacion
        | modelo_llm
        | StrOutputParser()
        | (lambda texto: texto.strip().lower())
    )

# ------------------------------------------------------------------------------
# 3. Rutas de Destino
# ------------------------------------------------------------------------------


cadena_pregunta = (
    PromptTemplate.from_template(
        "Responde a esta pregunta técnica sobre mallas curriculares o demanda laboral "
        "con precisión y claridad:\n\n{mensaje}"
    )
    | modelo
    | StrOutputParser()
)

cadena_queja = (
    PromptTemplate.from_template(
        "Responde a esta queja sobre la plataforma o los datos con empatía, "
        "reconociendo el problema antes de ofrecer una solución:\n\n{mensaje}"
    )
    | modelo
    | StrOutputParser()
)

cadena_sugerencia = (
    PromptTemplate.from_template(
        "Agradece esta sugerencia para mejorar el sistema de información "
        "y explica cómo se evaluará dentro del proyecto:\n\n{mensaje}"
    )
    | modelo
    | StrOutputParser()
)

# ------------------------------------------------------------------------------
# 4. Factoría de la Cadena
# ------------------------------------------------------------------------------


def construir_cadena_con_enrutamiento(paso_clasificacion, cadena_queja=None, cadena_sugerencia=None, cadena_pregunta=None, ):
    cadena_queja = cadena_queja or RunnablePassthrough()
    cadena_sugerencia = cadena_sugerencia or RunnablePassthrough()
    cadena_pregunta = cadena_pregunta or RunnablePassthrough()

    bifurcacion = RunnableBranch(
        (lambda x: x["categoria"] == "queja", cadena_queja),
        (lambda x: x["categoria"] == "sugerencia", cadena_sugerencia),
        cadena_pregunta,  # Ruta por defecto ante preguntas o casos no reconocidos
    )

    return (
        RunnablePassthrough.assign(categoria=paso_clasificacion)
        | bifurcacion
    )


paso_clasificacion = construir_paso_clasificacion(modelo)
cadena_con_enrutamiento = construir_cadena_con_enrutamiento(
    paso_clasificacion=paso_clasificacion,
    cadena_queja=cadena_queja,
    cadena_sugerencia=cadena_sugerencia,
    cadena_pregunta=cadena_pregunta,
)

# ------------------------------------------------------------------------------
# 5. Ejecución con ejemplos del proyecto miniapp servicio orientacion ciudadana zonas rurales
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    print("------------------------------------------------------------------")
    print(" EJECUTANDO PRUEBAS DE ENRUTAMIENTO CON CASOS DEL PROYECTO")
    print("------------------------------------------------------------------\\n")

    mensajes_proyecto = [
        ("PREGUNTA TÉCNICA",
         "¿Cómo se vincula la malla del liceo técnico con la demanda laboral comunal?"),
        ("QUEJA", "Los datos demográficos de la comuna no cargan y la vista se queda congelada."),
        ("SUGERENCIA", "Sería útil poder filtrar la oferta formativa por localidad rural.")
    ]

    for tipo, msg in mensajes_proyecto:
        print(f"📌 [{tipo}]: '{msg}'")
        res = cadena_con_enrutamiento.invoke({"mensaje": msg})
        print(f"👉 RESPUESTA:\n{res}\n")
        print("-" * 66)
