// Bar chart color picker

const backgroundColors = (values, members=1) => {
    return values.map((value) => {
        if (value > 7*members) {
            return 'rgba(200, 0, 0, 0.4)'; // red
        } else if (value > 6*members) {
            return 'rgba(200, 200, 0, 0.4)'; // yellow
        } else {
            return 'rgba(0, 200, 0, 0.4)'; // green
        }
    });
};

const borderColors = (values, members=1) => {
    return values.map((value) => {
        if (value > 7*members) {
            return 'rgba(255, 0, 0, 0.9)'; // red
        } else if (value > 6*members) {
            return 'rgba(255, 255, 0, 0.9)'; // yellow
        } else {
            return 'rgba(0, 255, 0, 0.9)'; // green
        }
    });
};

/* My Workload Chart related - Start */

const weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
let dataToday = [6.8];
let dataValuesWeek = [6.8, 1.5, 0, 7.5, 2.5];
let dataValuesNextWeek = [1, 0, 2, 0, 0];
let dataValuesNextNextWeek = [0, 8, 0, 8, 0];

// Today Workload chart
const ctx = document.getElementById('myTodayChart');
          
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Hours'],
        datasets: [{
            label: '17-7-2023',
            data: dataToday,
            backgroundColor: backgroundColors(dataToday),
            borderColor: borderColors(dataToday),
            borderWidth: 1.5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                suggestedMax: 8
            }
        },
        layout: {
            padding: 20
        }
    }
});

// Weekly hours chart
const ctx_week = document.getElementById('chart_current_week');

new Chart(ctx_week, {
    type: 'bar',
    data: {
        labels: weekDays,
        datasets: [{
            label: 'Week beginning 17-7-2023',
            data: dataValuesWeek,
            backgroundColor: backgroundColors(dataValuesWeek),
            borderColor: borderColors(dataValuesWeek),
            borderWidth: 1.5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                suggestedMax: 8
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

// Next Weekly hours chart
const ctx_week2 = document.getElementById('chart_next_week');

new Chart(ctx_week2, {
    type: 'bar',
    data: {
        labels: weekDays,
        datasets: [{
            label: 'Week beginning 24-7-2023',
            data: dataValuesNextWeek,
            backgroundColor: backgroundColors(dataValuesNextWeek),
            borderColor: borderColors(dataValuesNextWeek),
            borderWidth: 1.5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                suggestedMax: 8
            }
        },
        layout: {
            padding: 10
        }
    }
});

// Next Next Weekly hours chart
const ctx_week3 = document.getElementById('chart_next_next_week');

new Chart(ctx_week3, {
    type: 'bar',
    data: {
        labels: weekDays,
        datasets: [{
            label: 'Week beginning 31-7-2023',
            data: dataValuesNextNextWeek,
            backgroundColor: backgroundColors(dataValuesNextNextWeek),
            borderColor: borderColors(dataValuesNextNextWeek),
            borderWidth: 1.5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                suggestedMax: 8
            }
        },
        layout: {
            padding: 10
        }
    }
});

/* My Workload Chart related - End */

/* Team Workload Chart related - Start */

let teamMembers = ['Ken', 'Steen', 'Alex', 'Inacio'];
let teamDataToday = [6.8, 7.7, 7.1, 7.2];
let teamDataWeek = [26.8, 24.6, 30.22, 22.5, 16.12];
let teamDataNextWeek = [5, 4.2, 2, 2, 1];
let teamDataNextNExtWeek = [0, 8, 0, 8, 0];

// Today Team Workload chart
const ctx_team = document.getElementById('teamTodayChart');
          
new Chart(ctx_team, {
    type: 'bar',
    data: {
        labels: teamMembers,
        datasets: [{
            label: '17-7-2023',
            data: teamDataToday,
            backgroundColor: backgroundColors(teamDataToday),
            borderColor: borderColors(teamDataToday),
            borderWidth: 1.5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                suggestedMax: 8
            }
        },
        layout: {
            padding: 20
        }
    }
});

// Team Weekly hours chart
const ctx_team_week = document.getElementById('team_week');

new Chart(ctx_team_week, {
    type: 'bar',
    data: {
        labels: weekDays,
        datasets: [{
            label: 'Week beginning 24-7-2023',
            data: teamDataWeek,
            backgroundColor: backgroundColors(teamDataWeek, teamMembers.length),
            borderColor: borderColors(teamDataWeek, teamMembers.length),
            borderWidth: 1.5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                suggestedMax: teamMembers.length * 8
            }
        },
        layout: {
            padding: 10
        }
    }
});

// Team Next Weekly hours chart
const ctx_team_next_week = document.getElementById('team_next_week');

new Chart(ctx_team_next_week, {
    type: 'bar',
    data: {
        labels: weekDays,
        datasets: [{
            label: 'Week beginning 24-7-2023',
            data: teamDataNextWeek,
            backgroundColor: backgroundColors(teamDataNextWeek, teamMembers.length),
            borderColor: borderColors(teamDataNextWeek, teamMembers.length),
            borderWidth: 1.5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                suggestedMax: teamMembers.length * 8
            }
        },
        layout: {
            padding: 10
        }
    }
});

// Team Next Next Weekly hours chart
const ctx_team_next_next_week = document.getElementById('team_next_next_week');

new Chart(ctx_team_next_next_week, {
    type: 'bar',
    data: {
        labels: weekDays,
        datasets: [{
            label: 'Week beginning 24-7-2023',
            data: teamDataNextNExtWeek,
            backgroundColor: backgroundColors(teamDataNextNExtWeek, teamMembers.length),
            borderColor: borderColors(teamDataNextNExtWeek, teamMembers.length),
            borderWidth: 1.5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                suggestedMax: teamMembers.length * 8
            }
        },
        layout: {
            padding: 10
        }
    }
});

/* Team Workload Chart related - End */

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

// listen for backToTop event (just in case needed)
document.addEventListener('backToTop', backToTop);

// Scroll to top function
const backToTop = () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}