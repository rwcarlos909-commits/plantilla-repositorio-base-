import time
from consumir_groq import armar_peticion, enviar_peticion

pregunta = "¿Cuál es la capital de Alemania?"
url, headers, body = armar_peticion(pregunta)

inicio = time.perf_counter()
respuesta_json = enviar_peticion(url, headers, body)
fin = time.perf_counter()

latencia = fin - inicio
print(f"Latencia: {latencia:.2f} segundos")
