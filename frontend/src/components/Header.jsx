import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header className="bg-slate-900 text-white py-6 shadow">
      <div className=" w-[80%] m-auto flex items-center justify-between">
        <div className="">
          <h1 className="text-3xl font-bold">
            AI-Based Web Log Anomaly Detection
          </h1>
          <p className="text-slate-300 mt-1">
            Unsupervised Intrusion Detection System
          </p>
        </div>
        <div className="flex items-center gap-4">
          <Link to="/monitor">
            <button className="text-sm bg-green-500 hover:bg-green-600 px-4 py-2 rounded cursor-pointer">
              Monitor Status
            </button>
          </Link>
          <Link to="/">
            <button className="text-sm bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded cursor-pointer">
              Dashboard
            </button>
          </Link>

          <button
            onClick={() => {
              localStorage.removeItem("isAuthenticated");
              localStorage.removeItem("anomalyResult");
              window.location.href = "/login";
            }}
            className="text-sm bg-red-500 hover:bg-red-600 px-4 py-2 rounded cursor-pointer"
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
