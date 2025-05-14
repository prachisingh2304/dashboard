const dateFields = ['doj', 'exit_date', 'timestamp', 'assigned_date', 'expiry_date'];

function formatDate(dateString) {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString; // If invalid date, return as-is
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const dd = String(date.getDate()).padStart(2, '0');
    const yyyy = date.getFullYear();
    return `${mm}/${dd}/${yyyy}`;
}

// Optional: Use this to customize labels
const customColumnLabels = {
    full_name: 'Agent Name',
    total_call_attempt: 'Total Calls',
    total_call_duration: 'Total Duration (mins)',
    call_back_later: 'Call Back Later',
    not_connected: 'Not Connected',
    unique_dialed: 'Unique Dialed',
    time_clock_hrs: 'Shift Time',
    email_id: 'Email ID',
    doj: 'Date of Joining',
    exit_date: 'Exit Date',
    phone_number: 'Phone Number',
    google_drive_link: 'Drive Link',
    reminder_status: 'Reminder Status',
    agent_name: 'Agent Name',
    agent_email: 'Email',
    agent_status: 'Status',
    key_assigned: 'Assigned Key',
    assigned_date: 'Assigned Date',
    expiry_date: 'Expiry Date'
};

// Define custom column order per table (if desired)
const tableColumnOrder = {
    onboarding: [
        'id', 'timestamp', 'email_address', 'full_name', 'phone_number', 'email_id',
        'job_position', 'google_drive_link', 'last_in_hand_salary', 'interview_status',
        'reminder_status', 'results', 'salary', 'doj', 'exit_date', 'days_left'
    ],
    agents: [
        'agent', 'status', 'time_clock_hrs', 'total_call_attempt',
        'connected', 'not_connected', 'call_back_later',
        'total_call_duration', 'unique_dialed'
    ],
    calls: ['call_id','agent','duration','phone','connected_status','call_back_status','date_time'

    ]
 

};

function renderTable(data) {
    const header = document.getElementById("table-header");
    const body = document.getElementById("table-body");

    if (!data || data.length === 0) {
        header.innerHTML = "";
        body.innerHTML = "<tr><td colspan='100'>No data available</td></tr>";
        return;
    }

    // Detect current table name from global variable (defined in main.js)
    const headers = (tableColumnOrder[currentTable] || Object.keys(data[0])).filter(key => key in data[0]);

    // Create table header row
    const headerRow = headers
        .map(h => `<th>${customColumnLabels[h] || h.replace(/_/g, " ").toUpperCase()}</th>`)
        .join("");
    header.innerHTML = `<tr>${headerRow}</tr>`;

    // Create table body rows
    const bodyRows = data
        .map(row => {
            return `<tr>${headers.map(h => {
                let cellValue = row[h];
                if (cellValue !== null && cellValue !== undefined) {
                    if (dateFields.includes(h)) {
                        cellValue = formatDate(cellValue);
                    }
                } else {
                    cellValue = "";
                }
                return `<td title="${row[h] || ''}">${cellValue}</td>`;
            }).join("")}</tr>`;
        })
        .join("");

    body.innerHTML = bodyRows;
}
