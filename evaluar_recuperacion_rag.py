# ==============================================================================
# BLOQUE 27: EVALUACIÓN CUANTITATIVA DE RECUPERACIÓN (PRECISIÓN, RECALL Y F1)
# ==============================================================================
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# ------------------------------------------------------------------------------
# 1. Carga de Variables de Entorno y Validación
# ------------------------------------------------------------------------------
load_dotenv()
if not os.environ.get("GEMINI_API_KEY"):
    raise SystemExit("❌ ERROR: Falta GEMINI_API_KEY en tu archivo .env")

# ------------------------------------------------------------------------------
# 2. Conexión al Vector Store Persistido en Disco
# ------------------------------------------------------------------------------
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma(
    persist_directory="vectorstore/",
    embedding_function=embeddings
)

# ------------------------------------------------------------------------------
# 3. Funciones Matemáticas de Evaluación (Python Puro)
# ------------------------------------------------------------------------------


def precision_at_k(aciertos: int, k: int) -> float:
    """Calcula la proporción de fragmentos útiles dentro de los k recuperados."""
    if k == 0:
        return 0.0
    return aciertos / k


def recall_at_k(aciertos: int, total_relevantes: int) -> float:
    """Calcula la proporción de relevantes recuperados respecto al total esperado."""
    if total_relevantes == 0:
        return 0.0
    return aciertos / total_relevantes


def f1_score(precision: float, recall: float) -> float:
    """Media armónica entre precisión y recall para medir equilibrio."""
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)


# ------------------------------------------------------------------------------
# 4. Conjunto de Evaluación Etiquetado (4 Casos de Prueba)
# ------------------------------------------------------------------------------
casos_evaluacion = [
    {"pregunta": "¿Qué hace el cliente si una llamada tarda demasiado?",
        "termino_clave": "TimeoutError"},
    {"pregunta": "¿Qué ocurre con los errores de autenticación?",
        "termino_clave": "autenticación"},
    {"pregunta": "¿Cómo se calcula el costo de una llamada?",
        "termino_clave": "totalTokenCount"},
    {"pregunta": "¿Cómo decide el agente qué herramienta usar?",
        "termino_clave": "agente"}
]

# ------------------------------------------------------------------------------
# 5. Ejecución del Experimento de Evaluación
# ---------------------------------------------


def evaluar_retriever(k: int = 3):
    print("\n==================================================================")
    print(f"📊 EVALUACIÓN DE RECUPERACIÓN RAG CON CHROMA (k={k})")
    print("==================================================================")

    precisiones = []
    recalls = []

    for idx, caso in enumerate(casos_evaluacion, start=1):
        pregunta = caso["pregunta"]
        clave = caso["termino_clave"]

        # Inferencia real sobre ChromaDB
        documentos = vectorstore.similarity_search(pregunta, k=k)

        # Verificamos cuántos de los k chunks recuperados contienen la información clave
        aciertos = sum(1 for doc in documentos if clave.lower()
                       in doc.page_content.lower())

        p = precision_at_k(aciertos, k)
        r = recall_at_k(1 if aciertos > 0 else 0, total_relevantes=1)
        f1 = f1_score(p, r)

        precisiones.append(p)
        recalls.append(r)

        print(
            f"Caso {idx}: P@{k}={p:.2f} | R@{k}={r:.2f} | F1={f1:.2f} | Pregunta: '{pregunta[:42]}...'")

    p_prom = sum(precisiones) / len(precisiones)
    r_prom = sum(recalls) / len(recalls)
    f1_prom = f1_score(p_prom, r_prom)

    print("\n------------------------------------------------------------------")
    print(f"📈 PROMEDIOS EVALUADOS (k={k}):")
    print(f" • Precisión Promedio (P@{k}): {p_prom:.3f}")
    print(f" • Recall Promedio (R@{k}): {r_prom:.3f}")
    print(f" • F1-Score Promedio: {f1_prom:.3f}")
    print("------------------------------------------------------------------")


if __name__ == "__main__":
    evaluar_retriever(k=3)
