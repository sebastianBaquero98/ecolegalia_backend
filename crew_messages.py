from dataclasses import dataclass
from crewai import Crew, Process
from agents import LegalEnvironmentAgents
from job_manager import append_event, parse_text_to_json
from tasks import LegalEnvironmentTasks
from crewai.agents.parser import AgentAction, AgentFinish
from typing import List

@dataclass
class Message:
    query: str
    response: str
        
class LegalEnvironmentalCrewMessages:
    def __init__(self, job_id: str):
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

    def setup_crew(self, messages: List[Message], question:str):
        # SETUP AGENTS
        agents = LegalEnvironmentAgents()
        super_agente = agents.super_agente()
        #agente_revision_cumplimiento = agents.agente_revision_cumplimiento()

        # SETUP TASKS
        tasks = LegalEnvironmentTasks("1234")
        tarea_super_mensajes = tasks.tarea_super_mensajes(super_agente, messages, question)
        #tarea_revision_legal = tasks.tarea_revision_legal_messages(agente_revision_cumplimiento, question)

        # CREATE CREW
        self.crew = Crew(
            agents=[super_agente],
            tasks=[tarea_super_mensajes],
            process=Process.sequential,
            verbose=False,
            step_callback=self.append_event_callback,
        )

    def kickoff(self):
        if not self.crew:
            print(f"No crew found")
            return
        
        #append_event(self.job_id, "CREW STARTED")
        try:
            #print(f"Running crew")
            answer = self.crew.kickoff()
            #append_event(self.job_id, "CREW COMPLETED")
            return answer
        except Exception as e:
            return str(e)
