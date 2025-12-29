import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

function Charts({ refresh, progress, startFakeProgress, stopFakeProgress }) {
  const [version, setVersion] = useState(Date.now());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [imagesLoaded, setImagesLoaded] = useState(0);
  const totalImages = 3;

  useEffect(() => {
    const generateCharts = async () => {
      startFakeProgress();
      try {
        setLoading(true);
        setError("");
        setImagesLoaded(0);

        // Fetch ALL chart APIs in parallel
        await fetch(`${API_BASE}/charts/anomaly-score-distribution`);
        await fetch(`${API_BASE}/charts/anomaly-count`);
        await fetch(`${API_BASE}/charts/top-anomalies`);

        stopFakeProgress();
        // Update cache  AFTER charts are created
        setVersion(Date.now());
      } catch (err) {
        setError("Failed to generate charts");
        setLoading(false);
      } finally {
        setLoading(false);
      }
    };

    generateCharts();
  }, [refresh]);

  useEffect(() => {
    if (imagesLoaded === totalImages) {
      setLoading(false);
    }
  }, [imagesLoaded]);

  if (error) {
    return <p className="text-red-600 mt-6">{error}</p>;
  }

  return (
    <>
      {loading && (
        <div className="mt-6 mb-6">
          <p className="text-blue-600 mb-2">
            Generating charts... {Math.floor(progress)}%
          </p>
          <div className="w-full bg-gray-200 rounded h-3 overflow-hidden">
            <div
              className="bg-blue-600 h-3 transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {!loading && (
        <div className="mt-10 mb-10">
          <h2 className="text-2xl font-semibold mb-6">
            Anomaly Detection Visualisations
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Chart
              title="Anomaly Score Distribution"
              src={`${API_BASE}/charts/anomaly_score_distribution.png?v=${version}`}
              onLoad={() => setImagesLoaded((c) => c + 1)}
            />
            <Chart
              title="Normal vs Anomalous Traffic"
              src={`${API_BASE}/charts/anomaly_count.png?v=${version}`}
              onLoad={() => setImagesLoaded((c) => c + 1)}
            />
            <Chart
              title="Top Anomalous IPs"
              src={`${API_BASE}/charts/top_anomalies.png?v=${version}`}
              onLoad={() => setImagesLoaded((c) => c + 1)}
            />
          </div>
        </div>
      )}
    </>
  );
}

function Chart({ title, src, onLoad }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="text-lg font-medium mb-3">{title}</h3>
      <a href={src} target="__blank">
        <img
          src={src}
          alt={title}
          onLoad={onLoad}
          className="w-full border rounded"
        />
      </a>
    </div>
  );
}

export default Charts;
