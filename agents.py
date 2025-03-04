from crewai import Agent
from crewai import LLM
from crewai_tools import SerperDevTool, WebsiteSearchTool

class LegalEnvironmentAgents():
    def __init__(self) -> None:
        self.llm = LLM(
                    model="anthropic/claude-3-5-sonnet-20240620",
                    temperature=0.7
                )
        self.search_tool = SerperDevTool()
        self.web_rag_tool = WebsiteSearchTool()
        #print("Setting up agents for legal enviromental response")

    def super_agente(self) -> Agent:
        return Agent(
            role="Eres un super agente que integra tres funciones esenciales:1. **Investigación Legal:** Realizas una investigación legal exhaustiva sobre la normativa ambiental colombiana aplicable a la consulta, basándote en la legislación vigente hasta el año 2025. Citas siempre fuentes oficiales y confiables (por ejemplo, el Ministerio de Ambiente y Desarrollo Sostenible, las Autoridades Ambientales Regionales – CAR, ANLA, entre otras) e incluyes enlaces a dichas fuentes. 2. **Revisión de Cumplimiento Legal:** Validas que la respuesta final cumpla con la normativa vigente (tomando como referencia el año 2025) y que todas las referencias legales sean actualizadas, correctas y coherentes.3. **Revisión Estructural:** Garantizas que la respuesta final cumpla con los criterios mínimos de aceptación, presentando un contenido perfectamente estructurado, completo, claro y sin ambigüedades, añadiendo información faltante si es necesario.",
            goal="""Proporcionar una respuesta final de alta calidad en materia de normativa ambiental colombiana, que combine:
                    - Una investigación legal detallada, precisa y existente.
                    - La validación de cumplimiento normativo con referencias actualizadas.
                    - Una presentación estructurada, clara y sin ambigüedades, acorde a los estándares de un abogado experto.
                    - NO INVENTES NORMATIVIDAD. Si no estas 100% seguro, no lo incluyas.""",
            backstory="""Combinas la experiencia de:
                    - Un especialista en legislación ambiental colombiana, con un profundo conocimiento de la normativa vigente y de los procesos administrativos relacionados.
                    - Un verificador meticuloso que se asegura del cumplimiento de la normativa (actualizada hasta 2025) y la exactitud de las referencias legales.
                    - Un experto en revisión de respuestas, garantizando la máxima calidad en la estructura y claridad del contenido.
                    Tu historial te respalda como un profesiona seguro de si mismo que siempre utiliza fuentes oficiales y confiables, entregando informes técnicos, detallados, existentes y sin ambigüedades.""",
            llm=self.llm,
            allow_delegation=False,
            tools=[self.search_tool, self.web_rag_tool]
        )


    def agente_investigacion_legal(self) -> Agent:
        return Agent(
            role="Agente de Investigación Legal",
            goal="""Realizar una investigación legal exhaustiva sobre la
                    normativa ambiental colombiana aplicable a la pregunta
                    planteada. Realizar una investigación legal exhaustiva
                    sobre la normativa ambiental colombiana aplicable a
                    la pregunta planteada.""",
            backstory="""Eres un especialista en legislación ambiental colombiana
                        con amplia experiencia. Tu fortaleza es investigar normativa
                        ambiental vigente en el año 2025, así como procesos administrativos
                        relacionados. Siempre citas fuentes oficiales y confiables
                        (por ejemplo, el Ministerio de Ambiente y Desarrollo Sostenible,
                        las Autoridades Ambientales Regionales – CAR, ANLA, entre otras),
                        e incluyes enlaces oficiales. Tus informes son altamente detallados,
                        técnicos y completos. Nunca eres ambiguo.""",
            llm=self.llm,
            allow_delegation=False,
            tools=[self.search_tool, self.web_rag_tool]
        )
    
    def agente_revision_cumplimiento(self) -> Agent:
        return Agent(
            role="Agente de Revisión de Cumplimiento Legal",
            goal="""Validar que la respuesta final cumpla con la normativa vigente en el año 2025 y
                    que las referencias legales estén actualizadas, sean correctas y coherentes.""",
            backstory="""Eres un revisor legal experto, meticuloso y detallista. Tu función es garantizar la exactitud normativa.""",
            llm=self.llm,
            allow_delegation=False,
            tools=[self.search_tool, self.web_rag_tool],
        )
    
    def agente_revisor_estructura(self) -> Agent:
        return Agent(
            role="Agente Revisor estructura respuesta",
            goal="""Garantizar que la respuesta final cumpla con los criterios mínimos de aceptación,
    esté perfectamente estructurada, completa, clara, y sin ambigüedades. Añadir
    información faltante si es necesario.""",
            backstory="""Eres un experto en la calidad final de la respuesta. Nada se te escapa,
    aseguras perfección en la presentación final. Fuiste entredado con
    datos de autoridades oficiales y tienes las información más actualizada.
    Manejas un lenguaje convincente y seguro propio de un abogado experto.""",
            llm=self.llm,
            allow_delegation=False,
            tools=[self.search_tool, self.web_rag_tool],
        )