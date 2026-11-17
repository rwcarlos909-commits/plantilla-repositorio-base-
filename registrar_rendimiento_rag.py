# ==============================================================================
# BLOQUE 28: INSTRUMENTACIÓN DE LATENCIA, TOKENS Y COSTO DEL FLUJO RAG
# ==============================================================================
import os
import time
import json
from contextlib import contextmanager
from datetime import datetime, timezone
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# ------------------------------------------------------------------------------
# 1. Carga de Variables y Configuración Inicial
# ------------------------------------------------------------------------------
load_dotenv()

if not os.environ.get("GEMINI_API_KEY") or not os.environ.get("GROQ_API_KEY"):
    raise SystemExit("❌ ERROR: Faltan las claves en tu archivo .env")

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma(
    persist_directory="vectorstore/",
    embedding_function=embeddings
)

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

# ------------------------------------------------------------------------------
# 2. Context Manager para Medición de Tiempos
# ------------------------------------------------------------------------------
tiempos = {}


@contextmanager
def medir_etapa(etapa_nombre: str):
    inicio = time.perf_counter()
    try:
        yield
    finally:
        fin = time.perf_counter()
        tiempos[etapa_nombre] = (fin - inicio) * \
            1000  # Convertir a milisegundos

# ------------------------------------------------------------------------------
# 3. Formateo de Contexto y Prompt RAG
# ------------------------------------------------------------------------------


def formatear_contexto(documentos_recuperados):
    bloques_texto = []
    for idx, doc in enumerate(documentos_recuperados, start=1):
        bloques_texto.append(f"[{idx}] {doc.page_content}")
    return "\n\n".join(bloques_texto)


prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un asistente técnico estricto y preciso.\\n"
        "REGLAS OBLIGATORIAS:\n"
        "1. Responde a la pregunta utilizando ÚNICAMENTE la información provista en el CONTEXTO.\n"
        "2. Si la respuesta no está contenida en el contexto, indica explícitamente: '"
        "La información solicitada no se encuentra en el corpus indexado.'\n"
        "3. Cada afirmación DEBE incluir la cita entre corchetes, por ejemplo [14].\n\n"
        "CONTEXTO DISPONIBLE:\n{contexto}"
    ),
    ("human", "{pregunta}")
])

cadena_rag = prompt_template | llm

# ------------------------------------------------------------------------------
# 4. Función de Inferencia Instrumentada
# ------------------------------------------------------------------------------


def ejecutar_consulta_instrumentada(pregunta: str, k: int = 3):
    tiempos.clear()

    # Etapa A: Búsqueda Semántica en ChromaDB (Red + VectorStore)
    with medir_etapa("busqueda_vectorial_ms"):
        documentos = vectorstore.similarity_search(pregunta, k=k)

    contexto_numerado = formatear_contexto(documentos)

    # Etapa B: Inferencia y Generación con Groq 120b
    with medir_etapa("generacion_llm_ms"):
        respuesta = cadena_rag.invoke(
            {"contexto": contexto_numerado, "pregunta": pregunta})

    tiempo_total_ms = sum(tiempos.values())

    # Extracción de metadatos de tokens (si el proveedor los expone)
    tokens_info = getattr(respuesta, "usage_metadata", None)

    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pregunta": pregunta,
        "k": k,
        "desglose_tiempos_ms": {k: round(v, 2) for k, v in tiempos.items()},
        "tiempo_total_ms": round(tiempo_total_ms, 2),
        "tokens": tokens_info if tokens_info else "Metadatos de tokens no disponibles en este proveedor"
    }

    print("\n==================================================================")
    print(f"📊 REGISTRO DE RENDIMIENTO Y LATENCIA (RAG k={k})")
    print("==================================================================")
    print(json.dumps(registro, indent=2, ensure_ascii=False))

    # Persistencia del registro en un archivo JSONL (JSON Lines)
    with open("registros-latencia-costo.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

    print(f"\n🤖 RESPUESTA:\n{respuesta.content}")


if __name__ == "__main__":
    ejecutar_consulta_instrumentada(
        "¿Cuál es la política de reintentos ante un TimeoutError?")
