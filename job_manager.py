from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime
from threading import Lock

@dataclass
class Event:
    timestamp: datetime
    message: str

@dataclass
class Job:
    status: str
    events: List[Event]
    result: str

jobs_lock = Lock()
jobs: Dict[str, "Job"] = {}

def append_event(job_id:str, event_data: str ):
    with jobs_lock:
        if job_id not in jobs:
            print(f"Start job: {job_id}")
            jobs[job_id] = Job(
                status="STARTED",
                events=[],
                result=""
            )
        else:
            print("Appending event for job")
        
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), message=event_data)
        )

# Modificaciones propuestas para job_manager.py

def parse_text_to_json(input_text: str) -> Dict[str, Any]:
    """
    Versión mejorada de parse_text_to_json que extrae información valiosa
    para el usuario sobre el proceso de investigación legal.
    """
    import re
    import json
    steps: List[Dict[str, Any]] = []
    text = input_text.strip()
    
    # Extraer nombre del agente con formato mejorado para frontend
    agent_name = None
    agent_role = None
    agent_prefix = "Agent: "
    
    # Identificar al agente y asignar un rol comprensible para el usuario
    for line in text.splitlines():
        if line.startswith(agent_prefix):
            agent_name = line[len(agent_prefix):].strip()
            
            # Mapear nombres técnicos a roles comprensibles
            if "investigacion_legal" in agent_name.lower():
                agent_role = "Investigador Jurídico Ambiental"
            elif "revision_cumplimiento" in agent_name.lower():
                agent_role = "Auditor de Normativa Ambiental"
            elif "revisor_estructura" in agent_name.lower():
                agent_role = "Comunicador Jurídico Ambiental"
            else:
                agent_role = "Especialista Legal"
            break
    
    # Detectar fase del proceso según contenido
    current_phase = "análisis"  # Valor por defecto
    if "<plan>" in text:
        current_phase = "investigación"
    elif "verificación" in text.lower() or "vigencia" in text.lower():
        current_phase = "verificación"
    elif "estructura" in text.lower() or "redacción" in text.lower():
        current_phase = "análisis"
    
    # Extraer fuentes consultadas (información de alto valor para el usuario)
    sources = []
    if "Fuente:" in text or "URL:" in text or "Fuentes consultadas:" in text:
        for line in text.splitlines():
            line = line.strip()
            if any(marker in line for marker in ["Fuente:", "URL:", "http"]):
                # Extraer URLs
                urls = re.findall(r'https?://[^\s"<>,]+', line)
                
                # Detectar referencias a normativa (información valiosa)
                doc_refs = re.findall(r'(Ley|Decreto|Resolución|Código)\s+[\d\-\.]+\s+de\s+\d{4}', line, re.IGNORECASE)
                
                for url in urls:
                    source_name = None
                    
                    # Intentar determinar nombre de la fuente (más valioso para el usuario)
                    if "minambiente" in url:
                        source_name = "Ministerio de Ambiente"
                    elif "anla" in url:
                        source_name = "ANLA"
                    elif "suin-juriscol" in url:
                        source_name = "SUIN-Juriscol"
                    elif "funcionpublica" in url:
                        source_name = "Función Pública"
                    
                    source_item = {
                        "url": url,
                        "name": source_name or "Fuente oficial",
                        "doc_name": next(iter(doc_refs), None)
                    }
                    sources.append(source_item)
    
    # Extraer razonamiento del agente
    reasoning_content = None
    if "<plan>" in text and "</plan>" in text:
        reasoning_content = text.split("<plan>", 1)[1].split("</plan>", 1)[0].strip()
        
        # Extraer puntos clave para mejor visualización
        key_points = []
        for line in reasoning_content.split("\n"):
            line = line.strip()
            if line.startswith("- "):
                key_points.append(line.strip()[2:])
        
        steps.append({
            "type": "Reasoning",
            "content": reasoning_content,
            "display_type": "Plan de Investigación",
            "key_points": key_points,
            "agent": agent_name,
            "agent_role": agent_role,
            "sources": sources,
            "phase": current_phase
        })
    elif "Thought:" in text:
        thought_parts = text.split("Thought:", 1)
        if len(thought_parts) > 1:
            reasoning_content = thought_parts[1].split("\n", 1)[0].strip() if "\n" in thought_parts[1] else thought_parts[1]
            
            # Extraer puntos clave para mejor visualización
            key_points = []
            for line in reasoning_content.split("\n"):
                line = line.strip()
                if line.startswith("- "):
                    key_points.append(line.strip()[2:])
            
            steps.append({
                "type": "Reasoning",
                "content": reasoning_content,
                "display_type": "Análisis Legal",
                "key_points": key_points,
                "agent": agent_name,
                "agent_role": agent_role,
                "sources": sources,
                "phase": current_phase
            })
    
    # Extraer acciones con información mejorada
    current_action = None
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Action:"):
            action_content = line[len("Action:"):].strip()
            
            # Mejorar descripción para el usuario
            display_action = action_content
            action_phase = current_phase
            
            if "Consulta Base Legal" in action_content:
                display_action = "Búsqueda en Base de Datos Normativa"
                action_phase = "investigación"
            elif "Search" in action_content:
                display_action = "Búsqueda en Fuentes Oficiales"
                action_phase = "investigación"
            elif "verificación" in action_content.lower():
                display_action = "Verificación de Normativa"
                action_phase = "verificación"
            
            current_action = {
                "type": "Action",
                "content": action_content,
                "display_type": display_action,
                "agent": agent_name,
                "agent_role": agent_role,
                "phase": action_phase
            }
            steps.append(current_action)
        elif line.startswith("Action Input:"):
            action_input = line[len("Action Input:"):].strip()
            
            # Extraer términos de búsqueda (valiosos para el usuario)
            search_query = None
            search_filters = []
            try:
                input_json = json.loads(action_input)
                if "query" in input_json:
                    search_query = input_json["query"]
                
                # Extraer filtros aplicados (muestran trabajo profundo)
                if "metadata_filters" in input_json:
                    for key, value in input_json["metadata_filters"].items():
                        search_filters.append({"name": key, "value": value})
            except:
                search_query = action_input
            
            steps.append({
                "type": "ActionInput",
                "content": action_input,
                "display_type": "Términos de Búsqueda",
                "search_query": search_query,
                "search_filters": search_filters,
                "agent": agent_name,
                "agent_role": agent_role,
                "related_action": current_action["content"] if current_action else None,
                "phase": current_action["phase"] if current_action else current_phase
            })
        elif line.startswith("Observation:"):
            observation_content = line[len("Observation:"):].strip()
            
            # Procesar resultados de búsqueda (altamente valiosos)
            display_type = "Resultados de Búsqueda"
            found_docs = []
            
            # Extraer documentos encontrados
            try:
                if observation_content.startswith("{") and "matches" in observation_content:
                    parsed_obs = json.loads(observation_content)
                    if "matches" in parsed_obs and isinstance(parsed_obs["matches"], list):
                        for match in parsed_obs["matches"][:5]:  # Limitamos a los 5 más relevantes
                            if "metadata" in match and "nombre" in match["metadata"]:
                                doc_name = match["metadata"]["nombre"]
                                doc_type = match["metadata"].get("tipo_acto", "Documento")
                                doc_year = match["metadata"].get("año", "")
                                
                                # Limpiar nombres de documentos (mejorar lectura)
                                if doc_name:
                                    doc_name = doc_name.replace("_", " ").title()
                                
                                found_docs.append({
                                    "name": doc_name,
                                    "type": doc_type,
                                    "year": doc_year,
                                    "relevance": match.get("score", 0)
                                })
            except:
                pass
            
            # Intenta extraer referencias a normativas específicas
            legal_references = []
            norm_patterns = [
                r'(Ley|Decreto|Resolución|Código|Acuerdo)\s+[\d\-\.]+\s+de\s+\d{4}',
                r'(artículo|Art\.)\s+\d+\s+de\s+la\s+(Ley|Decreto|Resolución|Código)',
                r'(MinAmbiente|ANLA|SINA|CORPONOR)'
            ]
            
            for pattern in norm_patterns:
                matches = re.findall(pattern, observation_content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        legal_references.append(" ".join(match))
                    else:
                        legal_references.append(match)
            
            observation_entry = {
                "type": "Observation",
                "content": observation_content,
                "display_type": display_type,
                "found_documents": found_docs,
                "legal_references": legal_references,
                "agent": agent_name,
                "agent_role": agent_role,
                "phase": current_action["phase"] if current_action else current_phase
            }
            
            # Procesar como JSON si es posible
            try:
                if observation_content.startswith("{") and observation_content.endswith("}"):
                    parsed_observation = json.loads(observation_content)
                    observation_entry["parsed"] = parsed_observation
            except:
                pass
                
            steps.append(observation_entry)

    # Procesar respuesta final
    for final_mark in ["### FINAL_ANSWER:", "RESPUESTA_FINAL:"]:
        if final_mark in text:
            answer = text.split(final_mark, 1)[1].strip()
            
            # Identificar secciones en el markdown para mejor visualización
            sections = []
            current_section = {"title": "Introducción", "content": ""}
            
            for line in answer.split("\n"):
                if line.startswith("#"):
                    # Guardar sección anterior si no está vacía
                    if current_section["content"].strip():
                        sections.append(current_section)
                    
                    # Iniciar nueva sección
                    section_level = len(re.match(r'^#+', line).group())
                    section_title = line.lstrip('#').strip()
                    current_section = {"title": section_title, "level": section_level, "content": ""}
                else:
                    current_section["content"] += line + "\n"
            
            # Añadir última sección
            if current_section["content"].strip():
                sections.append(current_section)
            
            # Extraer fuentes/referencias de la respuesta final
            final_sources = []
            if "## Fuentes" in answer or "### Fuentes" in answer or "## Recursos" in answer:
                sources_section = answer.split("## Fuentes", 1)[-1] if "## Fuentes" in answer else \
                              answer.split("### Fuentes", 1)[-1] if "### Fuentes" in answer else \
                              answer.split("## Recursos", 1)[-1]
                
                # Extraer URLs
                final_urls = re.findall(r'https?://[^\s\)"<>]+', sources_section)
                for url in final_urls:
                    final_sources.append({"url": url})
            
            steps.append({
                "type": "Answer",
                "content": answer,
                "sections": sections,
                "sources": final_sources or sources,  # Usar fuentes previas si no hay específicas
                "display_type": "Respuesta Final",
                "agent": agent_name,
                "agent_role": agent_role,
                "phase": "conclusión"
            })
            break

    # Generar información de resumen para el frontend
    summary = {
        "agent_info": {
            "name": agent_name,
            "role": agent_role
        },
        "current_phase": current_phase,
        "sources_count": len(sources),
        "key_findings": []
    }
    
    # Extraer hallazgos clave
    if reasoning_content:
        # Buscar puntos clave - líneas que comienzan con viñetas
        key_lines = [line.strip()[2:] for line in reasoning_content.split("\n") 
                    if line.strip().startswith("- ")]
        summary["key_findings"] = key_lines[:3]  # Limitar a 3 hallazgos clave
    
    # Retornar estructura enriquecida
    return {
        "steps": steps,
        "summary": summary,
        "agents": {
            agent_name or "agent": {
                "steps": steps,
                "role": agent_role
            }
        }
    }
