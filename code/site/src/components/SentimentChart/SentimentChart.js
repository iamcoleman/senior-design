import React from 'react';
import { Line } from 'react-chartjs-2';
import './SentimentChart.css';

const colors = {
  twitter: '29,161,242',
  reddit: '255,86,0',
  tumblr: '52,82,111'
}

function SentimentChart(props) {
  return (
    <div className="chart">
      <Line data={{
        labels: props.dates,
        datasets: Object.keys(props.datasets).map((datasetName) => {
          const dataset = {
            label: `${datasetName.charAt(0).toUpperCase()}${datasetName.slice(1)}`,
            data: props.datasets[datasetName]
          };
          const color = colors[datasetName];
          if(color !== undefined) {
            dataset.backgroundColor = `rgba(${color},0.1)`;
            dataset.borderColor = `rgba(${color},1)`;
          }
          return dataset;
        })
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
              max: 100
            }
          }]
        }
      }} />
    </div>
  );
}

export default SentimentChart;
