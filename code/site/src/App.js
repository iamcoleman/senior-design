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
    setData(await (await fetch(`/api/sentiment/query/${encodeURIComponent(query)}`)).json());
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
        <>
          <p style={{ textAlign: 'center' }}>Related hashtags: {
            data.hashtags.length === 0 ? 'None' : data.hashtags
              .map((tag, i) => <>
                <a href={`https://twitter.com/search?q=%23${tag}`} target="_blank" rel="noreferrer">#{tag}</a>
                {i === data.hashtags.length - 1 ? '' : ', '}
              </>)
          }</p>
          <div className="chart">
            <Line data={{
              labels: data.twitter.map(day => day.date),
              datasets: [{
                label: 'Twitter',
                backgroundColor: 'rgba(75,162,162,0.1)',
                borderColor: 'rgba(75,162,162,1)',
                data: data.twitter.map(day => day.score)
              }, {
                label: 'Reddit',
                backgroundColor: 'rgba(190,75,75,0.1)',
                borderColor: 'rgba(190,75,75,1)',
                data: data.reddit.map(day => day.score)
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
        </>
      }
    </>
  );
}

export default App;
