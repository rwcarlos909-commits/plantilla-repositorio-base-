# Decisión de Arquitectura: Elección de Modelo de Lenguaje 

## Modelo Elegido 
**`openai/gpt-oss-20b`** (vía API de Groq) para el asistente de vinculación educativa y laboral técnica en zonas rurales de la Región de Valparaíso. 

## Diagrama de Arquitectura 
![Diagrama de Arquitectura](diagrama-arquitectura.png) 

El flujo se inicia cuando el usuario consulta por cursos presenciales o recursos locales. La función `armar_peticion()` estructura el prompt, `enviar_peticion()` realiza la llamada HTTPS hacia la API de Groq enrutada al modelo `openai/gpt-oss-20b`, y `extraer\_texto()\` entrega la respuesta formateada al usuario. 

## Comparación de Candidatos | Criterio | Modelo A (\`openai/gpt-oss-120b\`) | Modelo B (\`openai/gpt-oss-20b\`) | 
| :--- | :--- | :--- | 
| \*\*Costo por 1000 tokens de entrada\*\* | $0.000150 USD | $0.000075 USD | 
| \*\*Costo por 1000 tokens de salida\*\* | $0.000600 USD | $0.000300 USD | 
| \*\*Latencia promedio observada\*\* | 2.07 segundos | 1.28 segundos | 
| \*\*Calidad de respuesta para el caso\*\* | Muy detallada y extensa | Concisa, estructurada y precisa para datos de contacto y ubicación | 
| \*\*Fecha de medición\*\* | 2026-10-26 | 2026-10-26 | 

## Justificación 
Se selecciona el \*\*Modelo B (\`openai/gpt-oss-20b\`)\*\* debido a que ofrece el equilibrio óptimo dentro del triángulo de arquitectura (Costo, Latencia y Calidad) para nuestro caso de uso. Al orientarse a usuarios de zonas rurales e interiores de la Región de Valparaíso, una latencia reducida a \*\*1.28 segundos\*\* es crítica para compensar la conectividad móvil limitada. Además, reduce el costo operativo por petición a la mitad ($0.000227 USD), garantizando la viabilidad económica del proyecto a escala sin sacrificar la claridad en la entrega de información técnica y geográfica. 

## Alternativa Descartada y Por Qué 
Se descarta el \*\*Modelo A (\`openai/gpt-oss-120b\`)\*\*. A pesar de ofrecer una mayor profundidad de razonamiento y respuestas más extensas, su latencia promedio (2.07 s) y su costo por consulta duplicado no se justifican para las necesidades de consulta estructurada de esta aplicación.
