import React, { useState } from "react";

const InputForm = ({ onSubmit }) => {
    const [formData, setFormData] = useState({
        role: "", // or "recruiter"
        job_title: "",
        company: "",
        location: "",
        current_salary: "",
        desired_salary: "",
        years_experience: "",
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({
            ...formData,
            current_salary: parseFloat(formData.current_salary),
            desired_salary: parseFloat(formData.desired_salary),
            years_experience: parseFloat(formData.years_experience)
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Enter Job and Salary Details</h2>
            <input
                type="text"
                name="job_title"
                placeholder="Job Title"
                value={formData.job_title}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="company"
                placeholder="Company"
                value={formData.company}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="location"
                placeholder="Location"
                value={formData.location}
                onChange={handleChange}
                required
            />
            <input
                type="number"
                name="current_salary"
                placeholder="Current Salary"
                value={formData.current_salary}
                onChange={handleChange}
                required
            />
            <input
                type="number"
                name="desired_salary"
                placeholder="Desired Salary"
                value={formData.desired_salary}
                onChange={handleChange}
                required
            />
            <input
                type="number"
                name="years_experience"
                placeholder="Years of Experience"
                value={formData.years_experience}
                onChange={handleChange}
                required
            />
            <button type="submit">Start Negotiation</button>
        </form>
    );
};

export default InputForm;
