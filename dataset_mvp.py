# ==============================================================================
# DATASET DE EVALUACIÓN MVP: Vinculación Educación-Trabajo (Quinta Región)
# Archivo: dataset_mvp.py (Ubicado en la raíz del proyecto)
# ==============================================================================

DATASET_EVALUACION_MVP = [
    # --------------------------------------------------------------------------
    # EJE 1: Mallas y Especialidades Técnico-Profesionales (TP)
    # --------------------------------------------------------------------------

    {
        "id": 1,
        "categoria": "Mallas TP",
        "pregunta": "¿Qué especialidades técnico-profesionales son tradicionales en los liceos industriales de la Quinta Región?",
        "referencia_oro": "Las especialidades tradicionales incluyen Mecánica Industrial, Electricidad, Metalmecánica y Minería.",
        "palabras_obligatorias": ["mecanica", "electricidad"]
    },
    {
        "id": 2,
        "categoria": "Mallas TP",
        "pregunta": "¿Cuál es el perfil de egreso de la especialidad de Explotación Minera en liceos técnicos del interior?",
        "referencia_oro": "El egresado opera equipos mineros, aplica normas de seguridad, prevención de riesgos y extracción sustentable.",
        "palabras_obligatorias": ["mineros", "seguridad"]
    },
    {
        "id": 3,
        "categoria": "Mallas TP",
        "pregunta": "¿Qué competencias agroindustriales se enseñan en liceos agrícolas de Quillota y Marga Marga?",
        "referencia_oro": "Se enseña riego tecnificado, manejo integrado de plagas, procesamiento de alimentos y empaque de exportación.",
        "palabras_obligatorias": ["riego", "alimentos"]
    },
    {
        "id": 4,
        "categoria": "Mallas TP",
        "pregunta": "¿Cómo se vincula la especialidad de Contabilidad y Administración con la gestión municipal local?",
        "referencia_oro": "Capacita en legislación laboral, presupuestos públicos, tramitación tributaria y soporte administrativo comunal.",
        "palabras_obligatorias": ["presupuestos", "administracion"]
    },
    {
        "id": 5,
        "categoria": "Mallas TP",
        "pregunta": "¿Qué módulos de automatización e hidráulica se incorporan en la especialidad de Mecánica Automotriz?",
        "referencia_oro": "Diagnóstico electrónico, lectura de escáner, sistemas oleohidráulicos y mantenimiento preventivo vehicular.",
        "palabras_obligatorias": ["diagnostico", "mantenimiento"]
    },

    # --------------------------------------------------------------------------
    # EJE 2: Demanda Laboral y Tendencias Comunales (Hub V21, Agricultura 5.0, Servicios)
    # --------------------------------------------------------------------------

    {
        "id": 6,
        "categoria": "Demanda Laboral",
        "pregunta": "¿Qué competencias demanda el ecosistema de innovación del Hub V21 en El Salto, Viña del Mar?",
        "referencia_oro": "Demanda analítica de datos, programación en Python, visión por computador, internet de las cosas y automatización.",
        "palabras_obligatorias": ["datos", "python"]
    },
    {
        "id": 7,
        "categoria": "Demanda Laboral",
        "pregunta": "¿Qué requerimientos técnicos exige la Agricultura 5.0 en los valles del interior de la región?",
        "referencia_oro": "Monitoreo por sensores de humedad, procesamiento de datos climáticos, drones y optimización del uso hídrico.",
        "palabras_obligatorias": ["sensores", "hidrico"]
    },
    {
        "id": 8,
        "categoria": "Demanda Laboral",
        "pregunta": "¿Cuáles son las necesidades de capital humano en el sector logístico portuario de Valparaíso?",
        "referencia_oro": "Operación de grúas, gestión de inventarios digitales, despacho aduanero y seguridad portuaria.",
        "palabras_obligatorias": ["inventarios", "aduanero"]
    },
    {
        "id": 9,
        "categoria": "Demanda Laboral",
        "pregunta": "¿Qué perfil de mantenimiento requiere la industria de alimentos y agroprocesamiento en la zona?",
        "referencia_oro": "Mantenimiento de líneas de envasado, control de calidad e inocuidad alimentaria bajo norma HACCP.",
        "palabras_obligatorias": ["mantenimiento", "inocuidad"]
    },
    {
        "id": 10,
        "categoria": "Demanda Laboral",
        "pregunta": "¿Qué habilidades digitales básicas solicitan los municipios para cargos de atención y análisis territorial?",
        "referencia_oro": "Manejo de planillas de cálculo Excel, bases de datos SQL, redacción técnica e intermediación social.",
        "palabras_obligatorias": ["excel", "datos"]
    },

    # --------------------------------------------------------------------------
    # EJE 3: Caracterización Socio-Demográfica y Brechas Comunales
    # --------------------------------------------------------------------------

    {
        "id": 11,
        "categoria": "Caracterización Demográfica",
        "pregunta": "¿Cuáles son los principales desafíos de inserción laboral juvenil en Placilla y Curauma?",
        "referencia_oro": "Falta de transporte directo a zonas industriales, descalce entre la oferta académica y la demanda tecnológica local.",
        "palabras_obligatorias": ["transporte", "descalce"]
    },
    {
        "id": 12,
        "categoria": "Caracterización Demográfica",
        "pregunta": "¿Cómo impacta la escasez hídrica en la empleabilidad rural de la provincia de Petorca?",
        "referencia_oro": "Reduce los empleos agrícolas de temporada y fuerza la reconversión laboral hacia servicios y minería no metálica.",
        "palabras_obligatorias": ["agricolas", "reconversion"]
    },
    {
        "id": 13,
        "categoria": "Caracterización Demográfica",
        "pregunta": "¿Qué barreras enfrentan las egresadas de liceos TP para ingresar a especialidades de tecnología e industria?",
        "referencia_oro": "Sesgos de género en contratación, falta de salas acondicionadas y menor difusión de becas STEM.",
        "palabras_obligatorias": ["sesgos", "stem"]
    },
    {
        "id": 14,
        "categoria": "Caracterización Demográfica",
        "pregunta": "¿Qué índice de vulnerabilidad social predomina en los liceos científico-humanistas de la periferia de Valparaíso?",
        "referencia_oro": "Presentan un Índice de Vulnerabilidad Escolar superior al ochenta por ciento, requiriendo articulación con el SENCE.",
        "palabras_obligatorias": ["vulnerabilidad", "sence"]
    },
    {
        "id": 15,
        "categoria": "Caracterización Demográfica",
        "pregunta": "¿Cuál es la principal vía de empleabilidad para jóvenes de liceos TP en la comuna de San Antonio?",
        "referencia_oro": "La logística de transporte de carga terrestre, el almacenamiento de contenedores y agencias marítimas.",
        "palabras_obligatorias": ["transporte", "logistica"]
    },

    # --------------------------------------------------------------------------
    # EJE 4: Articulación Educativo-Laboral y Políticas Públicas (AIEP, SLEP, SENCE)
    # --------------------------------------------------------------------------

    {
        "id": 16,
        "categoria": "Articulación Educativa",
        "pregunta": "¿Cómo beneficia la convalidación de ramos entre liceos TP e institutos técnicos como AIEP a los estudiantes?",
        "referencia_oro": "Acorta la duración de la carrera técnica superior, reduce los costos de arancel y reconoce aprendizajes previos.",
        "palabras_obligatorias": ["duracion", "reconoce"]
    },
    {
        "id": 17,
        "categoria": "Articulación Educativa",
        "pregunta": "¿Qué rol cumplen los Servicios Locales de Educación Pública en la actualización de equipos e insumos de taller?",
        "referencia_oro": "Gestionan fondos del Ministerio de Educación para equipamiento industrial, convenios con empresas y capacitación docente.",
        "palabras_obligatorias": ["fondos", "capacitacion"]
    },
    {"id": 18,
     "categoria": "Articulación Educativa",
     "pregunta": "¿Qué ventajas ofrece el modelo de Formación Dual en empresas metalmecánicas y de servicios?",
     "referencia_oro": "Permite al estudiante alternar días de clase en el liceo con práctica directa supervisada en la planta productiva.",
     "palabras_obligatorias": ["alternar", "practica"]

     },
    {
        "id": 19,
        "categoria": "Articulación Educativa",
        "pregunta": "¿Cómo apoya la franquicia tributaria del SENCE a la capacitación continua de operarios en la región?",
        "referencia_oro": "Financia cursos de perfeccionamiento técnico para trabajadores mediante franquicia tributaria impulsada por las empresas.",
        "palabras_obligatorias": ["cursos", "franquicia"]
    },
    {
        "id": 20,
        "categoria": "Articulación Educativa",
        "pregunta": "¿De qué manera el Análisis de Datos puede optimizar la oferta formativa de un municipio?",
        "referencia_oro": "Cruza vacantes de empleo en tiempo real con egresados de liceos para detectar brechas de competencias y ajustar la malla.",
        "palabras_obligatorias": ["vacantes", "brechas"]
    }
]
