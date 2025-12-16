import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

function Charts({ refresh }) {
  const [version, setVersion] = useState(Date.now());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const generateCharts = async () => {
      try {
        setLoading(true);
        setError("");

        await fetch(`${API_BASE}/charts/anomaly-score-distribution`);
        await fetch(`${API_BASE}/charts/anomaly-count`);
        await fetch(`${API_BASE}/charts/top-anomalies`);

        // Update cache  AFTER charts are created
        setVersion(Date.now());
      } catch (err) {
        setError("Failed to generate charts");
      } finally {
        setLoading(false);
      }
    };

    generateCharts();
  }, [refresh]);

  if (loading) {
    return <p className="text-blue-600 mt-6">Generating charts...</p>;
  }

  if (error) {
    return <p className="text-red-600 mt-6">{error}</p>;
  }

  return (
    <div className="mt-10 mb-10">
      <h2 className="text-2xl font-semibold mb-6">
        Anomaly Detection Visualisations
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Chart
          title="Anomaly Score Distribution"
          src={`${API_BASE}/charts/anomaly_score_distribution.png?v=${version}`}
        />
        <Chart
          title="Normal vs Anomalous Traffic"
          src={`${API_BASE}/charts/anomaly_count.png?v=${version}`}
        />
        <Chart
          title="Top Anomalous IPs"
          src={`${API_BASE}/charts/top_anomalies.png?v=${version}`}
        />
      </div>
    </div>
  );
}

function Chart({ title, src }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="text-lg font-medium mb-3">{title}</h3>
      <img src={src} alt={title} className="w-full border rounded" />
    </div>
  );
}

export default Charts;
