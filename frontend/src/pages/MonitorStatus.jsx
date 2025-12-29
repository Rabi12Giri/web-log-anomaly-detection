import { useEffect, useState } from "react";
import Header from "../components/Header";
import MitigationTable from "../components/MitigationTable";

const MonitorStatus = () => {
  const [status, setStatus] = useState(null);
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStatus = async () => {
    try {
      setLoading(true);

      // Fetch monitor status
      const statusRes = await fetch("http://localhost:8000/monitor/status");
      if (!statusRes.ok) {
        throw new Error("Failed to fetch monitor status");
      }
      const statusData = await statusRes.json();
      setStatus(statusData);

      // Fetch latest detection result (for mitigation)
      const detectRes = await fetch("http://localhost:8000/detect/latest");

      if (!detectRes.ok) {
        throw new Error("Failed to fetch detection data");
      }

      const detectData = await detectRes.json();
      setAnomalies(detectData.top_anomalies || []);

      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  return (
    <>
      <Header />
      <div className="w-full bg-green-400 text-white">
        {loading && (
          <div className="p-6  text-left max-w-5xl m-auto text-xl font-semibold">
            Loading monitor status...
          </div>
        )}
      </div>

      <div className="w-full bg-red-400 text-white">
        {error && (
          <div className="p-6  text-left max-w-5xl m-auto text-xl font-semibold">
            {error}...
          </div>
        )}
      </div>
      <div className="p-6 max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">
          Automated Log Monitor Status
        </h1>

        {/* Security Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
          <div className="p-5 bg-white shadow rounded-lg">
            <p className="text-sm text-gray-500">Overall Risk Level</p>
            <p
              className={`text-xl font-bold ${
                anomalies.some((a) => a.severity === "HIGH")
                  ? "text-red-600"
                  : anomalies.some((a) => a.severity === "MEDIUM")
                  ? "text-yellow-600"
                  : "text-green-600"
              }`}
            >
              {anomalies.some((a) => a.severity === "HIGH")
                ? "HIGH"
                : anomalies.some((a) => a.severity === "MEDIUM")
                ? "MEDIUM"
                : "LOW"}
            </p>
          </div>

          <div className="p-5 bg-white shadow rounded-lg">
            <p className="text-sm text-gray-500">Detected Anomalies</p>
            <p className="text-xl font-bold">{anomalies?.length}</p>
          </div>

          <div className="p-5 bg-white shadow rounded-lg">
            <p className="text-sm text-gray-500">System State</p>
            <p className="text-xl font-bold text-green-600">
              {status?.running ? "Monitoring Active" : "Stopped"}
            </p>
          </div>
        </div>

        {/* Monitor Status Table */}
        <div className="overflow-x-auto bg-white shadow rounded-lg mb-10">
          <table className="min-w-full border border-gray-200">
            <tbody>
              <TableRow
                label="Automation Running"
                value={status?.running ? "Yes" : "No"}
              />
              <TableRow
                label="Interval (seconds)"
                value={status?.interval_seconds}
              />
              <TableRow
                label="Processed Log Chunks"
                value={status?.processed_chunks}
              />
              <TableRow
                label="Last Processed Chunk"
                value={status?.last_chunk || "N/A"}
              />
              <TableRow
                label="Last Run Time"
                value={status?.last_run || "N/A"}
              />
              <TableRow
                label="Anomaly Detected (Last Run)"
                value={
                  status?.last_anomaly_detected ? (
                    <span className="text-red-600 font-semibold">Yes</span>
                  ) : (
                    <span className="text-green-600 font-semibold">No</span>
                  )
                }
              />
            </tbody>
          </table>
        </div>

        <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-700">
          <p className="font-semibold">Analyst Action Required</p>
          <p className="text-sm">
            Review detected anomalies and decide appropriate mitigation actions.
            The system does not automatically block traffic.
          </p>
        </div>

        {/*  Mitigation Table (Human-in-the-loop) */}
        <MitigationTable anomalies={anomalies} />
      </div>
      {/* Footer */}
      <footer className="text-center text-sm text-gray-500 py-6">
        MSc Cyber Security & AI • AI-Based Web Log Anomaly Detection • Rabi Giri
        • 21049563
      </footer>
    </>
  );
};

const TableRow = ({ label, value }) => (
  <tr className="border-b">
    <td className="px-6 py-4 font-medium text-gray-700 bg-gray-50 w-1/3">
      {label}
    </td>
    <td className="px-6 py-4 text-gray-800">{value}</td>
  </tr>
);

export default MonitorStatus;
