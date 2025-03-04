from dataclasses import dataclass
from crewai import Crew, Process
from agents import LegalEnvironmentAgents
from job_manager import append_event, parse_text_to_json
from tasks import LegalEnvironmentTasks
from crewai.agents.parser import AgentAction, AgentFinish
from typing import List

class LegalEnvironmentCrew:
    def __init__(self,job_id: str):
        self.crew = None
        self.job_id = job_id

    def append_event_callback(self, step):
        if isinstance(step, AgentAction):
            #print(f"Action: {step.text}")
            # Convert into dict string information
            r = parse_text_to_json(step.text.encode('utf-8').decode('utf-8'))  # Ensure proper encoding
            append_event(self.job_id, r)

        elif isinstance(step, AgentFinish):
            split_text = step.text.split("Final Answer:")
            if len(split_text) == 1:
                append_event(self.job_id, "Finish:"+split_text.replace("Thought:", ""))
            else:
                append_event(self.job_id, "Finish:"+split_text[0].strip().replace("Thought:", ""))

        
    def setup_crew(self, question: str):
        print(f"Setting up crew for {self.job_id} and question {question}")

        # SETUP AGENTS
        agents = LegalEnvironmentAgents()
        agente_investigacion_legal = agents.agente_investigacion_legal()
        agente_revision_cumplimiento = agents.agente_revision_cumplimiento()
        agente_revisor_estructura = agents.agente_revisor_estructura()

        # SETUP TASKS
        tasks = LegalEnvironmentTasks(self.job_id)
        tarea_investigacion = tasks.tarea_investigacion(agente_investigacion_legal, question)
        tarea_revision_legal = tasks.tarea_revision_legal(agente_revision_cumplimiento)
        tarea_estructura = tasks.tarea_estructura(agente_revisor_estructura, question)

        # CREATE CREW
        self.crew = Crew(
            agents=[agente_investigacion_legal,agente_revision_cumplimiento,agente_revisor_estructura],
            tasks=[tarea_investigacion,tarea_revision_legal,tarea_estructura],
            process=Process.sequential,
            verbose=False,
            step_callback=self.append_event_callback,
        )

    def kickoff(self):
        if not self.crew:
            print(f"No crew found for {self.job_id}")
            return
        
        append_event(self.job_id, "CREW STARTED")
        try:
            print(f"Running crew for {self.job_id}")
            answer = self.crew.kickoff()
            #append_event(self.job_id, "CREW COMPLETED")
            return answer
        except Exception as e:
            return str(e)
        
