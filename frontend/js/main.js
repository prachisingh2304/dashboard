const API_URL = "http://127.0.0.1:5000/api"; // Update with deployed URL (e.g., Vercel)
// const API_URL = "https://sherlocks-v3.onrender.com/api"
let currentTable = "agents";
let daysFilter = 0; // Default to show all calls

document.getElementById("table-select").addEventListener("change", (e) => {
    currentTable = e.target.value;
    // Show filter container only for calls table 
    document.getElementById("filter-container").style.display = currentTable === "calls" ? "block" : "none";
    // Reset filter and error on table change
    document.getElementById("days-filter").value = "";
    document.getElementById("filter-error").style.display = "none";
    daysFilter = 0;
    loadTableData();
    loadChart();
});

document.getElementById("apply-filter")?.addEventListener("click", () => {
    const daysInput = document.getElementById("days-filter").value;
    const errorSpan = document.getElementById("filter-error");

    // Validate input
    if (daysInput === "" || isNaN(daysInput) || daysInput < 0) {
        errorSpan.textContent = "Please enter a valid number (0 or positive)";
        errorSpan.style.display = "inline";
        return;
    }

    errorSpan.style.display = "none";
    daysFilter = parseInt(daysInput); // Convert to integer
    console.log(`Applying filter: past ${daysFilter} days`);
    loadTableData();
});

async function loadTableData() {
    try {
        let url = `${API_URL}/${currentTable}`;
        let response;
        let json;

        if (currentTable === "calls" && daysFilter !== 0) {
            url += `?days=${daysFilter}`;
            response = await fetch(url);
        } else if (currentTable === "calls") {
            response = await fetch(url);
        } else if (currentTable === "onboarding") {
            response = await fetch(url);
        } else if (currentTable === "key_assignment") {
            response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            });
        } else {
            response = await fetch(url);
        }

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to fetch ${currentTable} data: ${errorData.message || response.statusText}`);
        }

        json = await response.json();
        let data =[]; // Directly use json for calls data
       
        // Check the structure for each table
        if (currentTable === "key_assignment") {
            data = json.assigned_keys || [];
        } else if (currentTable === "agents" || currentTable === "onboarding") {
            data = json.data || []; // Use json.data for agents and onboarding
        } else {
            data = json || []; // Default for other tables
        }
        console.log(`Received ${data.length} records for ${currentTable}`, data);

        if (!data || data.length === 0) {
            renderTable([]);  // Ensure the table is cleared when no data
            document.getElementById("filter-error").textContent = "No data found for selected table.";
            document.getElementById("filter-error").style.display = currentTable === "calls" ? "inline" : "none";
        } else {
            document.getElementById("filter-error").style.display = "none";  // Hide error message when data is available
            renderTable(data);
        }

        document.getElementById("download-csv").style.display = data.length ? "block" : "none";
        updateChart(data);

    } catch (error) {
        console.error(`Error loading ${currentTable} data:`, error);
        renderTable([]);  // Clear table on error
        document.getElementById("filter-error").textContent = `Error: ${error.message}`;
        document.getElementById("filter-error").style.display = currentTable === "calls" ? "inline" : "none";
    }
}




// Initial load
document.getElementById("filter-container").style.display = currentTable === "calls" ? "block" : "none";
loadTableData();
