import { useState } from "react";
import Charts from "./components/Charts";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [refreshCharts, setRefreshCharts] = useState(0); // for charts

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/detect-upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      setResult(data);
      setRefreshCharts((prev) => prev + 1);
    } catch (err) {
      setError("Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100">
      {/* Header */}
      <header className="bg-slate-900 text-white py-6 shadow">
        <div className="max-w-6xl mx-auto px-4">
          <h1 className="text-3xl font-bold">
            AI-Based Web Log Anomaly Detection
          </h1>
          <p className="text-slate-300 mt-1">
            Unsupervised Intrusion Detection System
          </p>
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
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded font-medium"
            >
              Run Detection
            </button>
          </div>

          {loading && (
            <p className="mt-4 text-blue-600">Running anomaly detection...</p>
          )}

          {error && <p className="mt-4 text-red-600">{error}</p>}
        </div>

        {result && <Charts refresh={refreshCharts} />}

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
                      <th className="text-left p-3 border">Anomaly Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.top_anomalies.map((item, index) => (
                      <tr key={index} className="hover:bg-slate-50">
                        <td className="p-3 border font-mono">{index + 1}</td>
                        <td className="p-3 border font-mono">{item.ip}</td>
                        <td className="p-3 border">
                          {item.anomaly_score.toFixed(4)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="text-center text-sm text-gray-500 py-6">
        MSc Cyber Security & AI • Unsupervised Anomaly Detection • Rabi Giri -
        21049563
      </footer>
    </div>
  );
}

export default App;
