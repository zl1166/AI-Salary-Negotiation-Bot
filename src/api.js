import axios from "axios";

// Define the interface for user data
const API_URL = axios.create({
    baseURL: "http://0.0.0.0:8000"
});

export const startNegotiation = async (userData) => {
    try {
        const response = await axios.post(`${API_URL.defaults.baseURL}/api/start-negotiation`, {
            role: userData.role,
            jobTitle: userData.job_title,
            seekerMin: userData.current_salary,
            seekerTarget: userData.desired_salary,
            seekerMax: userData.desired_salary * 1.1, // Set max slightly higher than desired
            recruiterMin: userData.current_salary * 0.9, // For recruiter role
            recruiterMax: userData.desired_salary, // For recruiter role
            yearsExperience: userData.years_experience
        });
        return response.data.session_id;
    } catch (error) {
        console.error("Error starting negotiation:", error);
        return null;
    }
};

export default API_URL;