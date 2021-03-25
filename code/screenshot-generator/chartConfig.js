module.exports = {
    type: 'line',
    data: {
        labels: ['2021-03-19', '2021-03-20', '2021-03-21', '2021-03-22', '2021-03-23', '2021-03-24', '2021-03-25'],
        datasets: [
            {
                "label": "Twitter",
                "data": [
                    99.37938451766968,
                    99.82855319976807,
                    99.97645616531372,
                    99.13029670715332,
                    99.99222159385681,
                    99.4616150856018,
                    38.59477639198303
                ],
                "fill": false,
                "borderColor": "rgba(29,161,242,1)"
            },
            {
                "label": "Twitter lower quartile",
                "data": [
                    97.19147443771364,
                    99.5769703388214,
                    99.92067694664001,
                    98.70130658149719,
                    99.98210668563843,
                    99.1953194141388,
                    37.82758593559266
                ],
                "borderColor": "transparent",
                "pointRadius": 0,
                "fill": 0,
                "backgroundColor": "rgba(29,161,242,0.1)"
            },
            {
                "label": "Twitter upper quartile",
                "data": [
                    99.69086050987244,
                    99.94534492492676,
                    99.98233914375305,
                    99.58243489265442,
                    99.99395370483398,
                    99.75503087043762,
                    75.43776035308835
                ],
                "borderColor": "transparent",
                "pointRadius": 0,
                "fill": 0,
                "backgroundColor": "rgba(29,161,242,0.1)"
            },
            {
                "label": "Reddit",
                "data": [
                    1.4667609706521034,
                    49.559518694877625,
                    73.74012470245361,
                    45.22465467453003,
                    43.30720901489258,
                    84.89936590194702,
                    25.016990303993225
                ],
                "fill": false,
                "borderColor": "rgba(255,86,0,1)"
            },
            {
                "label": "Reddit lower quartile",
                "data": [
                    0.062245974550023675,
                    20.00993238762023,
                    49.559518694877625,
                    0.4193184251198549,
                    23.678325116634376,
                    66.90342107787731,
                    0.4031856800429524
                ],
                "borderColor": "transparent",
                "pointRadius": 0,
                "fill": 3,
                "backgroundColor": "rgba(255,86,0,0.1)"
            },
            {
                "label": "Reddit upper quartile",
                "data": [
                    2.871275879442692,
                    79.63137149810788,
                    98.30674290657043,
                    64.90212917327878,
                    71.08465194702147,
                    89.08127069473267,
                    56.13231062889099
                ],
                "borderColor": "transparent",
                "pointRadius": 0,
                "fill": 3,
                "backgroundColor": "rgba(255,86,0,0.1)"
            },
            {
                "label": "Tumblr",
                "data": [
                    99.62456822395325,
                    99.63470697402954,
                    92.52013564109802,
                    99.13578033447266,
                    99.95775818824768,
                    17.11304634809494,
                    99.60035681724548
                ],
                "fill": false,
                "borderColor": "rgba(52,82,111,1)"
            },
            {
                "label": "Tumblr lower quartile",
                "data": [
                    99.25889730453493,
                    99.14289593696594,
                    90.7165515422821,
                    98.41833829879761,
                    82.7505633234978,
                    0.38528188597410923,
                    99.20392274856566
                ],
                "borderColor": "transparent",
                "pointRadius": 0,
                "fill": 6,
                "backgroundColor": "rgba(52,82,111,0.1)"
            },
            {
                "label": "Tumblr upper quartile",
                "data": [
                    99.69921588897705,
                    99.99252796173096,
                    95.5120575428009,
                    99.40552949905396,
                    99.96599078178406,
                    43.27052593231202,
                    99.98561143875122
                ],
                "borderColor": "transparent",
                "pointRadius": 0,
                "fill": 6,
                "backgroundColor": "rgba(52,82,111,0.1)"
            }
        ]
    },
    options: {
        animation: false,
        title: {
            display: true,
            text: `Sentiment for "#cats"`,
            fontSize: 20
        },
        elements: {
            line: {
                tension: 0 // disables bezier curves
            }
        },
        maintainAspectRatio: false,
        responsive: false,
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,
                    min: 0,
                    max: 100
                }
            }]
        },
        legend: {
            labels: {
                filter: (item) => !item.text.includes(' quartile')
            }
        },
        tooltips: {
            filter: (tooltipItem) => tooltipItem.datasetIndex % 3 === 0,
            callbacks: {
                label: (tooltipItem) => {
                    const dataset = datasets[tooltipItem.datasetIndex];
                    let score = parseFloat(tooltipItem.value).toFixed(1);
                    if (/\.0$/.test(score)) {
                        score = score.slice(0, -2);
                    }
                    return `${dataset.label} score: ${score}`;
                }
            }
        }
    }
};
