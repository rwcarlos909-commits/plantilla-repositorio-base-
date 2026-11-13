
# ==============================================================================
# BLOQUE 22: AGENTE CON HERRAMIENTAS AVANZADAS (ArgsSchema) Y MEMORIA
# ==============================================================================

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()


# ------------------------------------------------------------------------------
# 1. Configuración del Modelo Groq 120b
# ------------------------------------------------------------------------------

modelo = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# ------------------------------------------------------------------------------
# 2. Definición de Esquema Pydantic (ArgsSchema) para Validación Estricta
# ------------------------------------------------------------------------------


class EsquemaConsultaMalla(BaseModel):
    especialidad: str = Field(description="Nombre de la especialidad TP a consultar (ej: agropecuaria, mecanica, tecnologia)."
                              )


class EsquemaBrechaEmpleabilidad(BaseModel):
    egresados: int = Field(description="Cantidad total de estudiantes egresados de la especialidad. Debe ser mayor a 0.", gt=0
                           )
    puestos_disponibles: int = Field(description="Cantidad de vacantes o puestos de trabajo ofrecidos por las empresas comunales.", ge=0
                                     )

# ------------------------------------------------------------------------------
# 3. Herramientas Avanzadas usando args_schema
# ------------------------------------------------------------------------------


@tool(args_schema=EsquemaConsultaMalla)
def consultar_malla_curricular_avanzada(especialidad: str) -> str:
    """Consulta la estructura de asignaturas y horas de una especialidad TP."""
    mallas = {
        "agropecuaria": "Malla Agropecuaria: Módulos en Riego Automatizado (40h), Manejo de Suelos (30h) y Cosecha Sustentable (35h).",
        "mecanica": "Malla Mecánica: Módulos en Mantenimiento de Maquinaria Agrícola (50h) y Soldadura Estructural (45h).",
        "tecnologia": "Malla TI: Módulos en Soporte de Redes Comunitarias (40h) y Programación Python Básica (60h)."
    }
    for clave, detalle in mallas.items():
        if clave in especialidad.lower():
            return detalle
    return f"No se encontró registro curricular para '{especialidad}'."


@tool(args_schema=EsquemaBrechaEmpleabilidad)
def calcular_brecha_empleabilidad_avanzada(egresados: int, puestos_disponibles: int) -> str:
    """Calcula el porcentaje de cobertura y la diferencia neta de empleo comunal."""
    diferencia = puestos_disponibles - egresados
    cobertura = (puestos_disponibles / egresados) * 100
    return (
        f"Datos de Empleabilidad: Egresados={egresados}, Puestos={puestos_disponibles}. "
        f"Diferencia neta={diferencia} puestos. Cobertura de demanda={cobertura:.1f}%."
    )


herramientas = [consultar_malla_curricular_avanzada,
                calcular_brecha_empleabilidad_avanzada]

# ------------------------------------------------------------------------------
# 4. Prompt del Agente con Historial de Chat (chat_history)
# ------------------------------------------------------------------------------

prompt_agente = ChatPromptTemplate.from_messages([
    ("system", "Eres un asesor experto en articulación TP y mercado laboral comunal. " "Utiliza las herramientas disponibles para responder de forma precisa."),
    MessagesPlaceholder("chat_history"),  # Memoria conversacional previa
    ("human", "{entrada}"),
    MessagesPlaceholder("agent_scratchpad"),  # Pasos intermedios del agente
])

# ------------------------------------------------------------------------------
# 5. Construcción del Agente y Ejecutor
# ------------------------------------------------------------------------------

agente = create_tool_calling_agent(modelo, herramientas, prompt_agente)
ejecutor = AgentExecutor(agent=agente, tools=herramientas, verbose=True)

# ------------------------------------------------------------------------------
# 6. Memoria Situacional (Gestión de Sesiones)
# ------------------------------------------------------------------------------

almacen_sesiones = {}


def obtener_historial_sesion(session_id: str) -> ChatMessageHistory:
    if session_id not in almacen_sesiones:
        almacen_sesiones[session_id] = ChatMessageHistory()
    return almacen_sesiones[session_id]


agente_con_memoria = RunnableWithMessageHistory(
    ejecutor,
    obtener_historial_sesion,
    input_messages_key="entrada",
    history_messages_key="chat_history"
)


# ------------------------------------------------------------------------------
# 7. Demostración en Vivo: Conversación Multiturno
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    configuracion_sesion = {"configurable": {"session_id": "sesion_comuna_01"}}
    print("------------------------------------------------------------------")
    print(" PROBANDO AGENTE CON MEMORIA CONVERSACIONAL (BLOQUE 22)")
    print("------------------------------------------------------------------\n")

    # Turno 1
    p1 = "¿Qué módulos tiene la malla de mecánica?"
    print(f"👤 Usuario (Turno 1): {p1}")
    r1 = agente_con_memoria.invoke(
        {"entrada": p1}, config=configuracion_sesion)
    print(f"🤖 Agente: {r1['output']}\n")

   # Turno 2 (Pregunta contextual basada en el Turno 1)
    p2 = "¿Y cuántas horas totales suman los módulos que me mencionaste?"
    print(f"👤 Usuario (Turno 2 - Seguimiento): {p2}")
    r2 = agente_con_memoria.invoke(
        {"entrada": p2}, config=configuracion_sesion)
    print(f"🤖 Agente: {r2['output']}\n")
