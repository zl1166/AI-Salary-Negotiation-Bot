import React from "react";

const RoleSelection = ({ onSelectRole }) => {
    return (
        <div className="role-selection">
            <h2>Select Your Role</h2>
            <button onClick={() => onSelectRole("job_seeker")}>Job Seeker</button>
            <button onClick={() => onSelectRole("recruiter")}>Recruiter</button>
        </div>
    );
};

export default RoleSelection;
