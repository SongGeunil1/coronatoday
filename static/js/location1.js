var ctx = document.getElementById('myChart').getContext('2d');
var data = {
    type: 'line',
    data: {
        labels: ["7일 전", "6일 전", "5일 전", "4일 전","3일 전", "2일 전","하루 전"],
        datasets: [{
            label: "확진자 방문자 수",
            backgroundColor: "#F9A729",
            fill:false,
            borderColor: "#F9A729",
            lineTension:0.5,
            data: [0,0,0,0,0,0,0],
        }]
    },
    options: {
        title: {
            display: true,
            fontSize: 18,
            text: '확진자 방문자 수',
            fontFamily: 'MapoPeacefull'
        },
        responsive: true,
        maintainAspectRatio: false,
        legend:{
            display: false,
        labels:{
                fontSize: 12,
                fontFamily: 'MapoPeacefull'
            }
        },
        scales: {
            yAxes: [{
                ticks: {
                stepSize: 1,
                unitStepSize: 1,
                suggestedMin: 0,
                beginAtZero: true
                }
            }]
        }
    }
}
var chart = new Chart(ctx, data);




var ctx = document.getElementById('myChart2').getContext('2d');
var data = {
    type: 'bar',
    data: {
        labels: ['1km 내','2km 내','3km 내','4km 내','5km 내'],
        datasets: [{
            label: "반경 내 확진자 수",
            backgroundColor: "#F9A729",
            fill:false,
            borderColor: "#F9A729",
            lineTension:0.5,
            data: [0, 0,0,0,0],
        }]

    },
    options: {
        title: {
            display: true,
            fontSize: 18,
            text: '반경 내 확진자 수',
            fontFamily: 'MapoPeacefull'
        },
        legend:{
            display: false,
        labels:{
                fontSize: 12,
                fontFamily: 'MapoPeacefull'
            }
        },
        responsive: true, 
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                stepSize: 2,
                unitStepSize: 2,
                suggestedMin: 0
                }
            }]
        }
    }
}
var chart = new Chart(ctx, data);
