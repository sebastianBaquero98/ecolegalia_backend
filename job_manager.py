from dataclasses import dataclass
from typing import List, Dict
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

import json
import ast

def parse_text_to_json(input_text: str) -> dict:
    """
    Parses the input_text containing Reasoning, Action, Action Input, Observation,
    and optionally Answer, into a structured dictionary.
    """
    # Markers we look for
    ACTION_MARK = "Action:"
    ACTION_INPUT_MARK = "Action Input:"
    OBSERVATION_MARK = "Observation:"
    ANSWER_MARK = "Answer:"
    
    # Find indices for each marker
    idx_action = input_text.find(ACTION_MARK)
    idx_action_input = input_text.find(ACTION_INPUT_MARK)
    idx_observation = input_text.find(OBSERVATION_MARK)
    idx_answer = input_text.find(ANSWER_MARK)
    
    # Prepare a list to hold all steps
    steps = []
    
    # 1) Reasoning: from start of text up to 'Action:' (if Action is found)
    reasoning_text = ""
    if idx_action != -1:
        reasoning_text = input_text[:idx_action].strip()
    else:
        # If for some reason there's no Action, assume everything is Reasoning
        reasoning_text = input_text.strip()
    
    if reasoning_text:
        steps.append({
            "type": "Reasoning",
            "content": reasoning_text
        })
    
    # 2) Action: from 'Action:' up to 'Action Input:' (or next marker)
    action_text = ""
    if idx_action != -1:
        start = idx_action + len(ACTION_MARK)
        end = idx_action_input if idx_action_input != -1 else idx_observation
        if end == -1:  # if 'Action Input:' wasn't found
            end = idx_answer if idx_answer != -1 else len(input_text)
        action_text = input_text[start:end].strip()
    
    # 3) Action Input: from 'Action Input:' up to 'Observation:' (or next marker)
    action_input_text = ""
    if idx_action_input != -1:
        start = idx_action_input + len(ACTION_INPUT_MARK)
        end = idx_observation if idx_observation != -1 else idx_answer
        if end == -1:
            end = len(input_text)
        action_input_text = input_text[start:end].strip()
    
    # Attempt to parse the Action Input text as JSON
    action_input_data = None
    if action_input_text:
        # It's typically JSON with double quotes in your example
        # so we can try json.loads. If that fails, fallback to literal_eval.
        try:
            action_input_data = json.loads(action_input_text)
        except json.JSONDecodeError:
            # Attempt to parse with ast.literal_eval if quotes are single or mixed
            try:
                action_input_data = ast.literal_eval(action_input_text)
            except Exception:
                # Fallback: just store the raw string
                action_input_data = action_input_text
    
    # If there's any action_text or action_input_data, create an Action step
    if action_text or action_input_data is not None:
        action_step = {
            "type": "Action",
            "content": action_text
        }
        if action_input_data is not None:
            action_step["input"] = action_input_data
        
        steps.append(action_step)
    
    # 4) Observation: from 'Observation:' up to 'Answer:' (if present)
    observation_text = ""
    if idx_observation != -1:
        start = idx_observation + len(OBSERVATION_MARK)
        end = idx_answer if idx_answer != -1 else len(input_text)
        observation_text = input_text[start:end].strip()
    
    # Attempt to parse the Observation text as a dictionary (often it's a Python-like dict)
    observation_content = None
    if observation_text:
        # In your example, it's often single-quoted. We'll try literal_eval first.
        # Then fallback to JSON if that fails.
        try:
            observation_content = ast.literal_eval(observation_text)
        except Exception:
            # Try JSON
            try:
                observation_content = json.loads(observation_text)
            except Exception:
                # Fallback: keep raw string
                observation_content = observation_text

        steps.append({
            "type": "Observation",
            "content": observation_content
        })
    
    # 5) Answer: from 'Answer:' to the end (if 'Answer:' is found)
    answer_text = ""
    if idx_answer != -1:
        start = idx_answer + len(ANSWER_MARK)
        end = len(input_text)
        answer_text = input_text[start:end].strip()
        if answer_text:
            steps.append({
                "type": "Answer",
                "content": answer_text
            })
    
    # Wrap everything in the desired top-level structure
    result = {
        "steps": steps
    }
    r = json.dumps(result, indent=2, ensure_ascii=False)
    return r
