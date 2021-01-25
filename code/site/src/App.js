import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [searched, setSearched] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const search = async (e) => {
    e.preventDefault();
    setSearched(query);
    setLoading(true);
    setData(await (await fetch(`/sentiment/query/${encodeURIComponent(query)}`)).json());
    setLoading(false);
  }

  return (
    <>
      <h1 className="title">Sentiment Analysis</h1>
      <form className="searchForm" onSubmit={search}>
        <input className="searchField" type="text" value={query} onChange={e => setQuery(e.target.value)} disabled={loading} />
        <button className="searchButton" type="submit" disabled={loading}>Search</button>
      </form>
      {data !== null &&
        <div className="chart">
          <Line data={{
            labels: data.map(day => day.date),
            datasets: [{
              backgroundColor: 'rgba(75,162,162,0.1)',
              borderColor: 'rgba(75,162,162,1)',
              data: data.map(day => day.score)
            }]
          }}
          width={1000}
          height={500}
          options={{
            title: {
              display: true,
              text: `Sentiment for "${searched}"`,
              fontSize: 20
            },
            legend: {
              display: false
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
      }
    </>
  );
}

export default App;
