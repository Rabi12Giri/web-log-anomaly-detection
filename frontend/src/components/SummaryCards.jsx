function SummaryCards({ summary }) {
  const cards = [
    {
      title: "Total Records",
      value: summary.total_rows,
      color: "bg-slate-100",
    },
    {
      title: "Total Anomalies",
      value: summary.anomalies_detected,
      color: "bg-red-100",
    },
    {
      title: "Critical",
      value: summary.critical_count,
      color: "bg-red-200",
    },
    {
      title: "High",
      value: summary.high_count,
      color: "bg-orange-200",
    },
    {
      title: "Medium",
      value: summary.medium_count,
      color: "bg-yellow-200",
    },
    {
      title: "Low",
      value: summary.low_count,
      color: "bg-green-200",
    },
    {
      title: "% Anomalous",
      value: `${summary.anomaly_percentage}%`,
      color: "bg-purple-200",
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 mb-8">
      {cards.map((card, index) => (
        <div
          key={index}
          className={`${card.color} rounded-lg p-4 shadow text-center`}
        >
          <p className="text-sm text-gray-700">{card.title}</p>
          <p className="text-2xl font-bold mt-1">{card.value}</p>
        </div>
      ))}
    </div>
  );
}

export default SummaryCards;
