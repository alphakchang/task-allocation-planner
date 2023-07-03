const ctx = document.getElementById('kenChart');
          
new Chart(ctx, {
    type: 'bar',
    data: {
    labels: ['Hours'],
    datasets: [{
        label: '4-7-2023',
        data: [6.8],
        borderWidth: 1
    }]
    },
    options: {
    scales: {
        y: {
            beginAtZero: true,
            suggestedMax: 8
        }
    }
    }
});

const ctx2 = document.getElementById('oldKenChart');
          
new Chart(ctx2, {
    type: 'bar',
    data: {
    labels: ['Hours'],
    datasets: [{
        label: '4-7-2023',
        data: [2.5],
        borderWidth: 1
    }]
    },
    options: {
    scales: {
        y: {
            beginAtZero: true,
            suggestedMax: 8
        }
    }
    }
});