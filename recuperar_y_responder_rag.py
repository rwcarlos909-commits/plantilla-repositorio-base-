# ==============================================================================
# BLOQUE 26: FLUJO COMPLETO RAG (RECUPERACIÓN + GENERACIÓN CON CITAS Y GROQ 120B)
# ==============================================================================
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# ------------------------------------------------------------------------------
# 1. Carga de Variables de Entorno y Validación de APIs
# ------------------------------------------------------------------------------
load_dotenv()

missing_keys = [
    key for key in ("GEMINI_API_KEY", "GROQ_API_KEY")
    if not os.environ.get(key)
]
if missing_keys:
    raise SystemExit(
        f"❌ ERROR: Faltan estas variables en tu archivo .env: {', '.join(missing_keys)}"
    )

# ------------------------------------------------------------------------------
# 2. Reconexión al Vector Store y Configuración del Modelo Groq 120b
# ------------------------------------------------------------------------------
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma(
    persist_directory="vectorstore/",
    embedding_function=embeddings
)

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0  # Determinismo absoluto para evitar alucinaciones
)

# ------------------------------------------------------------------------------
# 3. Función Auxiliar: Formatear Contexto Numerado para Citas
# ------------------------------------------------------------------------------


def formatear_contexto(documentos_recuperados):
    """ 
    Transforma la lista de documentos en una cadena de texto numerada [1], [2], ... 
    para facilitar la citación exacta por parte del LLM. 
    """
    bloques_texto = []
    for idx, doc in enumerate(documentos_recuperados, start=1):
        bloques_texto.append(f"[{idx}] {doc.page_content}")
    return "\n\n".join(bloques_texto)


# ------------------------------------------------------------------------------
# 4. Diseño del Prompt RAG de Confinamiento
# ------------------------------------------------------------------------------
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un asistente técnico estricto y preciso.\n"
        "REGLAS OBLIGATORIAS:\n"
        "1. Responde a la pregunta del usuario utilizando ÚNICAMENTE la información provista en el CONTEXTO.\n"
        "2. Si la respuesta no está contenida en el contexto, indica explícitamente: 'La información solicitada no se encuentra "
        "en el corpus indexado.'\n"
        "3. Cada afirmación de tu respuesta DEBE incluir la cita del fragmento fuente entre corchetes, por ejemplo [1] o [1, 2].\n"
        "4. No agregues conocimiento externo ni suposiciones no respaldadas.\n\n"
        "CONTEXTO DISPONIBLE:\n{contexto}"
    ),
    ("human", "{pregunta}")
])

# Construcción de la cadena RAG declarativa (Prompt + LLM)
cadena_rag = prompt_template | llm

# ------------------------------------------------------------------------------
# 5. Función Principal de Inferencia RAG
# ------------------------------------------------------------------------------


def responder_consulta_rag(pregunta: str, k: int = 3):
    print("\n==================================================================")
    print(f"👤 CONSULTA: {pregunta}")
    print("==================================================================")

    # Paso A: Búsqueda Semántica en ChromaDB
    documentos = vectorstore.similarity_search(pregunta, k=k)
    print(f"🔎 Se recuperaron {len(documentos)} fragmentos del Vector Store.")

    # Paso B: Formatear Contexto Numerado
    contexto_numerado = formatear_contexto(documentos)

    # Paso C: Generación con Groq 120b
    respuesta = cadena_rag.invoke({
        "contexto": contexto_numerado,
        "pregunta": pregunta
    })

    print(f"\n🤖 RESPUESTA GENERADA CON CITAS:\n{respuesta.content}")


# ------------------------------------------------------------------------------
# 6. Demostración en Vivo con 2 Casos de Prueba
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Prueba 1: Pregunta contenida en el corpus
    responder_consulta_rag(
        "¿Cuál es la política de reintentos ante un TimeoutError?")

    # Prueba 2: Pregunta NO contenida en el corpus (debe activar el confinamiento)
    responder_consulta_rag("¿Cómo se configura la base de datos PostgreSQL?")
