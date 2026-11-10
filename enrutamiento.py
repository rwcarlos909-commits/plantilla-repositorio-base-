# ==============================================================================
# BLOQUE 20 - HOJA 1 Y 3: MANEJO DE ERRORES Y FALLBACKS EN ENRUTAMIENTO
# ==============================================================================

from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableBranch, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import logging
from dotenv import load_dotenv
load_dotenv()


# Configuración formal del logger del sistema
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# 1. Modelo de Lenguaje Principal
# ------------------------------------------------------------------------------

modelo = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# ------------------------------------------------------------------------------
# 2. Paso de Clasificación de la Entrada
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
# 3. Rutas de Destino Específicas
# ------------------------------------------------------------------------------


cadena_pregunta = (
    PromptTemplate.from_template(
        "Responde a esta pregunta técnica sobre mallas curriculares o demanda laboral "
        "con precisión:\n\n{mensaje}"
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
# 4. Fallback y Protección Específica para Quejas (Plan B)
# ------------------------------------------------------------------------------

respuesta_generica = RunnableLambda(
    lambda x: (
        "Gracias por contactar al equipo de soporte del sistema de mallas curriculares. "
        "Hemos recibido tu reporte sobre la plataforma y un especialista lo revisará a la brevedad."
    )
)


def construir_cadena_queja_segura(cadena_queja_base):
    """Enuelve la cadena de queja con un fallback en caso de error de red o API."""
    return cadena_queja_base.with_fallbacks([respuesta_generica])


cadena_queja_protegida = construir_cadena_queja_segura(cadena_queja)

# ------------------------------------------------------------------------------
# 5. Factoría de Enrutamiento
# ------------------------------------------------------------------------------


def construir_cadena_con_enrutamiento(
    paso_clasificacion,
    cadena_queja=None,
    cadena_sugerencia=None,
    cadena_pregunta=None,
):
    """Construye la cadena con enrutamiento inyectando las rutas o Mocks."""
    # 1. Aseguramos que ninguna ruta quede en None
    cadena_queja = cadena_queja or RunnablePassthrough()
    cadena_sugerencia = cadena_sugerencia or RunnablePassthrough()
    cadena_pregunta = cadena_pregunta or RunnablePassthrough()

    # 2. Definimos la bifurcación
    bifurcacion = RunnableBranch(
        (lambda x: x["categoria"] == "queja", cadena_queja),
        (lambda x: x["categoria"] == "sugerencia", cadena_sugerencia),
        cadena_pregunta
    )

    return (
        RunnablePassthrough.assign(categoria=paso_clasificacion)
        | bifurcacion
    )


paso_clasificacion = construir_paso_clasificacion(modelo)
cadena_con_enrutamiento = construir_cadena_con_enrutamiento(
    paso_clasificacion=paso_clasificacion,
    cadena_queja=cadena_queja_protegida,
    cadena_sugerencia=cadena_sugerencia,
    cadena_pregunta=cadena_pregunta,
)

# ------------------------------------------------------------------------------
# 6. Función de Entrada Segura con try/except General y Logger
# ------------------------------------------------------------------------------


def procesar_mensaje_seguro(cadena, mensaje):
    """Invoca la cadena de forma segura; ante cualquier fallo no capturado, registra el log y responde."""
    try:
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        logger.error(f"Error procesando mensaje en la cadena: {error}")
        return (
            "No pudimos procesar tu consulta sobre la plataforma en este momento. "
            "Por favor, intenta nuevamente en unos minutos."
        )


# ------------------------------------------------------------------------------
# 7. Prueba de ejecución en consola
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("------------------------------------------------------------------")
    print(" EJECUTANDO CADENA CON ENRUTAMIENTO Y MANEJO DE ERRORES")
    print("------------------------------------------------------------------\n")
    mensaje_queja = "Los datos demográficos de la comuna no cargan y la vista se queda congelada."
    print(f"📩 Mensaje recibido: '{mensaje_queja}'")
    print("⏳ Procesando a través de la función segura...\n")
    resultado = procesar_mensaje_seguro(cadena_con_enrutamiento, mensaje_queja)
    print("✅ RESPUESTA GENERADA:")
    print(resultado)
