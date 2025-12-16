import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

function Charts() {
  const charts = [
    {
      title: "Anomaly Score Distribution",
      img: "/temp/charts/anomaly_score_distribution.png",
    },
    {
      title: "Normal vs Anomalous Traffic",
      img: "/temp/charts/anomaly_count.png",
    },
    {
      title: "Top Anomalous IPs",
      img: "/temp/charts/top_anomalies.png",
    },
  ];

  return (
    <div className="mt-10">
      <h2 className="text-2xl font-semibold mb-6">
        Anomaly Detection Visualisations
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {charts.map((chart, index) => (
          <div key={index} className="bg-white p-4 rounded-lg shadow">
            <h3 className="text-lg font-medium mb-3">{chart.title}</h3>
            {console.log(chart)}
            <a href={API_BASE + chart.img + `?t=${Date.now()}`} target="_blank">
              <img
                src={API_BASE + chart.img + `?t=${Date.now()}`}
                alt={chart.title}
                className="w-full border rounded"
              />
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Charts;
