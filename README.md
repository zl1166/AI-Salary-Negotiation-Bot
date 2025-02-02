
# **AI Salary Negotiation Bot 🤖💼**
> **An AI-powered web application that facilitates real-time salary negotiations using GPT-4.**

This project enables users to simulate and participate in **salary negotiations** with two AI agents:
- **Candidate AI**: Assists the job seeker by providing insights, strategies, and recommendations.
- **Recruiter AI**: Represents the company's interests and makes counteroffers during negotiations.

The app uses GPT-4 for AI reasoning and WebSocket for real-time interactions, creating a seamless and engaging user experience.

---

## **🌟 Features**
- **Dual AI Agents**: Two distinct AI agents for job seeker and recruiter roles.
- **Real-Time Negotiation**: WebSocket-powered live chat interaction.
- **GPT-4 Integration**: Utilizes OpenAI's GPT-4 for natural language understanding and generation.
- **Salary Insights**: Includes tools to guide users toward better negotiation outcomes.
- **Frontend-Backend Integration**: React frontend with a FastAPI backend.
- **Lightweight Data Storage**: Uses JSON file storage—no database required.

---

## **🛠️ Tech Stack**
- **Frontend**: React.js, Axios, WebSocket
- **Backend**: FastAPI, OpenAI GPT-4
- **Storage**: JSON file for session and negotiation data
- **Real-Time Communication**: WebSocket for live chat functionality

---

## **🚀 How It Works**
1. **Role Selection**:
   - Users select their role: **Job Seeker** or **Recruiter**.
2. **Salary Input**:
   - Users enter details such as desired salary, current salary, job title, and location.
3. **AI Negotiation**:
   - The AI agents interact in real time, simulating negotiation offers and counteroffers.
4. **Real-Time Updates**:
   - Users see the conversation unfold live, with responses from both AI agents.

---

## **📁 Project Structure**
```
salary-negotiation-bot/
│
├── backend/
│   ├── main.py             # FastAPI backend and WebSocket handling
│   ├── ai_agents.py        # AI logic for Candidate AI and Recruiter AI
│   ├── database.py         # JSON file-based storage
│   └── negotiation_data.json # JSON file storing negotiation sessions
│
├── salary-negotiation-bot/ # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Chat.js     # Chat interface for live negotiation
│   │   │   ├── RoleSelection.js  # Role selection interface
│   │   │   ├── InputForm.js # Form for entering job details
│   │   ├── api.js          # API calls to backend
│   │   ├── App.js          # Main React app
│   ├── package.json        # Frontend dependencies
│   └── public/             # Static assets
│
└── .env                    # API keys and configurations
```

---

## **⚙️ Setup Instructions**

### **1️⃣ Backend Setup**
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn openai python-dotenv
   ```
3. Add your OpenAI API key in `.env`:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ```
4. Run the backend server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

### **2️⃣ Frontend Setup**
1. Navigate to the React frontend directory:
   ```bash
   cd salary-negotiation-bot
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm start
   ```

---

## **💡 Key Features to Highlight on Your Resume**
When adding this project to your resume, highlight:
- **Built a real-time, full-stack AI application** using React.js and FastAPI.
- **Integrated GPT-4** to simulate complex salary negotiation scenarios with dual AI agents.
- **Designed a WebSocket-based communication system** for live AI-to-user interactions.
- **Implemented lightweight JSON file storage** to track negotiation sessions and user inputs.

---

## **📖 Example Resume Description**
> **AI Salary Negotiation Bot**  
> Developed a full-stack web application to simulate salary negotiations using GPT-4. Designed dual AI agents (job seeker and recruiter roles) to provide real-time negotiation assistance. Built a React-based frontend integrated with a FastAPI backend via WebSockets, enabling live interaction between the user and AI agents. Implemented a lightweight JSON-based storage system for managing negotiation session data without a database.

---

## **📜 License**
This project is licensed under the MIT License. Feel free to use, modify, and distribute.

---

## **📧 Contact**
If you have any questions or feedback about this project, feel free to contact me!
