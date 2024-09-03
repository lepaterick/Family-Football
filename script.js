// Fetch data from NCAA

async function fetchData() {
    const response = await fetch('https://www.ncaa.com/standings/football/fbs', { mode: 'no-cors' });
    const text = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(text, 'text/html');
    console.log(doc);
    const teams = [];
    const records = [];

    // List of teams to filter
    const teamList = ['Notre Dame', 'Missouri', 'Rutgers', 'Miami', 'Cornell', 'UNC'];
    // const tr_list = doc.querySelectorAll('tr');
    // console.log(tr_list);
    // Adjust the selectors based on the actual HTML structure of the page
    doc.querySelectorAll('tr').forEach(row => {
        const teamElement = row.querySelector('td.standings-team');
        // const teamElement = row.querySelector('a');
        console.log(teamElement);
        const recordElement = row.querySelector('td:nth-child(3)'); // Adjust based on actual column index

        if (teamElement && recordElement) {
            const team = teamElement.textContent.trim();
            const record = recordElement.textContent.trim();

            // Check if the team is in the list
            // if (teamList.includes(team)) {
                teams.push(team);
                records.push(record);
            // }
        }
    });
    console.log(teams, records);
    return { teams, records };
}

// Process data and create chart
async function createChart() {
    const data = await fetchData();

    const wins = data.records.map(record => parseInt(record.split('-')[0]));
    const losses = data.records.map(record => parseInt(record.split('-')[1]));

    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.teams,
            datasets: [
                {
                    label: 'Wins',
                    data: wins,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Losses',
                    data: losses,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

createChart();
