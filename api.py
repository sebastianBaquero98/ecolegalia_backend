from datetime import datetime
from threading import Thread
from uuid import uuid4 as uuid
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import json

from crew import LegalEnvironmentCrew
from crew_messages import LegalEnvironmentalCrewMessages
from job_manager import Event, append_event, jobs_lock, jobs

app = Flask(__name__)
CORS(app, resources={r"/api/*":{"origins":"*"}})


def kickoff_crew(job_id: str, question: str):
    print(f"Running crew for {job_id} with question {question}")
    try:
        legalEnvironmentCrew = LegalEnvironmentCrew(job_id)
        legalEnvironmentCrew.setup_crew(question)
        answer = legalEnvironmentCrew.kickoff()

        # Extract RESPUESTA_FINAL if present
        if isinstance(answer, str) and "RESPUESTA_FINAL:" in answer:
            answer = answer.split("RESPUESTA_FINAL:", 1)[1].strip()

    except Exception as e:
        print(f"Crew Failed: {str(e)}")
        append_event(job_id, f"CREW FAILED: {str(e)}")
        with jobs_lock:
            jobs[job_id].status = "ERROR"
            jobs[job_id].result = str(e)
        return

    # If no valid answer produced, mark job as error
    if answer is None or (isinstance(answer, str) and (answer.strip() == "" or "Invalid response from LLM call" in answer)):
        with jobs_lock:
            jobs[job_id].status = "ERROR"
            jobs[job_id].result = "Crew did not produce a valid response."
        return

    # Use the last "Finish:" event as the definitive result if available
    with jobs_lock:
        final_msg = None
        for event in reversed(jobs[job_id].events):
            if event.message.startswith("Finish:"):
                final_msg = event.message[len("Finish:"):].strip()
                break
        result_to_save = final_msg if final_msg is not None else answer

        jobs[job_id].status = "COMPLETED"
        jobs[job_id].result = str(result_to_save)
        jobs[job_id].events.append(
            Event(message="CREW COMPLETED", timestamp=datetime.now())
        )

@app.route("/api/crew/start", methods=['POST'])
def run_crew():
    data = request.json
    if not data or 'question' not in data:
        abort(400, description="Invalid request with missing data")

    job_id = str(uuid())
    question = data['question']

    thread = Thread(target=kickoff_crew, args=(job_id, question))
    thread.start()
    return jsonify({"job_id": job_id}), 200

@app.route("/api/crew/<job_id>", methods=['GET'])
def get_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            abort(404, description="Job not found")

    # Extraer información enriquecida para el frontend
    current_phase = get_current_phase(job.events)
    active_agents = extract_active_agents(job.events)
    sources_consulted = extract_sources_consulted(job.events)
    key_findings = extract_key_findings(job.events)

    # Enriquecer eventos con fases
    enriched_events = []
    for event in job.events:
        event_data = {
            "timestamp": event.timestamp.isoformat(),
            "message": event.message
        }
        
        # Intentar asignar fase si es posible
        if event.message == "CREW STARTED":
            event_data["phase"] = "inicio"
        elif event.message == "CREW COMPLETED":
            event_data["phase"] = "completado"
        elif "FINAL_ANSWER:" in event.message or "Finish:" in event.message:
            event_data["phase"] = "conclusión"
        elif event.message.startswith("{"):
            try:
                data = json.loads(event.message)
                if "steps" in data and len(data["steps"]) > 0:
                    first_step = data["steps"][0]
                    if "phase" in first_step:
                        event_data["phase"] = first_step["phase"]
                    
                    # Añadir información de agente si está disponible
                    if "agent_role" in first_step:
                        event_data["agent_role"] = first_step["agent_role"]
                    
                    # Extraer display_type si existe
                    if "display_type" in first_step:
                        event_data["display_type"] = first_step["display_type"]
            except:
                pass
        
        enriched_events.append(event_data)

    # Devolver respuesta con información enriquecida
    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": job.result,
        "events": enriched_events,
        "research_info": {
            "current_phase": current_phase,
            "active_agents": active_agents,
            "sources_consulted": sources_consulted,
            "key_findings": key_findings
        }
    }), 200


def kickoff_crew_messages(job_id: str, question: str, messages):
    print(f"Running crew messages for {job_id} with question {question}")
    try:
        legal_environmental_crew_messages = LegalEnvironmentalCrewMessages(job_id)
        legal_environmental_crew_messages.setup_crew(messages, question)
        results = legal_environmental_crew_messages.kickoff()

        # Extract RESPUESTA_FINAL if present
        if isinstance(results, str) and "RESPUESTA_FINAL:" in results:
            results = results.split("RESPUESTA_FINAL:", 1)[1].strip()

    except Exception as e:
        print(f"Crew Failed: {str(e)}")
        append_event(job_id, f"CREW FAILED: {str(e)}")
        with jobs_lock:
            jobs[job_id].status = "ERROR"
            jobs[job_id].result = str(e)
        return

    with jobs_lock:
        final_msg = None
        for event in reversed(jobs[job_id].events):
            if event.message.startswith("Finish:"):
                final_msg = event.message[len("Finish:"):].strip()
                break
        result_to_save = final_msg.replace("RESPUESTA_FINAL:","") if final_msg is not None else results

        jobs[job_id].status = "COMPLETED"
        jobs[job_id].result = str(result_to_save)
        jobs[job_id].events.append(
            Event(message="CREW COMPLETED", timestamp=datetime.now())
        )

@app.route("/api/crew/messages/start", methods=['POST'])
def run_crew_messages():
    data = request.json
    if not data or 'messages' not in data or 'question' not in data:
        abort(400, description="Invalid request with missing data")

    job_id = str(uuid())
    messages = data['messages']
    question = data['question']

    thread = Thread(target=kickoff_crew_messages, args=(job_id, question, messages))
    thread.start()
    return jsonify({"job_id": job_id}), 200

@app.route("/api/crew/messages/<job_id>", methods=['GET'])
def get_status_messages(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            abort(404, description="Job not found")

    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": job.result,
        "events": [
            {"timestamp": event.timestamp.isoformat(), "message": event.message}
            for event in job.events
        ]
    }), 200

def get_current_phase(events):
    """
    Determina la fase actual del proceso basado en los eventos.
    """
    if not events:
        return {
            "name": "inicio",
            "display_name": "Iniciando investigación",
            "progress": 5
        }
    
    # Buscar de atrás hacia adelante para encontrar la fase más reciente
    for event in reversed(events):
        if event.message == "CREW COMPLETED":
            return {
                "name": "completado",
                "display_name": "Proceso completado",
                "progress": 100
            }
        
        if "FINAL_ANSWER:" in event.message or "Finish:" in event.message:
            return {
                "name": "conclusión",
                "display_name": "Elaborando respuesta",
                "progress": 95
            }
        
        # Analizar eventos JSON para detectar la fase
        if event.message.startswith("{"):
            try:
                data = json.loads(event.message)
                if "summary" in data and "current_phase" in data["summary"]:
                    phase_name = data["summary"]["current_phase"]
                    
                    # Mapear nombre de fase a info completa
                    phase_info = {
                        "investigación": {
                            "name": "investigación",
                            "display_name": "Consultando normativa",
                            "progress": 30
                        },
                        "verificación": {
                            "name": "verificación",
                            "display_name": "Verificando vigencia y aplicabilidad",
                            "progress": 50
                        },
                        "análisis": {
                            "name": "análisis",
                            "display_name": "Analizando hallazgos",
                            "progress": 70
                        }
                    }
                    
                    return phase_info.get(phase_name, {
                        "name": phase_name,
                        "display_name": "Procesando información",
                        "progress": 40
                    })
                
                # Alternativamente, inferir de los pasos
                if "steps" in data:
                    for step in data["steps"]:
                        if "phase" in step:
                            phase_name = step["phase"]
                            
                            # Mapear nombre de fase a info completa
                            phase_info = {
                                "investigación": {
                                    "name": "investigación",
                                    "display_name": "Consultando normativa",
                                    "progress": 30
                                },
                                "verificación": {
                                    "name": "verificación",
                                    "display_name": "Verificando vigencia y aplicabilidad",
                                    "progress": 50
                                },
                                "análisis": {
                                    "name": "análisis",
                                    "display_name": "Analizando hallazgos",
                                    "progress": 70
                                }
                            }
                            
                            return phase_info.get(phase_name, {
                                "name": phase_name,
                                "display_name": "Procesando información",
                                "progress": 40
                            })
            except:
                pass
    
    # Valor por defecto si no se puede determinar
    return {
        "name": "investigación",
        "display_name": "Investigando normativa",
        "progress": 30
    }

def extract_active_agents(events):
    """
    Extrae información sobre los agentes activos en el proceso.
    """
    agents = {}
    
    for event in events:
        if event.message.startswith("{"):
            try:
                data = json.loads(event.message)
                
                # Extraer información del agente
                if "summary" in data and "agent_info" in data["summary"]:
                    agent_info = data["summary"]["agent_info"]
                    
                    if "name" in agent_info and "role" in agent_info:
                        agent_name = agent_info["name"] or "Agente"
                        
                        agents[agent_name] = {
                            "name": agent_name,
                            "role": agent_info["role"],
                            "last_active": event.timestamp.isoformat()
                        }
                
                # Buscar en los pasos también
                if "steps" in data:
                    for step in data["steps"]:
                        if "agent" in step and "agent_role" in step:
                            agent_name = step["agent"] or "Agente"
                            
                            agents[agent_name] = {
                                "name": agent_name,
                                "role": step["agent_role"],
                                "last_active": event.timestamp.isoformat(),
                                "current_action": step.get("display_type", step.get("type", "Analizando"))
                            }
            except:
                pass
    
    return list(agents.values())

def extract_sources_consulted(events):
    """
    Extrae las fuentes consultadas durante el proceso.
    """
    sources = {}
    
    for event in events:
        if event.message.startswith("{"):
            try:
                data = json.loads(event.message)
                
                # Buscar fuentes en los pasos
                if "steps" in data:
                    for step in data["steps"]:
                        # Fuentes explícitas
                        if "sources" in step and isinstance(step["sources"], list):
                            for source in step["sources"]:
                                if "url" in source:
                                    source_key = source["url"]
                                    sources[source_key] = {
                                        "url": source["url"],
                                        "name": source.get("name", "Fuente oficial"),
                                        "doc_name": source.get("doc_name", "")
                                    }
                        
                        # Documentos encontrados
                        if "found_documents" in step and isinstance(step["found_documents"], list):
                            for doc in step["found_documents"]:
                                doc_key = f"{doc.get('name', '')}-{doc.get('type', '')}-{doc.get('year', '')}"
                                sources[doc_key] = {
                                    "name": doc.get("name", "Documento"),
                                    "type": doc.get("type", "Normativa"),
                                    "year": doc.get("year", "")
                                }
            except:
                pass
    
    return list(sources.values())

def extract_key_findings(events):
    """
    Extrae hallazgos clave del proceso de investigación.
    """
    findings = []
    
    for event in events:
        if event.message.startswith("{"):
            try:
                data = json.loads(event.message)
                
                # Buscar hallazgos en el resumen
                if "summary" in data and "key_findings" in data["summary"]:
                    for finding in data["summary"]["key_findings"]:
                        if finding not in findings:
                            findings.append(finding)
                
                # Buscar en pasos de tipo Reasoning
                if "steps" in data:
                    for step in data["steps"]:
                        if step["type"] == "Reasoning" and "key_points" in step:
                            for point in step["key_points"]:
                                if point not in findings:
                                    findings.append(point)
                
                # Buscar referencias legales en observaciones
                if "steps" in data:
                    for step in data["steps"]:
                        if step["type"] == "Observation" and "legal_references" in step:
                            for ref in step["legal_references"]:
                                if ref not in findings:
                                    findings.append(ref)
            except:
                pass
    
    return findings[:5]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
