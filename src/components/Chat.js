import React, { useState, useEffect } from "react";
import API_URL from "../api.js"; 


const Chat = ({ sessionId }) => {
    const [messages, setMessages] = useState([]);
    const [socket, setSocket] = useState(null);
    const [input, setInput] = useState("");

    useEffect(() => {
        // Open WebSocket connection
        // ... existing code ...
        const wsUrl = API_URL.defaults.baseURL.replace('http://', 'ws://');
        const ws = new WebSocket(`${wsUrl}/ws/negotiation/${sessionId}`);

        setSocket(ws);

        // Listen for incoming messages
        ws.onmessage = (event) => {
            setMessages((prev) => [...prev, event.data]);
        };

        return () => ws.close(); // Clean up the WebSocket on unmount
    }, [sessionId]);

    const handleSendMessage = () => {
        if (socket && input.trim()) {
            socket.send(input); // Send the user's input to the backend
            setMessages((prev) => [...prev, `You: ${input}`]);
            setInput(""); // Clear the input field
        }
    };

    return (
        <div className="chat-container">
            <h2>AI Salary Negotiation</h2>
            <div className="chat-box">
                {messages.map((msg, index) => (
                    <p key={index}>{msg}</p>
                ))}
            </div>
            <div className="chat-input">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
};

export default Chat;
