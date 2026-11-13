
# ==============================================================================
# BLOQUE 21: PRIMER AGENTE CON HERRAMIENTAS Y TRAZA DE DECISIÓN (ReAct)
# ==============================================================================
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
# 👈 Importación desde langchain_classic
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from dotenv import load_dotenv
load_dotenv()


# ------------------------------------------------------------------------------
# 1. Configuración del Modelo de Lenguaje
# ------------------------------------------------------------------------------

modelo = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# ------------------------------------------------------------------------------
# 2. Definición de Herramientas (@tool) orientadas al Proyecto
# ------------------------------------------------------------------------------


@tool
def consultar_malla_curricular(especialidad: str) -> str:
    """ 
    Busca la estructura curricular y módulos técnicos de una especialidad TP. 
    Usar cuando el usuario pregunte sobre asignaturas, horas o contenidos de la malla. 
    """
    mallas = {
        "agropecuaria": "Malla Agropecuaria: Módulos en Riego Automatizado (40h), ""Manejo de Suelos (30h) y Cosecha Sustentable (35h).",
        "mecanica": "Malla Mecánica: Módulos en Mantenimiento de Maquinaria Agrícola (50h) y Soldadura Estructural (45h).",
        "tecnologia": "Malla TI: Módulos en Soporte de Redes Comunitarias (40h) y Programación Python Básica (60h)."
    }

    # Búsqueda por coincidencia de palabra clave
    for clave, detalle in mallas.items():
        if clave in especialidad.lower():
            return detalle
    return f"No se encontró registro curricular para la especialidad '{especialidad}'."


@tool
def calcular_brecha_empleabilidad(egresados: int, puestos_disponibles: int) -> str:
    """ 
    Calcula el porcentaje de brecha entre egresados de mallas TP y puestos laborales. 
    Usar cuando la pregunta requiera calcular porcentajes o deficit de contratacion laboral. 
    """
    try:
        if egresados <= 0:
            return "El número de egresados debe ser mayor a 0."
        diferencia = puestos_disponibles - egresados
        porcentaje_cobertura = (puestos_disponibles / egresados) * 100
        return (
            f"Análisis de Empleabilidad: Egresados={egresados}, Puestos={puestos_disponibles}. "
            f"Diferencia neta={diferencia} puestos. Cobertura de demanda={porcentaje_cobertura:.1f}%."
        )
    except Exception as error:
        return f"Error al calcular la brecha: {error}"


# Lista de herramientas disponibles para el agente
herramientas = [consultar_malla_curricular, calcular_brecha_empleabilidad]

# ------------------------------------------------------------------------------
# 3. Prompt del Agente con MessagesPlaceholder("agent_scratchpad")
# ------------------------------------------------------------------------------

# agent_scratchpad es la memoria intermedia requerida para guardar el ciclo ReAct
prompt_agente = ChatPromptTemplate.from_messages([
    ("system", "Eres un asesor experto en articulación de mallas curriculares y demanda laboral comunal. "
     "" "Responde a las consultas utilizando las herramientas disponibles según sea necesario."
     ),
    ("human", "{entrada}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# ------------------------------------------------------------------------------
# 4. Construcción y Orquestación del AgentExecutor
# ------------------------------------------------------------------------------

agente = create_tool_calling_agent(
    llm=modelo,
    tools=herramientas,
    prompt=prompt_agente
)

# AgentExecutor coordina la ejecución autónoma, los reintentos y muestra la traza
ejecutor_agente = AgentExecutor(
    agent=agente,
    tools=herramientas,
    verbose=True,  # Muestra la traza ReAct en consola
    return_intermediate_steps=True  # Permite inspeccionar programáticamente los pasos
)

# ------------------------------------------------------------------------------
# 5. Demostración y Prueba de Invocación
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    print("------------------------------------------------------------------")
    print(" EJECUTANDO AGENTE AUTÓNOMO CON DOS HERRAMIENTAS (BLOQUE 21)")
    print("------------------------------------------------------------------\\n")

    consulta = "¿Qué módulos tiene la malla de agropecuaria y cuál es la cobertura si egresan 50 estudiantes para 80 puestos laborales?"
    print(f"📩 Consulta del usuario: '{consulta}'\n")

    resultado = ejecutor_agente.invoke({"entrada": consulta})

    print("\n✅ RESPUESTA FINAL DEL AGENTE:")
    print(resultado["output"])

    print("\n🔍 INSPECCIÓN DE PASOS INTERMEDIOS (intermediate_steps):")
    for accion, observacion in resultado["intermediate_steps"]:
        print(f" 📌 Herramienta usada: {accion.tool}")
        print(f" Argumentos: {accion.tool_input}")
        print(f" Observación devuelta: {observacion}\n")
