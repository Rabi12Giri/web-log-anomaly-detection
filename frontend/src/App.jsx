import { useEffect, useState, useRef } from "react";
import Charts from "./components/Charts";
import { Navigate } from "react-router-dom";
import SummaryCards from "./components/SummaryCards";

const PAGE_SIZE = 10;

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [refreshCharts, setRefreshCharts] = useState(0); // for charts
  const progressIntervalRef = useRef(null);

  // for loader % and progress
  const [progress, setProgress] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);

  const isAuthenticated = localStorage.getItem("isAuthenticated");
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  const startFakeProgress = () => {
    setProgress(0);
    progressIntervalRef.current = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) return prev; // stop at 90%
        return prev + Math.random() * 5;
      });
    }, 600);
  };

  const stopFakeProgress = () => {
    clearInterval(progressIntervalRef.current);
    setProgress(100);
    setTimeout(() => setProgress(0), 800);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);
    setCurrentPage(1);
    localStorage.removeItem("anomalyResult");
    const formData = new FormData();
    formData.append("file", file);

    startFakeProgress();

    try {
      const response = await fetch("http://127.0.0.1:8000/detect-upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      stopFakeProgress();

      setResult(data);
      localStorage.setItem("anomalyResult", JSON.stringify(data));
      setRefreshCharts((prev) => prev + 1);
    } catch (err) {
      clearInterval(progressIntervalRef.current);
      setError("Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const savedResult = localStorage.getItem("anomalyResult");
    if (savedResult) {
      setResult(JSON.parse(savedResult));
    }
  }, []);

  // Pagination logic
  const totalPages = result
    ? Math.ceil(result.top_anomalies.length / PAGE_SIZE)
    : 0;

  const paginatedData = result
    ? result.top_anomalies.slice(
        (currentPage - 1) * PAGE_SIZE,
        currentPage * PAGE_SIZE
      )
    : [];

  return (
    <div className="min-h-screen bg-slate-100">
      {/* Header */}
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
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Upload Card */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Upload Log Dataset</h2>

          <div className="flex items-center gap-4">
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setFile(e.target.files[0])}
              className="block w-full text-sm text-gray-600
                         file:mr-4 file:py-2 file:px-4
                         file:rounded file:border-0
                         file:text-sm file:font-semibold
                         file:bg-slate-200 file:text-slate-700
                         hover:file:bg-slate-300"
            />
            <button
              onClick={handleUpload}
              className="bg-blue-600 cursor-pointer hover:bg-blue-700 text-white px-6 py-2 rounded font-medium"
            >
              Run Detection
            </button>
            {result && (
              <button
                onClick={() => {
                  localStorage.removeItem("anomalyResult");
                  setResult(null);
                }}
                className="bg-gray-400 hover:bg-gray-500 text-white px-4 py-2 rounded cursor-pointer"
              >
                Clear Results
              </button>
            )}
          </div>

          {/* Progress bar */}
          {loading && (
            <div className="mt-6">
              <p className="text-blue-600 mb-2">
                Running anomaly detection... {Math.floor(progress)}%
              </p>
              <div className="w-full bg-gray-200 rounded h-3 overflow-hidden">
                <div
                  className="bg-blue-600 h-3 transition-all duration-500"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          )}
          {/* {loading && (
            <p className="mt-4 text-blue-600">Running anomaly detection...</p>
          )} */}

          {error && <p className="mt-4 text-red-600">{error}</p>}
        </div>

        {result && (
          <Charts
            loading={loading}
            refresh={refreshCharts}
            progress={progress}
            startFakeProgress={startFakeProgress}
            stopFakeProgress={stopFakeProgress}
          />
        )}

        {/* Results */}
        {result && (
          <>
            {/* Alert Banner */}
            {result.alert && (
              <div className="bg-red-100 border border-red-300 text-red-800 px-6 py-4 rounded-lg mb-6">
                ⚠️ <strong>Security Alert:</strong> Anomalous activity detected
              </div>
            )}

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-sm text-gray-500">Total Records</p>
                <p className="text-3xl font-bold mt-1">{result.total_rows}</p>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-sm text-gray-500">Anomalies Detected</p>
                <p className="text-3xl font-bold mt-1 text-red-600">
                  {result.anomalies_detected}
                </p>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-sm text-gray-500">Email Alert</p>
                <p className="text-lg font-semibold mt-2">
                  {result.email?.sent
                    ? "Sent"
                    : result.email?.reason || "Not sent"}
                </p>
              </div>
            </div>
            {result?.summary && <SummaryCards summary={result.summary} />}

            {/* Results Table */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-semibold mb-4">
                Top Anomalous IP Addresses
              </h3>

              <div className="overflow-x-auto">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="bg-slate-200 text-slate-700">
                      <th className="text-left p-3 border">S.N.</th>
                      <th className="text-left p-3 border">IP Address</th>
                      <th className="text-left p-3 border">Score</th>
                      <th className="text-left p-3 border">Percentile</th>
                      <th className="text-left p-3 border">Severity</th>
                    </tr>
                  </thead>

                  <tbody>
                    {paginatedData.map((item, index) => (
                      <tr key={index} className="hover:bg-slate-50">
                        <td className="p-3 border">
                          {(currentPage - 1) * PAGE_SIZE + index + 1}
                        </td>
                        <td className="p-3 border">{item.ip}</td>
                        <td className="p-3 border text-red-600">
                          {item.anomaly_score.toFixed(4)}
                        </td>
                        <td className="p-3 border">
                          {item.anomaly_percentile.toFixed(2)}%
                        </td>
                        <td className="p-3 border font-semibold">
                          {item.severity}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
        {result && (
          <div className="flex justify-between items-center mt-4">
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => p - 1)}
              className="px-4 py-2 bg-indigo-500 text-white rounded disabled:opacity-50 cursor-pointer"
            >
              Previous
            </button>

            <span>
              Page {currentPage} of {totalPages}
            </span>

            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((p) => p + 1)}
              className="px-4 py-2 bg-indigo-500 text-white rounded disabled:opacity-50 cursor-pointer"
            >
              Next
            </button>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="text-center text-sm text-gray-500 py-6">
        MSc Cyber Security & AI • Unsupervised Anomaly Detection • Rabi Giri •
        21049563
      </footer>
    </div>
  );
}

export default App;
