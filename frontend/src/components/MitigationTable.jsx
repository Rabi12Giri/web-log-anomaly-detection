const MitigationTable = ({ anomalies }) => {
  if (!anomalies || anomalies.length === 0) {
    return (
      <div className="mt-10 p-6 bg-green-50 border border-green-200 rounded-lg text-green-700">
        <h3 className="font-semibold text-lg mb-1">No Mitigation Required</h3>
        <p className="text-sm">
          No anomalous activity detected in the latest analysis cycle.
        </p>
      </div>
    );
  }

  // Helper: derive reason from mitigation text
  const deriveReason = (mitigation) => {
    if (mitigation.some((m) => m.toLowerCase().includes("rate"))) {
      return "Abnormally high request volume detected";
    }
    if (mitigation.some((m) => m.toLowerCase().includes("error"))) {
      return "Suspicious probing or malformed request behavior";
    }
    if (mitigation.some((m) => m.toLowerCase().includes("crawl"))) {
      return "Potential automated crawling or brute-force attempt";
    }
    return "Unusual traffic pattern detected";
  };

  const severityBadge = (severity) => {
    const base = "px-3 py-1 rounded-full text-xs font-semibold";
    if (severity === "HIGH") return `${base} bg-red-100 text-red-700`;
    if (severity === "MEDIUM") return `${base} bg-yellow-100 text-yellow-700`;
    return `${base} bg-green-100 text-green-700`;
  };

  return (
    <div className="mt-12">
      <h2 className="text-xl font-semibold mb-4">
        Mitigation Recommendations{" "}
        <span className="text-sm text-gray-500">(Human-in-the-loop)</span>
      </h2>

      <div className="overflow-x-auto bg-white shadow rounded-lg">
        <table className="min-w-full border border-gray-200 text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-3 text-left">S.N</th>
              <th className="px-4 py-3 text-left">IP Address</th>
              <th className="px-4 py-3 text-left">Severity</th>
              <th className="px-4 py-3 text-left">Reason</th>
              <th className="px-4 py-3 text-left">Recommended Action</th>
              <th className="px-4 py-3 text-left">Mitigation Type</th>
            </tr>
          </thead>

          <tbody>
            {anomalies.map((item, index) => (
              <tr key={index} className="border-t hover:bg-gray-50">
                {/* S.N */}
                <td className="px-4 py-3">{index + 1}</td>

                {/* IP */}
                <td className="px-4 py-3 font-mono">{item.ip}</td>

                {/* Severity */}
                <td className="px-4 py-3">
                  <span className={severityBadge(item.severity)}>
                    {item.severity}
                  </span>
                </td>

                {/* Reason */}
                <td className="px-4 py-3 text-gray-700">
                  {deriveReason(item.mitigation)}
                </td>

                {/* Mitigation actions */}
                <td className="px-4 py-3">
                  <ul className="list-disc ml-5 space-y-1">
                    {item.mitigation.map((m, i) => (
                      <li key={i}>{m}</li>
                    ))}
                  </ul>
                </td>

                {/* Mitigation type */}
                <td className="px-4 py-3 text-gray-600">
                  {item.severity === "HIGH"
                    ? "Preventive"
                    : item.severity === "MEDIUM"
                    ? "Detective"
                    : "Monitoring"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MitigationTable;
