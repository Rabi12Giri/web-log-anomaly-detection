import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (username === "admin" && password === "admin@123") {
      localStorage.setItem("isAuthenticated", "true");
      navigate("/");
    } else {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="min-h-screen flex items-center flex-col justify-center bg-slate-100">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold text-indigo-600">
          AI-Based Web Log Anomaly Detection
        </h1>
        <p className="mt-1 text-indigo-500">
          Unsupervised Intrusion Detection System
        </p>
      </div>
      <div className="bg-white p-8 rounded-lg shadow w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Admin Login</h2>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full mb-4 p-2 border rounded"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-4 p-2 border rounded"
        />

        {error && <p className="text-red-600 mb-3">{error}</p>}

        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 cursor-pointer hover:bg-blue-700 text-white py-2 rounded"
        >
          Login
        </button>
      </div>
    </div>
  );
}

export default Login;
