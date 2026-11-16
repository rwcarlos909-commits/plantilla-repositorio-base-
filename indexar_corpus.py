# ==============================================================================
# SCRIPT DE INDEXACIÓN RAG - ETAPA POR ETAPA
# ==============================================================================
import os
from dotenv import load_dotenv

# Importamos los componentes clave del ciclo RAG:
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Etapa 1: Chunking
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # Etapa 2: Embeddings
from langchain_chroma import Chroma  # Etapa 3: Vector Store

# ------------------------------------------------------------------------------
# PREPARACIÓN: Cargar variables de entorno (API Key de Gemini)
# ------------------------------------------------------------------------------

load_dotenv()

if not os.environ.get("GEMINI_API_KEY"):
    raise SystemExit(
        '❌ ERROR: No se encontró GEMINI_API_KEY en el archivo .env')


# ------------------------------------------------------------------------------
# ETAPA 0: CORPUS ORIGEN (Información que el LLM no conoce por defecto)
# ------------------------------------------------------------------------------

# Definimos una lista de textos que representan el conocimiento propio de nuestra app.

corpus_proyecto = [
    "El cliente reintenta hasta 3 veces ante un TimeoutError, aplicando una espera exponencial creciente entre intentos.",
    "Los errores de autenticación (401/403) fallan de inmediato lanzando un ValueError y jamás deben reintentarse automáticamente.",
    "El costo de cada llamada al modelo se calcula a partir de totalTokenCount y la tarifa vigente por cada 1000 tokens de entrada y salida.",
    "El agente autónomo de la Unidad 2.4 analiza la intención de la consulta y decide por sí mismo qué herramienta invocar según su ArgsSchema.",
    "Las pruebas unitarias del cliente ejecutan mocks sobre las herramientas de riesgo alto, garantizando que la suite corra en sub-segundos sin gastar cuota."
]

# ------------------------------------------------------------------------------
# ETAPA 1: CHUNKING (Fragmentación Inteligente)
# ------------------------------------------------------------------------------

# Configuramos el cortador recursivo:
# - chunk_size=200: Intentará crear bloques de máximo 200 caracteres.
# - chunk_overlap=30: Copiará los últimos 30 caracteres del chunk anterior en el siguiente
#   para evitar que las frases cortadas en el límite pierdan continuidad semántica.

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

# Convertimos nuestros textos en objetos 'Document' listos para procesar

chunks = splitter.create_documents(corpus_proyecto)

print(
    f" ETAPA 1 COMPLETADA: Se generaron {len(chunks)} chunks a partir de {len(corpus_proyecto)} documentos.")


# ------------------------------------------------------------------------------

# ETAPA 2: EMBEDDINGS (Conversión de Texto a Matemática Vectorial)
# ------------------------------------------------------------------------------

# Instanciamos el modelo de embeddings de Gemini.
# Este modelo toma cada chunk de texto y produce un vector numérico (coordenada en espacio d=3072). # que significa esta coordenada espacial? ##

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# ------------------------------------------------------------------------------
# ETAPA 3: VECTOR STORE &amp; PERSISTENCIA EN DISCO (ChromaDB)
# ------------------------------------------------------------------------------

# Definimos la carpeta local donde se guardará la base de datos vectorial
DIRECTORIO_VECTORSTORE = "vectorstore/"

print(" ETAPA 2 & 3 EN PROCESO: Calculando embeddings y guardando en ChromaDB...")

# 'Chroma.from_documents' hace 3 cosas internamente:
# 1. Toma los chunks de la Etapa 1.
# 2. Los pasa por el modelo de Embeddings de la Etapa 2.
# 3. Guarda los vectores + el texto original dentro de la carpeta 'vectorstore/'.

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DIRECTORIO_VECTORSTORE
)

print(
    f"✅ ETAPA 3 COMPLETADA: Base de datos vectorial guardada con éxito en '{DIRECTORIO_VECTORSTORE}'.")


# ------------------------------------------------------------------------------
# ETAPA 4: VERIFICACIÓN DE RECONEXIÓN (Carga Offline)
# ------------------------------------------------------------------------------
# Demostramos que podemos reconectarnos a los datos ya indexados en disco
# sin tener que volver a llamar al modelo de embeddings para recalcular.

vectorstore_recargado = Chroma(
    persist_directory=DIRECTORIO_VECTORSTORE,
    embedding_function=embeddings
)

total_almacenado = vectorstore_recargado._collection.count()
print(
    f" VERIFICACIÓN FINAL: Se confirmaron {total_almacenado} chunks almacenados y listos en disco.")
