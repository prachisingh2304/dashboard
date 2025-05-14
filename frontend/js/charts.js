let chartInstance = null;

function loadChart() {
    const canvas = document.getElementById("chart");
    if (currentTable === "agent_hourly_metrics") {
        canvas.style.display = "block";
    } else {
        canvas.style.display = "none";
    }
}

function updateChart(data) {
    const canvas = document.getElementById("chart");
    if (currentTable !== "agent_hourly_metrics" || !data || data.length === 0) {
        canvas.style.display = "none";
        if (chartInstance) chartInstance.destroy();
        return;
    }

    canvas.style.display = "block";
    const ctx = canvas.getContext("2d");
    const labels = data.map(row => row.hour_timestamp);
    const datasets = [
        {
            label: "Total Call Attempt",
            data: data.map(row => row.total_call_attempt),
            borderColor: "#27AE60",
            fill: false
        },
        {
            label: "Connected",
            data: data.map(row => row.connected),
            borderColor: "#2ECC71",
            fill: false
        }
    ];

    if (chartInstance) chartInstance.destroy();
    chartInstance = new Chart(ctx, {
        type: "line",
        data: { labels, datasets },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: "Timestamp" } },
                y: { title: { display: true, text: "Count" } }
            }
        }
    });
}