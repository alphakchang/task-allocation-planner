const skillsArray = ["Translation", "Review", "LSO", "Client Meeting", "Time Management", "Teamwork"];
let skillsValue = [75, 90, 30, 0, 95, 40];

const ctx = document.getElementById('linguistSkills');

const config = {
    type: 'radar',
    data: {
        labels: skillsArray,
        datasets: [{
            label: 'Skills',
            data: skillsValue,
        }]
    },
    options: {
        elements: {
            line: {
                borderWidth: 3
            }
        },
        scales: {
            r: {
                angleLines: {
                    display: false
                },
                suggestedMin: 0,
                suggestedMax: 100
            }
        }
    }

};

// Client Experience Bar

let clients = ["EBAY", "BURB", "AMZN"];
let clientCount = [128, 76, 30];

const clientExp = document.getElementById('clientExp');

new Chart(clientExp, {
    type: 'bar',
    data: {
        labels: clients,
        datasets: [{
            label: 'Client Experience',
            data: clientCount,
            borderWidth: 1.5
        }]
    },
    options: {
        indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true,
            }
        },
        layout: {
            padding: {
                left: 20,
                right: 20,
            }
        }
    }
});

window.onload = function() {
    window.myRadar = new Chart(ctx, config);
};



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