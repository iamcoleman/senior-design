import React, { useState } from 'react';
import SentimentChart from '../SentimentChart/SentimentChart';
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
          <SentimentChart dates={data.dates} datasets={data.scores} searchTerm={searched} />
        </>
      }
    </>
  );
}

export default App;
