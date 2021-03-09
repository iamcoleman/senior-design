import React from 'react';
import { Line } from 'react-chartjs-2';
import './SentimentChart.css';

const colors = {
  twitter: '29,161,242',
  reddit: '255,86,0',
  tumblr: '52,82,111',
  average: '75,162,162'
}

function SentimentChart(props) {
  const datasets = [];
  const rawDatasets = [];
  let i = 0;
  for(const datasetName in props.datasets) {
    const upperName = `${datasetName.charAt(0).toUpperCase()}${datasetName.slice(1)}`;
    const rawDataset = props.datasets[datasetName];
    rawDatasets.push(rawDataset);
    const dataset = {
      label: upperName,
      data: rawDataset.map((datapoint) => datapoint.score),
      fill: false
    };
    const lowerBoundDataset = {
      label: `${upperName} low average`,
      data: rawDataset.map((datapoint) => datapoint.lowAverage),
      borderColor: 'transparent',
      pointRadius: 0,
      fill: i,
    };
    const upperBoundDataset = {
      label: `${upperName} high average`,
      data: rawDataset.map((datapoint) => datapoint.highAverage),
      borderColor: 'transparent',
      pointRadius: 0,
      fill: i,
    };
    const color = colors[datasetName];
    if(color !== undefined) {
      dataset.borderColor = `rgba(${color},1)`;
      lowerBoundDataset.backgroundColor = `rgba(${color},0.1)`;
      upperBoundDataset.backgroundColor = `rgba(${color},0.1)`;
    }
    datasets.push(dataset);
    datasets.push(lowerBoundDataset);
    datasets.push(upperBoundDataset);
    i += 3;
  }

  return (
    <div className="chart">
      <Line data={{
        labels: props.dates,
        datasets: datasets
      }}
      width={1000}
      height={500}
      options={{
        title: {
          display: true,
          text: `Sentiment for "${props.searchTerm}"`,
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
            filter: (item) => !item.text.includes(' average')
          }
        },
        tooltips: {
          filter: (tooltipItem) => tooltipItem.datasetIndex % 3 === 0,
          callbacks: {
            label: (tooltipItem) => {
              const dataset = datasets[tooltipItem.datasetIndex];
              let score = parseFloat(tooltipItem.value).toFixed(1);
              if(/\.0$/.test(score)) {
                score = score.slice(0, -2);
              }
              return `${dataset.label} score: ${score}`;
            },
            afterLabel: (tooltipItem) => {
              const rawDataset = rawDatasets[tooltipItem.datasetIndex / 3];
              return `Analyzed ${rawDataset[tooltipItem.index].count} posts`;
            }
          }
        }
      }} />
    </div>
  );
}

export default SentimentChart;
