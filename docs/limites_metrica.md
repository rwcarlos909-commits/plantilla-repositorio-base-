### Límites de la métrica de evaluación

#### Qué mide
La métrica evalúa la coincidencia token a token entre la salida del modelo y la
Referencia de Oro normalizada mediante el pipeline de texto, midiendo Precisión,
Cobertura (Recall) y F1-Score, complementado por un filtro cualitativo no
compensable (Gate 1).

#### Modos de falla conocidos
* **Verbosidad e información de contexto extra**: La IA suele agregar
  explicaciones completas y pedagógicas que incrementan los tokens de salida,
  reduciendo la Precisión cuantitativa sin perder corrección factual.
* **Sinónimos y variantes terminológicas locales**: Términos como "minería de
  superficie" vs "explotación minera" o "riego por goteo" vs "riego tecnificado"
  pueden ser penalizados cuantitativamente si no coinciden exactamente con la
  referencia.
* **Contradicción semántica en frases cortas**: Inversiones de sentido por
  negaciones ("no es seguro") son vetadas por el Gate 1 con score 0.0 antes de
  calcular similitudes de palabras.

#### Muestra revisada
Se revisaron a mano 10 casos (5 con el F1-Score más bajo y 5 con el más alto)
del dataset de 20 preguntas del MVP sobre vinculación educación-trabajo en la
Quinta Región.

#### Recomendación de uso
Confiar en la métrica automática para monitoreo continuo de regresiones y
cumplimiento de formato/palabras clave (Gate 1). Se recomienda auditar a mano
las salidas cuando el F1-Score se ubique entre 0.30 y 0.60 para verificar si la
caída en precisión se debe a verbosidad informativa o a errores factuales
reales.
