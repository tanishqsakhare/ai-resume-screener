document.addEventListener("DOMContentLoaded", function () {
  const radarLabels = JSON.parse(document.getElementById("radarChart").dataset.labels);
  const radarData = JSON.parse(document.getElementById("radarChart").dataset.data);
  const matched = parseInt(document.getElementById("skillChart").dataset.matched);
  const resumeOnly = parseInt(document.getElementById("skillChart").dataset.resumeOnly);
  const jdOnly = parseInt(document.getElementById("skillChart").dataset.jdOnly);

  // Radar Chart
  const radarCtx = document.getElementById("radarChart").getContext("2d");
  new Chart(radarCtx, {
    type: "radar",
    data: {
      labels: radarLabels,
      datasets: [{
        label: "Matched Skills by Category",
        data: radarData,
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "#36a2eb",
        pointBackgroundColor: "#36a2eb"
      }]
    },
    options: {
      responsive: true,
      scales: {
        r: {
          angleLines: { color: "rgba(128, 128, 128, 0.4)" },
          grid: {
            color: "rgba(128, 128, 128, 0.4)",
            borderColor: "#ffffff",
            lineWidth: 1.5
          },
          pointLabels: { color: "#808080" },
          ticks: {
            color: "#cccccc",
            backdropColor: "transparent"
          }
        }
      },
      plugins: {
        legend: {
          labels: { color: "#808080" }
        }
      }
    }
  });

  // Pie Chart
  const pieCtx = document.getElementById("skillChart").getContext("2d");
  new Chart(pieCtx, {
    type: "pie",
    data: {
      labels: ["Matched Skills", "Resume-only Skills", "JD-only Skills"],
      datasets: [{
        data: [matched, resumeOnly, jdOnly],
        backgroundColor: ["#28a745", "#ffc107", "#17a2b8"]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "bottom" }
      }
    }
  });
});
