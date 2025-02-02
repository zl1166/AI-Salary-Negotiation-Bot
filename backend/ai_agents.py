from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from database import get_session, save_session
from typing import Dict

# Load OpenAI API key
load_dotenv()
with open('/Users/zoey2022mac/study/devs/negociation/key.json', 'r') as file:
    key_data = json.load(file)
api_key = key_data['key']

# Step 3: Set the API key as an environment variable
os.environ['OPENAI_API_KEY'] = api_key
client = OpenAI()
client.api_key = key_data['key']

def get_session_data(session_id):
    """Retrieve negotiation session data"""
    return get_session(session_id)

def extract_facts_from_message(message: str, role: str) -> Dict:
    """Extract factual information in sentence format"""
    system_prompt = f"""Extract factual information from this {role}'s message as complete sentences.
    
    For job_seeker messages, create sentences about:
    - Their experience and background
    - Skills and expertise
    - Education and certifications
    - Achievements and impact
    - Current situation and preferences
    - Compensation expectations
    
    For recruiter messages, create sentences about:
    - Company benefits and perks
    - Role requirements and expectations
    - Team and company culture
    - Growth and development opportunities
    - Compensation structure
    - Working arrangements
    
    Return ONLY facts that were explicitly mentioned in the message.
    Format each fact as a complete, clear sentence."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Message: {message}\nExtract facts as sentences from this {role} message."}
            ],
            temperature=0.1
        )
        
        facts = response.choices[0].message.content.split('\n')
        facts = [f for f in facts if f.strip()]  # Remove empty lines
        print(f"Extracted facts from {role}: {facts}")  # Debug log
        return facts
    except Exception as e:
        print(f"Error extracting facts: {str(e)}")
        return []

def update_session_facts(session_id: str, new_facts: list, role: str):
    """Update session with new fact sentences"""
    session_data = get_session_data(session_id)
    if not session_data:
        return
    
    # Initialize facts structure if it doesn't exist
    if "facts" not in session_data:
        session_data["facts"] = {
            "job_seeker": [],
            "recruiter": []
        }
    
    # Add new facts if they're not already present
    current_facts = session_data["facts"][role]  # role is either "job_seeker" or "recruiter"
    
    for fact in new_facts:
        if fact not in current_facts:
            current_facts.append(fact)
    
    # Save updated session data
    save_session(session_id, session_data)

def get_recent_exchanges(session_data, num_messages=3):
    """Get the most recent messages from both parties"""
    facts = session_data.get("facts", {})
    messages = session_data.get("messages", [])
    
    # Get last 3 messages from each role
    job_seeker_messages = []
    recruiter_messages = []
    
    for msg in reversed(messages):  # Start from most recent
        if len(job_seeker_messages) < num_messages and msg["role"] == "job_seeker":
            job_seeker_messages.append(msg["content"])
        if len(recruiter_messages) < num_messages and msg["role"] == "recruiter":
            recruiter_messages.append(msg["content"])
        if len(job_seeker_messages) >= num_messages and len(recruiter_messages) >= num_messages:
            break
    
    return {
        "job_seeker": list(reversed(job_seeker_messages)),  # Restore chronological order
        "recruiter": list(reversed(recruiter_messages))
    }

def recruiter_ai(session_id, user_input):
    """AI Recruiter negotiates based on company's budget."""
    session_data = get_session_data(session_id)
    if not session_data:
        return "Error: Session not found"
    
    # Extract facts from job seeker's message
    job_seeker_facts = extract_facts_from_message(user_input, "job_seeker")
    if job_seeker_facts:
        update_session_facts(session_id, job_seeker_facts, "job_seeker")
    
    # Get updated session data with new facts
    session_data = get_session_data(session_id)
    facts = session_data.get("facts", {})
    recent_messages = get_recent_exchanges(session_data)
    
    system_prompt = f"""You are a professional recruiter negotiating for a {session_data['job_title']} position.
    Your budget range is ${session_data['recruiter_range']['min']:,} - ${session_data['recruiter_range']['max']:,}.
    
    What we know about the job seeker:
    {chr(10).join(facts.get('job_seeker', []))}
    
    Recent conversation history:
    Job Seeker's recent messages:
    {chr(10).join([f"- {msg}" for msg in recent_messages['job_seeker']])}
    
    Recruiter's recent messages:
    {chr(10).join([f"- {msg}" for msg in recent_messages['recruiter']])}
    
    Guidelines:
    - don't reveal the company's budget range 
    - response in 10-100 words
    - be concise and to the point
    - the goal is to reach a mutual agreement on the salary
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        ai_response = response.choices[0].message.content
        
        # Extract facts from AI's response
        recruiter_facts = extract_facts_from_message(ai_response, "recruiter")
        if recruiter_facts:
            update_session_facts(session_id, recruiter_facts, "recruiter")
        
        # Add response to message history
        session_data = get_session_data(session_id)
        if "messages" not in session_data:
            session_data["messages"] = []
        session_data["messages"].append({
            "role": "recruiter",
            "content": ai_response
        })
        save_session(session_id, session_data)
        
        return ai_response
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        return f"Error in generating response: {str(e)}"

def job_seeker_ai(session_id, user_input):
    """AI helps the job seeker negotiate."""
    session_data = get_session_data(session_id)
    if not session_data:
        return "Error: Session not found"
    
    # Extract facts from recruiter's message
    recruiter_facts = extract_facts_from_message(user_input, "recruiter")
    if recruiter_facts:
        update_session_facts(session_id, recruiter_facts, "recruiter")
    
    # Get updated session data with new facts
    session_data = get_session_data(session_id)
    facts = session_data.get("facts", {})
    recent_messages = get_recent_exchanges(session_data)
    seeker_range = session_data["seeker_range"]
    
    system_prompt = f"""You are a job seeker negotiating for a {session_data['job_title']} position.
    Your salary expectations:
    - Minimum acceptable: ${seeker_range['min']:,}
    - Target salary: ${seeker_range['target']:,}
    - Ideal maximum: ${seeker_range['max']:,}
    
    What we know about your background and preferences:
    {chr(10).join(facts.get('job_seeker', []))}
    
    What we know about the company and role:
    {chr(10).join(facts.get('recruiter', []))}
    
    Recent conversation history:
    Job Seeker's recent messages:
    {chr(10).join([f"- {msg}" for msg in recent_messages['job_seeker']])}
    
    Recruiter's recent messages:
    {chr(10).join([f"- {msg}" for msg in recent_messages['recruiter']])}
    
    Guidelines:
    - Use known facts about the company and role in your negotiation
    - Consider the recent conversation context
    - Reference your relevant experience and achievements
    - Be professional and confident
    - Don't reveal your exact salary ranges
    - Start negotiations near your target salary
    - Consider the entire compensation package
    - Use market research to support your position
    - Be prepared to compromise but don't go below your minimum
    - Keep responses focused on the negotiation
    - Add new factual information about your qualifications when relevant
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        ai_response = response.choices[0].message.content
        
        # Extract facts from AI's response
        job_seeker_facts = extract_facts_from_message(ai_response, "job_seeker")
        if job_seeker_facts:
            update_session_facts(session_id, job_seeker_facts, "job_seeker")
        
        # Add response to message history
        session_data = get_session_data(session_id)
        if "messages" not in session_data:
            session_data["messages"] = []
        session_data["messages"].append({
            "role": "job_seeker",
            "content": ai_response
        })
        save_session(session_id, session_data)
        
        return ai_response
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        return f"Error in generating response: {str(e)}"
