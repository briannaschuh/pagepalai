import React from "react";
import "../styles/Home.css";

import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate(); // used to programmatically navigate to /reader

  return (
    <div className="home-container">
      <h1>LLM Reading Tutor</h1>
      <p>An AI-powered reading assistant...</p>
      <button onClick={() => navigate("/reader")}>
        Get Started
      </button>
    </div>
  );
};

export default Home;
