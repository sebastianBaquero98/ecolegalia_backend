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

def kickoff_crew(job_id:str, question:str):
    print(f"Running crew for {job_id} with question {question}")
    
    results = None
    try:
        legalEnvironmentCrew = LegalEnvironmentCrew(job_id)
        legalEnvironmentCrew.setup_crew(question)
        results = legalEnvironmentCrew.kickoff()
        results = str(results)
    except Exception as e:
        print(f"Crew Failed: {str(e)}")
        append_event(job_id, f"CREW FAILED: {str(e)}")

        with jobs_lock:
            jobs[job_id].status = "ERROR"
            jobs[job_id].result = str(e)
        return
    
    with jobs_lock:
        jobs[job_id].status = "COMPLETED"
        jobs[job_id].result = results
        jobs[job_id].events.append(Event(
            message="CREW COMPLETED", timestamp=datetime.now()
        ))


@app.route("/api/crew/start", methods=['POST'])
def run_crew():
    data = request.json
    if not data or 'question' not in data:
        abort(400, description="Invalid request with missing data")

    job_id = str(uuid())
    question = data['question']

    # Run the crew
    thread = Thread(target=kickoff_crew, args=(job_id, question))
    thread.start()
    return jsonify({"job_id":job_id}), 200


@app.route("/api/crew/<job_id>", methods=['GET'])
def get_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            abort(404, description="Job not found")

    #print(f"....Type of job.result: {type(job.result)}")
    return jsonify({"job_id": job_id,
                    "status":job.status,
                    "result":job.result,
                    "events":[{"timestamp": event.timestamp.isoformat(), "message":event.message} for event in job.events]}), 200

def kickoff_crew_messages(job_id:str, question:str, messages ):
    print(f"Running crew messages for {job_id} with question {question}")
    
    results = None
    try:
        legal_environmental_crew_messages = LegalEnvironmentalCrewMessages(job_id)
        legal_environmental_crew_messages.setup_crew(messages, question)
        results = legal_environmental_crew_messages.kickoff()
        results = str(results)
        print("This is results")
        print(results)
    except Exception as e:
        print(f"Crew Failed: {str(e)}")
        append_event(job_id, f"CREW FAILED: {str(e)}")

        with jobs_lock:
            jobs[job_id].status = "ERROR"
            jobs[job_id].result = str(e)
        return
    
    with jobs_lock:
        jobs[job_id].status = "COMPLETED"
        jobs[job_id].result = results
        jobs[job_id].events.append(Event(
            message="CREW COMPLETED", timestamp=datetime.now()
        ))
  

@app.route("/api/crew/messages/start", methods=['POST'])
def run_crew_messages():
    data = request.json
    if not data or 'messages' not in data or 'question' not in data:
        abort(400, description="Invalid request with missing data")

    job_id = str(uuid())
    messages = data['messages']
    question = data['question']
    print(f"Running crew for messages")

    # Run the crew
    thread = Thread(target=kickoff_crew_messages, args=(job_id, question, messages))
    thread.start()
    return jsonify({"job_id":job_id}), 200


@app.route("/api/crew/messages/<job_id>", methods=['GET'])
def get_status_messages(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            abort(404, description="Job not found")

    #print(f"....Type of job.result: {type(job.result)}")
    return jsonify({"job_id": job_id,
                    "status":job.status,
                    "result":job.result,
                    "events":[{"timestamp": event.timestamp.isoformat(), "message":event.message} for event in job.events]}), 200


#@app.route("/api/crew/messages", methods=['POST'])
#def start_messages_crew():
    #data = request.json
    #if not data or 'messages' not in data or 'question' not in data:
    #    abort(400, description="Invalid request with missing data")
#
    #messages = data['messages']
    #question = data['question']
    #print(f"Running crew for messages")
    #result = None
    #try:
    #    legal_environmental_crew_messages = LegalEnvironmentalCrewMessages()
    #    legal_environmental_crew_messages.setup_crew(messages, question)
    #    result = legal_environmental_crew_messages.kickoff()
    #    result = str(result)
    #    #print("result")
    #    #print(result)
    #    return jsonify({"result": result}), 200
    #except Exception as e:
    #    print(f"Error: {str(e)}")  # Log the error for debugging
    #    return jsonify({"error": "An error occurred while processing the request."}), 500  # Return a valid error response

if __name__ == '__main__':
    app.run(debug=True, port=3001)