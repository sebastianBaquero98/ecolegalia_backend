from crewai import Task, Agent


class LegalEnvironmentTasks():
    def __init__(self, job_id:str):
        self.job_id = job_id
    
    def tarea_investigacion(self, agent: Agent, pregunta: str):
        return Task(
            description=f"""INSTRUCCIONES DE INVESTIGACIÓN JURÍDICA AMBIENTAL

            PREGUNTA A RESPONDER: «{pregunta}»

            EJECUTA ESTE PROTOCOLO DE INVESTIGACIÓN EXHAUSTIVA:

            1. PLANIFICACIÓN:
            <plan>
            - Identifica los conceptos jurídicos clave en la pregunta
            - Determina la jerarquía normativa aplicable
            - Establece estrategia de búsqueda usando primero la base de datos legal interna y luego fuentes web oficiales
            </plan>

            2. CONSULTA PRIORITARIA A BASE DE DATOS LEGAL INTERNA:
            - ESTE ES EL PRIMER PASO OBLIGATORIO: Consulta la base de datos vectorial legal interna.
            - Formula una consulta precisa relacionada con la pregunta.
            - Aplica filtros de metadata cuando sea pertinente:
              * tipo_acto: Auto, Concepto, Decreto, Anexo, Formato, Guía
              * año: año de emisión del documento
              * nombre: nombre específico del documento (si lo conoces)
            - Si los primeros resultados no son relevantes:
              * Reformula la consulta con términos más específicos
              * Aplica diferentes filtros de metadata
              * Aumenta el número de resultados (top_k)
            - Extrae y documenta la información relevante de los documentos recuperados

            3. INVESTIGACIÓN PRIMARIA (MARCO NORMATIVO):
            - Constitución: Arts. 8, 49, 58, 63, 79, 80, 81, 82, 95, 330
            - Ley 99/1993 (SINA): Busca artículos específicos para el caso
            - Ley 1333/2009 (Sancionatorio Ambiental): Si aplica
            - Decreto-Ley 2811/1974 (Código RN): Secciones aplicables
            - Decreto 1076/2015 (Decreto Único Ambiental): Normativa compilada
            - Resoluciones específicas por sector:
                * Agua: 631/2015, 883/2018, etc.
                * Aire: 909/2008, 910/2008, etc.
                * Biodiversidad: 1912/2017, etc.
                * Residuos: 1362/2007, etc.
            - Normativa específica de la autoridad ambiental regional mencionada
            - Acuerdos/determinantes ambientales territoriales

            4. INVESTIGACIÓN PROCEDIMENTAL:
            - Identificación de trámites específicos (SUIT/VITAL)
            - Términos de referencia (TR) actualizados
            - Formatos y formularios oficiales vigentes
            - Guías técnicas actualizadas (MinAmbiente/ANLA)
            - Tarifas y costos actualizados (VITAL/ANLA/CAR)
            - Procedimientos virtuales y presenciales
            - Directorio de autoridades competentes
            - Jurisdicciones específicas territoriales

            5. CONTROL DE CALIDAD (OBLIGATORIO):
            Para CADA norma o procedimiento identificado, verifica y documenta:
            - Existencia: URL oficial directa al texto normativo
            - Vigencia: Estatus actual según repositorios oficiales
            - Aplicabilidad: Pertinencia específica al caso consultado
            - Extracto textual: Transcripción exacta del fragmento relevante

            6. PRESENTACIÓN DE HALLAZGOS:
            Para cada elemento normativo o procedimental:
            - Identificación: [Tipo, número, fecha, autoridad emisora]
            - Transcripción: "Extracto textual entrecomillado"
            - Fuente: URL directa a documento oficial
            - Relevancia: Explicación concisa de aplicabilidad al caso
            - Estatus: [VIGENTE/DEROGADO/MODIFICADO]

            7. AUTOVERIFICACIÓN ANTI-ALUCINACIÓN:
            - Revisa cada afirmación contra fuentes oficiales
            - Marca con [❓] cualquier dato sin respaldo documental directo
            - Ejecuta verificación cruzada de consistencia interna

            PROHIBIDO: Avanzar sin verificación completa; inventar normas o procedimientos; omitir fuentes directas; proporcionar información desactualizada.

            RESPONDE UTILIZANDO ESTE ESQUEMA EXACTO:
            
            ## RESULTADOS DE INVESTIGACIÓN NORMATIVA

            ### 1. Consulta a Base de Datos Legal Interna
            [Detalle de consultas realizadas y resultados obtenidos]

            ### 2. Marco Jurídico Aplicable
            [Lista detallada de normas verificadas]

            ### 3. Requisitos y Procedimientos
            [Enumeración detallada de requisitos y pasos]

            ### 4. Autoridades Competentes
            [Autoridades con jurisdicción y datos de contacto]

            ### 5. Documentación Requerida
            [Formatos, estudios y soportes necesarios]

            ### 6. Verificación de Fuentes
            [Registro de todas las fuentes consultadas]
            """,
            expected_output="""Un informe jurídico exhaustivo en formato Markdown que incluya:
                            - Resultados de la consulta a la base de datos legal interna
                            - Marco normativo completo y verificado
                            - Requisitos detallados y procedimientos paso a paso
                            - Autoridades competentes con datos de contacto
                            - Enlaces directos a formatos oficiales y normativa
                            - Registro de verificación de fuentes
                            - CERO afirmaciones sin respaldo documental""",
            agent=agent     
        )

    def tarea_revision_legal(self, agent: Agent):
        return Task(
            description="""INSTRUCCIONES DE AUDITORÍA FORENSE NORMATIVA

            EJECUTA ESTE PROTOCOLO DE VERIFICACIÓN EXHAUSTIVA:

            1. EXTRACCIÓN PRECISA DE REFERENCIAS:
            <plan>
            - Identifica y extrae TODAS las referencias normativas del informe
            - Clasifica por jerarquía y tipología normativa
            - Crea registro estructurado para auditoría
            </plan>

            2. VERIFICACIÓN EN BASE DE DATOS LEGAL INTERNA:
            - Para cada norma identificada, verifica primero en la base de datos legal interna:
              * Usa filtros precisos (tipo_acto, año, nombre si está disponible)
              * Compara textualmente los fragmentos citados con los originales
              * Documenta la correspondencia o discrepancia

            3. VERIFICACIÓN DE AUTENTICIDAD MULTI-FUENTE:
            Para CADA norma identificada, verifica en estas fuentes oficiales:
            
            a) SUIN-Juriscol (https://www.suin-juriscol.gov.co/):
                - Existencia del texto normativo oficial
                - Estado de vigencia actualizado
                - Historial de modificaciones
            
            b) Gestor Normativo Función Pública (https://www.funcionpublica.gov.co/web/gestor-normativo):
                - Vigencia actual
                - Notas de derogatoria o modificación
                - Referencias cruzadas
            
            c) Diario Oficial (http://svrpubindc.imprenta.gov.co/diario/):
                - Verificación de publicación original
                - Texto auténtico primario
            
            d) Normogramas Oficiales:
                - MinAmbiente (https://www.minambiente.gov.co/)
                - ANLA (https://www.anla.gov.co/)
                - CAR específica mencionada en la consulta

            4. ANÁLISIS FORENSE DE TEXTO NORMATIVO:
            Para cada cita o extracto normativo mencionado:
            - Copia el texto exacto de la fuente oficial
            - Compara palabra por palabra con el texto citado
            - Registra cualquier discrepancia, omisión o adición

            5. VALIDACIÓN DE CADENA NORMATIVA:
            - Verifica la jerarquía completa:
                * ¿La norma reglamentaria citada desarrolla correctamente la ley marco?
                * ¿Las resoluciones citadas implementan correctamente los decretos?
                * ¿Existen vacíos en la cadena de desarrollo normativo?
            - Registra cualquier inconsistencia jerárquica

            6. VERIFICACIÓN DE APLICABILIDAD:
            - Competencia territorial: ¿La autoridad citada tiene jurisdicción?
            - Competencia material: ¿La norma regula específicamente la materia consultada?
            - Vigencia temporal: ¿Aplica al año 2025 o está derogada/modificada?

            7. DOCUMENTACIÓN DE HALLAZGOS:
            Para cada norma verificada, genera este registro forense:
            ```json
            {
                "norma": "[Tipo, número, año]",
                "vigencia": "[VIGENTE/DEROGADA/MODIFICADA]",
                "verificacion_textual": "[COINCIDE/NO COINCIDE]",
                "verificacion_interna": "[ENCONTRADA/NO ENCONTRADA] en base de datos legal",
                "fuentes_verificacion": ["URL1", "URL2", "URL3"],
                "observaciones": "[Hallazgos detallados]",
                "recomendacion": "[MANTENER/CORREGIR/ELIMINAR]"
            }
            ```

            8. DICTAMEN FINAL DE VERIFICACIÓN:
            - Generar informe ejecutivo de cumplimiento normativo
            - Clasificar cada referencia como: ✅ VERIFICADA, ⚠️ PARCIAL, ❌ NO VERIFICADA
            - Proporcionar recomendaciones específicas de corrección

            NORMAS ANTI-ALUCINACIÓN:
            - Si una norma no puede verificarse tras dos intentos en fuentes oficiales, márquela explícitamente como NO VERIFICADA
            - Documenta el proceso de búsqueda fallido con evidencias
            - Nunca asumas la existencia o vigencia de una norma sin verificación directa
            - Si encuentras contradicciones entre fuentes oficiales, regístralas explícitamente
            """,
            expected_output="""Un informe forense de verificación normativa en formato Markdown que incluya:
                            - Registro de verificación en base de datos legal interna
                            - Registro detallado de la verificación de cada norma
                            - Dictamen de autenticidad y vigencia de cada referencia
                            - Recomendaciones específicas de corrección
                            - Evidencia documental de cada verificación
                            - Clasificación final de confiabilidad normativa""",
            agent=agent     
        )
    
    def tarea_estructura(self, agent: Agent, pregunta: str):
        return Task(
            description=f"""INSTRUCCIONES DE ESTRUCTURACIÓN Y REDACCIÓN FINAL

            PREGUNTA ORIGINAL: «{pregunta}»

            EJECUTA ESTE PROTOCOLO DE ESTRUCTURACIÓN Y COMUNICACIÓN:

            1. PLANIFICACIÓN DE ESTRUCTURA:
            <plan>
            - Evalúa la integridad de la información jurídica verificada
            - Identifica la estructura óptima para responder la consulta específica
            - Determina jerarquía informativa: esencial → complementario
            </plan>

            2. VERIFICACIÓN DE COMPLETITUD:
            Confirma que la respuesta incluya TODOS estos elementos:
            - ✓ Marco normativo completo y actualizado
            - ✓ Requisitos detallados y específicos
            - ✓ Procedimiento paso a paso (virtual y presencial)
            - ✓ Formatos oficiales con enlaces directos de descarga
            - ✓ Autoridades competentes con datos actualizados
            - ✓ Referencias precisas a fuentes oficiales
            - ✓ Costos y tiempos de trámite (cuando aplique)

            3. TRANSFORMACIÓN A LENGUAJE CLARO:
            - Simplifica terminología jurídica sin sacrificar precisión técnica
            - Convierte construcciones pasivas a activas
            - Sustituye lenguaje abstracto por concreto y específico
            - Estructura oraciones simples (sujeto + verbo + complemento)
            - Elimina redundancias y circunloquios
            - Utiliza voz activa e imperativa para instrucciones

            4. ESTRUCTURACIÓN VISUAL OPTIMIZADA:
            - Implementa jerarquía visual con encabezados Markdown (# ## ###)
            - Utiliza listas numeradas para procedimientos secuenciales
            - Crea tablas para información comparativa o multi-elemento
            - Emplea listas con viñetas para requisitos y documentos
            - Destaca información crítica con **negritas** o *cursivas*
            - Incluye enlaces como [texto descriptivo](URL)

            5. VERIFICACIÓN DE ACCESIBILIDAD:
            - Evalúa legibilidad (Flesch-Kincaid < 70)
            - Verifica que no existan ambigüedades o zonas grises
            - Confirma que cada procedimiento sea accionable
            - Asegura que los contactos y enlaces estén actualizados
            - Comprueba que la respuesta sea autocontenida

            6. REVISIÓN ANTI-AMBIGÜEDAD:
            - Identifica y elimina cualquier ambigüedad normativa o procedimental
            - Específica exactamente QUÉ, QUIÉN, CÓMO, DÓNDE y CUÁNDO
            - Esclarece cualquier posible interpretación divergente
            - Añade ejemplos concretos cuando sea necesario para clarificar

            7. AUTOVERIFICACIÓN FINAL:
            Confirma que la respuesta:
            - ✓ Responde completamente a la pregunta original
            - ✓ Proporciona información 100% verificada y precisa
            - ✓ No contiene disclaimers ni sugerencias de consultar expertos
            - ✓ Presenta información de forma clara y comprensible
            - ✓ Incluye únicamente información verificada y actualizada
            - ✓ Está estructurada óptimamente para facilitar comprensión

            ESTRUCTURA DE RESPUESTA FINAL:

            # Respuesta: {pregunta}

            ## Resumen Ejecutivo
            [Síntesis clara y concisa de la respuesta]

            ## Marco Normativo Aplicable
            [Normas verificadas con citas y enlaces]

            ## Requisitos y Documentación
            [Lista detallada de requisitos y soportes]

            ## Procedimiento Paso a Paso
            [Secuencia numerada y detallada]

            ## Autoridades Competentes
            [Información de contacto completa]

            ## Recursos Adicionales
            [Enlaces a formatos y guías oficiales]

            ## Fuentes Oficiales
            [Referencias precisas verificadas]
        
            IMPORTANTE: Tu respuesta FINAL DEBE empezar con '### FINAL_ANSWER:' seguido del texto completo en Markdown. NO hagas referencias a texto anterior o utilizando frases como "Como mencioné anteriormente" o "Como se muestra arriba". Incluye SIEMPRE el contenido completo.
            """,
            expected_output="""Una respuesta final completa en formato Markdown que comience con 'RESPUESTA_FINAL:' y que:
                            - Responda íntegramente a la pregunta original
                            - Mantenga precisión técnica con lenguaje accesible
                            - Estructura óptima para facilitar comprensión
                            - Incluya todos los elementos informativos requeridos
                            - Proporcione enlaces actualizados a fuentes oficiales
                            - Cero ambigüedades o zonas grises
                            - Información 100% verificada y actualizada""",
            agent=agent     
        )

    def tarea_super_mensajes(self, agent: Agent, chat_history:str, pregunta: str):
        return Task(
            description=f"""
                Año de referencia: 2025.

                1. **Revisión del Historial de Chat**  
                   - **PRIMERO:** Lee detenidamente el historial completo del chat:  
                     "{chat_history}"  
                   - **EXTRAE:** Resume los puntos clave y el contexto relevante del historial para asegurarte de comprender toda la información previa que pueda influir en la respuesta.

                2. **Investigación y Respuesta Normativa**  
                   - Investiga exhaustivamente la normatividad vigente utilizando PRIMERO la base de datos legal interna vectorizada y luego complementa con búsquedas web.
                   - Consulta la base de datos legal interna utilizando filtros de metadata cuando sea relevante.
                   - Verifica la información en fuentes oficiales como la Ley 99/93, Decretos 1076/15, 2811/74 y cualquier otra norma aplicable al año 2025.
                   - Elabora una respuesta completa, precisa y detallada que únicamente responde a la siguiente pregunta:
                     "{pregunta}" en el contexto del chat
                   - Asegúrate de que la respuesta cumpla estrictamente con:
                     - La inclusión de referencias normativas correctas y vigentes.
                     - La integración de todos los requisitos esenciales que plantea la pregunta y la normativa.
                     - La corrección de cualquier información desactualizada o errónea.

                3. **Formato y Fuentes**  
                   - Redacta la respuesta en formato Markdown.
                   - Al final de la respuesta, incluye una sección titulada "Fuentes" en la que cites todas las referencias normativas utilizadas.

                **IMPORTANTE:** No omitas la etapa de análisis del historial de chat. Este contexto es fundamental para contextualizar y personalizar adecuadamente la respuesta a la pregunta.

                """,
            expected_output="""- Un breve resumen del contexto extraído del historial del chat (Una frase máximo).- Una respuesta completa y precisa a la pregunta: "{pregunta}".
            - Una sección final titulada "Fuentes" con todas las referencias normativas en *formato Markdown.*""",
            agent=agent
        )