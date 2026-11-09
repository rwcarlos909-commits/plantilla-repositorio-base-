# Script de registro manual generado automáticamente
import json

revision_manual = [
  {
    "id": 1,
    "consulta": "¿Qué especialidades técnico-profesionales son tradicionales en los liceos industriales de la Quinta Región?",
    "f1": 0.0,
    "correccion_factual": "no",
    "completitud": "no",
    "contradiccion": "si",
    "nota": "Evaluado en Gate 1 como RECHAZADO_GATE1. Falta palabra clave obligatoria exigida por el negocio: 'mecanica'."
  },
  {
    "id": 2,
    "consulta": "¿Cuál es el perfil de egreso de la especialidad de Explotación Minera en liceos técnicos del interior?",
    "f1": 0.0,
    "correccion_factual": "no",
    "completitud": "no",
    "contradiccion": "si",
    "nota": "Evaluado en Gate 1 como RECHAZADO_GATE1. Falta palabra clave obligatoria exigida por el negocio: 'mineros'."
  },
  {
    "id": 3,
    "consulta": "¿Qué competencias agroindustriales se enseñan en liceos agrícolas de Quillota y Marga Marga?",
    "f1": 0.0,
    "correccion_factual": "no",
    "completitud": "no",
    "contradiccion": "si",
    "nota": "Evaluado en Gate 1 como RECHAZADO_GATE1. Falta palabra clave obligatoria exigida por el negocio: 'riego'."
  },
  {
    "id": 4,
    "consulta": "¿Cómo se vincula la especialidad de Contabilidad y Administración con la gestión municipal local?",
    "f1": 0.0,
    "correccion_factual": "no",
    "completitud": "no",
    "contradiccion": "si",
    "nota": "Evaluado en Gate 1 como RECHAZADO_GATE1. Falta palabra clave obligatoria exigida por el negocio: 'presupuestos'."
  },
  {
    "id": 5,
    "consulta": "¿Qué módulos de automatización e hidráulica se incorporan en la especialidad de Mecánica Automotriz?",
    "f1": 0.0,
    "correccion_factual": "no",
    "completitud": "no",
    "contradiccion": "si",
    "nota": "Evaluado en Gate 1 como RECHAZADO_GATE1. Falta palabra clave obligatoria exigida por el negocio: 'diagnostico'."
  },
  {
    "id": 16,
    "consulta": "¿Cómo beneficia la convalidación de ramos entre liceos TP e institutos técnicos como AIEP a los estudiantes?",
    "f1": 0.0,
    "correccion_factual": "no",
    "completitud": "no",
    "contradiccion": "si",
    "nota": "Evaluado en Gate 1 como RECHAZADO_GATE1. Falta palabra clave obligatoria exigida por el negocio: 'duracion'."
  },
  {
    "id": 17,
    "consulta": "¿Qué rol cumplen los Servicios Locales de Educación Pública en la actualización de equipos e insumos de taller?",
    "f1": 0.0,
    "correccion_factual": "no",
    "completitud": "no",
    "contradiccion": "si",
    "nota": "Evaluado en Gate 1 como RECHAZADO_GATE1. Falta palabra clave obligatoria exigida por el negocio: 'fondos'."
  },
  {
    "id": 18,
    "consulta": "¿Qué ventajas ofrece el modelo de Formación Dual en empresas metalmecánicas y de servicios?",
    "f1": 0.0,
    "correccion_factual": "no",
    "completitud": "no",
    "contradiccion": "si",
    "nota": "Evaluado en Gate 1 como RECHAZADO_GATE1. Falta palabra clave obligatoria exigida por el negocio: 'alternar'."
  },
  {
    "id": 19,
    "consulta": "¿Cómo apoya la franquicia tributaria del SENCE a la capacitación continua de operarios en la región?",
    "f1": 0.0,
    "correccion_factual": "no",
    "completitud": "no",
    "contradiccion": "si",
    "nota": "Evaluado en Gate 1 como RECHAZADO_GATE1. Falta palabra clave obligatoria exigida por el negocio: 'cursos'."
  },
  {
    "id": 20,
    "consulta": "¿De qué manera el Análisis de Datos puede optimizar la oferta formativa de un municipio?",
    "f1": 0.0,
    "correccion_factual": "no",
    "completitud": "no",
    "contradiccion": "si",
    "nota": "Evaluado en Gate 1 como RECHAZADO_GATE1. Falta palabra clave obligatoria exigida por el negocio: 'vacantes'."
  }
]

if __name__ == "__main__":
    with open("revision_manual.json", "w", encoding="utf-8") as archivo:
        json.dump(revision_manual, archivo, indent=2, ensure_ascii=False)
        print("Archivo revision_manual.json actualizado.")
