import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!username || !password) {
      setError("Username and password are required!");
      return;
    }

    try {
      // Send login request to Django backend
      const response = await axios.post("http://localhost:8000/api/auth/login/", {
        username,
        password,
      });

      // Save token (e.g., in localStorage or context)
      localStorage.setItem("token", response.data.token);
      console.log("Login successful!", response.data);

      // Redirect to dashboard/home
      navigate("/dashboard");
    } catch (err) {
      setError("Invalid username or password.");
      console.error("Login error:", err.response?.data || err.message);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto" }}>
      <h2>Login</h2>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "15px" }}>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: "100%", padding: "8px" }}
          />
        </div>
        <div style={{ marginBottom: "15px" }}>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: "100%", padding: "8px" }}
          />
        </div>
        <button type="submit" style={{ padding: "10px 15px", background: "#007bff", color: "white", border: "none" }}>
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;