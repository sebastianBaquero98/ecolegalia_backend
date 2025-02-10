from crewai import Task, Agent


class LegalEnvironmentTasks():
    def __init__(self, job_id:str):
        self.job_id = job_id

    def tarea_super(self, agent: Agent, pregunta: str):
        return Task(
            description=f"""Realiza una investigación exhaustiva y responde de manera completa y precisa a la pregunta {pregunta} siguiendo las siguientes fases:
                1. **Investigación Legal:**
                   - Investiga utilizando la normativa aplicable vigente en 2025, incluyendo (pero no limitado a) la Ley 99/93, Decretos 1076/15, 2811/74, y otras leyes, decretos y resoluciones específicas según el tema.
                   - El informe deberá incluir:
                     * Requisitos detallados.
                     * Normatividad aplicable.
                     * Pasos específicos para acceder a los formatos y trámites ambientales.
                     * Autoridades competentes y datos de contacto.
                     * Fuentes en cada sección, incluyendo enlaces a fuentes oficiales (ej. Ministerio de Ambiente y Desarrollo Sostenible, CAR, ANLA, etc.).

                2. **Revisión de Cumplimiento Normativo:**
                   - Verifica que la normatividad y los trámites ambientales sean vigentes y aplicables a la pregunta en 2025.
                   - Asegúrate de que todas las referencias normativas sean correctas, exactas y sin omisiones.

                3. **Revisión de Estructura y Calidad:**
                   - Confirma que la respuesta cumpla con los siguientes criterios mínimos de aceptación:
                     (a) Responder completamente a la pregunta {pregunta}.
                     (b) Cada sección debe incluir la fuente utilizada.       
                     (c) Presentar un marco normativo completo y vigente en 2025.
                     (d) Garantizar claridad, precisión y ausencia de ambigüedades.
                     (e) NO incluir disclaimers ni recomendaciones de contactar a expertos o mencionar que el proceso requiere conocimientos especializados.""",
            expected_output="""Una respuesta final **sin hipotéticos** en formato markdown que incluya:
                    - Un informe detallado y completo basado en la normativa vigente en 2025, conteniendo:
                        * Requisitos detallados.
                        * Normatividad aplicable y vigente.
                        * Pasos detallados para acceder a formatos y trámites ambientales.
                        * Autoridades competentes y datos de contacto.
                        * Fuentes en cada sección, con enlaces a organismos oficiales.
                    - Una validación que demuestre que la información legal y los trámites ambientales son actuales y correctos.
                    - Una estructura final que cumpla con los criterios mínimos de aceptación, presentando la información de forma clara, precisa y sin ambigüedades.""",
            agent=agent     
        )
    
    #def tarea_investigacion(self, agent: Agent, pregunta: str):
    #    return Task(
    #        description=f"""INSTRUCCIONES:
    #1. Investiga exhaustivamente y responde de manera completa y precisa a la pregunta: {pregunta}
    #2. Incluye en tu respuesta:
    #   - Requisitos detallados.
    #   - Normativa aplicable (Ley 99/93, Decretos 1076/15, 2811/74, y otras específicas según el tema).
    #   - Autoridades competentes y sus funciones.
    #   - Procedimientos (virtuales y presenciales).
    #   - Menciona los pasos detallados para acceder a los formatos oficiales
    #   - Datos de contacto de las autoridades competentes (dirección, teléfono, correo, página web).
    #   - Referencias a normas y fuentes oficiales.
    #   - En caso de requerir una licencia o permiso, incluir:
    #     * Enlace directo a los términos de referencia.
    #     * Pasos para diligenciar el formato necesario.""",
    #        expected_output="""Un informe detallado""",
    #        agent=agent     
    #    )
#
    #def tarea_revision_legal(self, agent: Agent):
    #    return Task(
    #        description=f"""INSTRUCCIONES:
    #        El año actual es 2025
    #        Revisa cuidadosamente que la respuesta cumpla con lo siguiente:
    #        1. Que la información legal esté vigente en el año actual.
    #        2. Que las referencias normativas sean correctas.
    #        3. Inclusión de todos los requisitos esenciales según la pregunta y normativa.
    #        4. Corrección de información desactualizada o errónea.""",
    #        expected_output="""- Respuesta corregida, con normas y requisitos vigentes en el año actual
    #- Referencias normativas exactas, completas y sin omisiones.""",
    #        agent=agent     
    #    )
#
    #def tarea_estructura(self, agent: Agent, pregunta: str):
    #    return Task(
    #        description=f"""INSTRUCCIONES:
    #1. Revisa la respuesta validada para garantizar que cumpla con los criterios mínimos de aceptación.
    #2. Agrega información o enlaces si falta algo importante.
    #3. Asegura claridad, precisión y ausencia de ambigüedades.
    #4. Asegúrate de que los enlaces funcionen y remitan a la fuente correcta.
    #5. NO incluyas disclaimers. No hagas recomendaciones de contactar a expertos ni mencionar que el proceso requiere conocimientos especializados. Tu objetivo es proporcionar información precisa, actualizada y completa según los criterios mínimos.
    #  **Criterios mínimos de aceptación:**
    #   - (1) Responder la pregunta {pregunta} con completitud.
    #   - (2) Cada sección debe tener la fuente usada con título y enlace válido.
    #   - (3) Proveer enlaces directos y pasos detallados para acceder a formatos oficiales.
    #   - (4) Para licencias ambientales o permisos, incluir enlace directo a los términos de referencia y pasos específicos.
    #   - (5) Presentar marco normativo completo (normas y artículos relevantes).""",
    #        expected_output="""-- Respuesta final en formato markdown valido:
    #  * Integre la validación legal.
    #  * Cumpla con los criterios mínimos de aceptación.
    #  * Sea perfectamente clara, con fuentes y enlaces correctos.
    #  * NO incluya descargo de responsabilidad o recomendaciones de consultar directamente la autoridad pertinente. TU ERES EXPERTO y fuente pertinente y oficial""",
    #        agent=agent     
    #    )
    
    def tarea_super_mensajes(self, agent: Agent, chat_history:str, pregunta: str):
        return Task(
            description=f"""El año actual es el 2025.
            Haces parte de un agente conversacional. Siempre como primer paso usa el historial
            del chat {chat_history} para contextualizarte y después
            investiga exhaustivamente y responde de manera completa
            y precisa a esta pregunta: {pregunta} sustentado en una
            normatividad vigente en 2025 aplicable (Ley 99/93,
            Decretos 1076/15, 2811/74, y otras leyes, decretos y resoluciones específicas según el tema).Revisa cuidadosamente que la respuesta cumpla con lo siguiente:
                1. Que la información legal esté vigente en el año 2025.
                2. Que las referencias normativas sean correctas.
                3. Inclusión de todos los requisitos esenciales según la pregunta y normativa.
                4. Corrección de información desactualizada o errónea.""",
            expected_output="""Un respuesta completa que responda la pregunta "{pregunta}" de forma puntal. Al final una sección con las fuentes. Todo formato markdown.""",
            agent=agent
        )
    
    #def tarea_revision_legal_messages(self, agent: Agent, pregunta:str):
    #    return Task(
    #        description=f"""INSTRUCCIONES:
    #            Revisa cuidadosamente que la respuesta cumpla con lo siguiente:
    #            1. Que la información legal esté vigente en el año 2025.
    #            2. Que las referencias normativas sean correctas.
    #            3. Inclusión de todos los requisitos esenciales según la pregunta y normativa.
    #            4. Corrección de información desactualizada o errónea.""",
    #            #expected_output="Respuesta corregida y con normas y requisitos vigentes en 2025. Referencias normativas exactas, completas y sin omisiones.",
    #            expected_output=f'Respuesta corregida y completa que responda la pregunta "{pregunta}" de forma puntal. Al final una sección con las fuentes. Todo formato markdown.',
    #        agent=agent
    #    )