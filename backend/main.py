from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Optional
import uuid
import random
import json
from database import save_session, get_session
import os
from pathlib import Path
from ai_agents import job_seeker_ai, recruiter_ai

# Define the data model for negotiation input
class NegotiationData(BaseModel):
    role: str  # This will be either "job_seeker" or "recruiter"
    jobTitle: str
    seekerMin: Optional[float] = None
    seekerTarget: Optional[float] = None
    seekerMax: Optional[float] = None
    recruiterMin: Optional[float] = None
    recruiterMax: Optional[float] = None
    yearsExperience: Optional[float] = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the data file exists
if not os.path.exists("negotiation_data.json"):
    Path("negotiation_data.json").write_text("{}")

@app.post("/api/start-negotiation")
async def start_negotiation(userData: NegotiationData):
    """Start a new negotiation session with role and salary information"""
    session_id = str(uuid.uuid4())
    print(f"Creating new session: {session_id}")
    print(f"Received user data: {userData}")
    
    try:
        # Initialize variables
        seeker_min = 0
        seeker_max = 0
        seeker_target = 0
        recruiter_min = 0
        recruiter_max = 0

        if userData.role == "job_seeker":  # Changed from "seeker"
            if not all([userData.seekerMin, userData.seekerTarget, userData.seekerMax]):
                raise HTTPException(status_code=400, detail="Seeker salary ranges required")
                
            seeker_min = userData.seekerMin
            seeker_target = userData.seekerTarget
            seeker_max = userData.seekerMax
            
            recruiter_max = round(seeker_max * 1.5)
            recruiter_min = round(seeker_min * 0.8)
        
        else:  # recruiter
            if not all([userData.recruiterMin, userData.recruiterMax]):
                raise HTTPException(status_code=400, detail="Recruiter salary range required")
                
            recruiter_min = userData.recruiterMin
            recruiter_max = userData.recruiterMax
            
            seeker_min = recruiter_min * 0.9
            seeker_max = recruiter_max * 1.2
            seeker_target = (seeker_min + seeker_max) / 2

        session_data = {
            "session_id": session_id,
            "role": userData.role,  # This will be "job_seeker" or "recruiter"
            "job_title": userData.jobTitle,
            "seeker_range": {
                "min": seeker_min,
                "target": seeker_target,
                "max": seeker_max
            },
            "recruiter_range": {
                "min": recruiter_min,
                "max": recruiter_max
            },
            "facts": {
                "job_seeker": [],
                "recruiter": []
            }
        }
        
        # Store session data
        save_session(session_id, session_data)
        print(f"Stored session data: {session_data}")
        
        return {"session_id": session_id}
        
    except Exception as e:
        print(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/negotiation/{session_id}")
async def negotiation_chat(websocket: WebSocket, session_id: str):
    await websocket.accept()
    print(f"WebSocket connection accepted for session: {session_id}")
    
    try:
        while True:
            client_message = await websocket.receive_text()
            print(f"Received message from client: {client_message}")
            
            session_data = get_session(session_id)
            if not session_data:
                await websocket.send_text("Error: Session not found.")
                break

            try:
                # Store user message
                if "messages" not in session_data:
                    session_data["messages"] = []
                session_data["messages"].append({
                    "role": session_data["role"],
                    "content": client_message
                })
                save_session(session_id, session_data)
                
                # Process message with appropriate AI
                if session_data["role"] == "job_seeker":
                    print("Processing as job seeker role")
                    ai_response = recruiter_ai(session_id, client_message)
                    if ai_response:
                        await websocket.send_text(f"Recruiter: {ai_response}")
                    else:
                        await websocket.send_text("Error: No response from recruiter AI")
                else:
                    print("Processing as recruiter role")
                    ai_response = job_seeker_ai(session_id, client_message)
                    if ai_response:
                        await websocket.send_text(f"Job Seeker: {ai_response}")
                    else:
                        await websocket.send_text("Error: No response from job seeker AI")

            except Exception as ai_error:
                print(f"AI Error: {str(ai_error)}")
                await websocket.send_text(f"AI Error: {str(ai_error)}")

    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
    except Exception as e:
        print(f"Error in session {session_id}: {str(e)}")
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        try:
            await websocket.close()
        except:
            pass

@app.get("/api/session/{session_id}")
async def get_session_data(session_id: str):
    """Get session data"""
    session_data = get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_data
