window.onload = function() {
    const inputs = document.querySelectorAll("tbody tr:first-child input");
    const table = document.querySelector("table");
    const rows = Array.from(table.querySelectorAll("tbody tr:nth-child(n+2)"));

    const dateRegEx = /^\d{2}-\d{2}-\d{4}$/; // Regular Expression to check date format
    const dateTimeRegEx = /^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$/; // Regular Expression to check date and time format

    inputs.forEach((input, index) => {
        input.addEventListener("input", function() {
            // If this is the Deadline input, only run the filter if a valid date or datetime string is entered, or if the input is empty
            if (index === 3 && !dateRegEx.test(input.value) && !dateTimeRegEx.test(input.value) && input.value !== '') return;

            // Otherwise, run the filter
            filterTable();
        });
    });
	
	sortTableByDeadline();
    
	function filterTable() {
		const rows = Array.from(table.querySelectorAll("tbody tr:nth-child(n+2)")); // Get rows here
		
		rows.forEach(row => {
			let showRow = true; // we start by assuming that we should show the row

			for (let index = 0; index < inputs.length; index++) { // Replace forEach with traditional for loop
				const input = inputs[index];
				const filter = input.value.trim().toLowerCase();
				let cell = row.cells[index].innerText.toLowerCase().trim();

				if (index == 1) { // Column index for "Required Hrs" changed to 1
					cell = parseFloat(cell);
					
					// Checks if the filter includes a comparison operator
					if (filter.includes(">")) {
						const value = parseFloat(filter.split(">")[1].trim());
						showRow = cell > value;
					} else if (filter.includes("<")) {
						const value = parseFloat(filter.split("<")[1].trim());
						showRow = cell < value;
					} else if (filter.includes("=")) {
						const value = parseFloat(filter.split("=")[1].trim());
						showRow = cell === value;
					} else if (filter === "") { // When filter is empty
						showRow = true;
					} else { // For any other case, treat it as a string
						const value = parseFloat(filter);
						showRow = isNaN(value) ? false : cell === value;
					}
				} else if (index == 3) { // Column index for "Deadline"
					if (filter === "") {
						showRow = true;
					} else {
						// Convert dd-mm-yyyy HH:MM to mm/dd/yyyy HH:MM
						const cellDateParts = cell.split(' ')[0].split('-').reverse();
						const cellTimePart = cell.split(' ')[1];
						const cellDate = new Date([...cellDateParts, cellTimePart].join('/'));

						const filterDateParts = filter.split(' ')[0].split('-').reverse();
						const filterTimePart = filter.split(' ')[1] || '';
						const filterDate = new Date([...filterDateParts, filterTimePart].join('/'));

						if (isNaN(filterDate.getTime())) {
							showRow = false;
						} else {
							showRow = cellDate <= filterDate;
						}
					}
				} else {
					if (filter === "" || cell.includes(filter)) { // When filter is empty
						showRow = showRow && true;
					} else {
						showRow = false;
					}
				}

				// If showRow is false, break the loop
				if (!showRow) {
					break;
				}
			}

			row.style.display = showRow ? "" : "none";
		});
	}
    
    function sortTableByDeadline() {
        let tbody = table.querySelector('tbody');
        let rows = Array.from(tbody.querySelectorAll('tr:nth-child(n+2)')); // Get rows here, use Array.from to make it a mutable array

        // Sort rows by the Deadline column
        rows.sort((a, b) => {
            const [aDay, aMonth, aYearTime] = a.cells[3].innerText.split("-");
            const [aYear, aTime] = aYearTime.split(" ");
            const [bDay, bMonth, bYearTime] = b.cells[3].innerText.split("-");
            const [bYear, bTime] = bYearTime.split(" ");

            const aDate = new Date(aYear, aMonth - 1, aDay, ...aTime.split(":")); // month is 0-indexed
            const bDate = new Date(bYear, bMonth - 1, bDay, ...bTime.split(":")); // month is 0-indexed

            return aDate - bDate;
        });

        // Append sorted rows back to the table body
        rows.forEach(row => tbody.appendChild(row));
    }
}


/* Color mode toggle - Start */
// get colorModeToggle element
const colorModeToggle = document.getElementById('colorModeToggle');

// add event listener to colorModeToggle
colorModeToggle.addEventListener('click', () => {
    // get html element
    const html = document.querySelector('html');

    // get attribute data-bs-theme
    htmlAttribute = html.getAttribute('data-bs-theme');

    // if attribute is dark
    if (htmlAttribute === 'dark') {
        // set attribute to light
        html.setAttribute('data-bs-theme', 'light');
    }   else {
        // set attribute to dark
        html.setAttribute('data-bs-theme', 'dark');
    }
});
/* Color mode toggle - End */