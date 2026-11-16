# ==============================================================================
# BLOQUE 25: PRUEBA DE RESILIENCIA Y MAPA DE ERRORES DEL VECTOR STORE
# ## Por que se hace esta prueba?
# Esta prueba tiene como objetivo verificar que el Vector Store (ChromaDB) pueda reconectarse y recuperar datos
# correctamente después de haber sido persistido en disco. Esto es crucial para garantizar la resiliencia del sistema
# y la integridad de los datos indexados, especialmente en entornos de producción donde los reinicios o fallos pueden ocurrir.
# ## Qué se espera lograr?
# Se espera que el script pueda: 1. Validar la existencia del directorio del Vector Store.
# 2. Reconectarse al Vector Store persistido sin necesidad de recalcular embeddings.
# 3. Recuperar y mostrar un número de chunks indexados.
# 4. Realizar una consulta semántica de prueba y mostrar los resultados con sus respectivas puntuaciones de similitud.
# ==============================================================================

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# ------------------------------------------------------------------------------
# 1. Validación de Entorno y Claves
# ------------------------------------------------------------------------------

load_dotenv()  # que significa el acronimo dotenv? ##

if not os.environ.get("GEMINI_API_KEY"):
    raise SystemExit(
        '❌ ERROR CRÍTICO: Falta GEMINI_API_KEY en el archivo .env.')

DIRECTORIO_VECTORSTORE = "vectorstore/"

# ------------------------------------------------------------------------------
# 2. Diagnóstico de Persistencia en Disco
# ------------------------------------------------------------------------------
if not os.path.exists(DIRECTORIO_VECTORSTORE):
    raise SystemExit(f"❌ ERROR DE DIRECTORIO: No existe la carpeta '{DIRECTORIO_VECTORSTORE}'. "
                     "Ejecuta primero 'python indexar_corpus.py'."
                     )

print(" Iniciando diagnóstico del Vector Store persistido...")

# ------------------------------------------------------------------------------
# 3. Conexión Segura al Índice y Prueba de Recuperación
# ------------------------------------------------------------------------------
try:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001")

    vectorstore = Chroma(
        persist_directory=DIRECTORIO_VECTORSTORE,
        embedding_function=embeddings
    )

    total_chunks = vectorstore._collection.count()
    if total_chunks == 0:
        print("⚠️ ADVERTENCIA: La base de datos existe pero está vacía (0 chunks).")
    else:
        print(
            f"✅ CONEXIÓN EXITOSA: La base contiene {total_chunks} chunks indexados.")

    # --------------------------------------------------------------------------
    # 4. Prueba de Recuperación Semántica Directa (k=2)
    # --------------------------------------------------------------------------
    consulta_prueba = "¿Cómo maneja el sistema los errores de autenticación?"
    print(f"\n🧪 Probando consulta semántica: '{consulta_prueba}'")

    # Realiza la búsqueda por similitud recuperando los 2 fragmentos más cercanos
    resultados = vectorstore.similarity_search_with_score(consulta_prueba, k=2)

    print("\n📄 RESULTADOS DE RECUPERACIÓN:")
    for idx, (doc, score) in enumerate(resultados, start=1):
        print(f" [{idx}] Distancia: {score:.4f} | Fragmento: \"{doc.page_content}\"")

except Exception as error:
    print(f"❌ FALLO TÉCNICO DETECTADO: {type(error).__name__} - {error}")
