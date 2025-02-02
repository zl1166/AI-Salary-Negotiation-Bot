import React, { useState } from "react";
import Chat from "./components/Chat";
import RoleSelection from "./components/RoleSelection";
import InputForm from "./components/InputForm";
import { startNegotiation } from "./api";

const App = () => {
    const [role, setRole] = useState(null);
    const [sessionId, setSessionId] = useState(null);

    const handleRoleSelect = (selectedRole) => {
        setRole(selectedRole); // Store the selected role
    };

    const handleFormSubmit = async (formData) => {
        try {
            // Add the role to formData
            const data = { ...formData, role };
            
            // Get the session ID from the API response
            const sessionId = await startNegotiation(data);
            
            if (sessionId) {
                setSessionId(sessionId);
            } else {
                console.error("Failed to get session ID from API");
            }
        } catch (error) {
            console.error("Error in form submission:", error);
        }
    };

    return (
        <div className="app-container">
            <h1>AI Salary Negotiation Bot</h1>
            {!role ? (
                <RoleSelection onSelectRole={handleRoleSelect} />
            ) : !sessionId ? (
                <InputForm onSubmit={handleFormSubmit} />
            ) : (
                <Chat sessionId={sessionId} />
            )}
        </div>
    );
};

export default App;
