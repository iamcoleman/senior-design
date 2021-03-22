import React, { useState } from 'react';
import searchQuery from '../../api/searchQuery';
import SentimentChart from '../SentimentChart/SentimentChart';
import TagDisplay from '../TagDisplay/TagDisplay';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [searched, setSearched] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [display, setDisplay] = useState('all');

  const search = async (searchText) => {
    setLoading(true);
    setData(await searchQuery(searchText));
    setSearched(searchText);
    setLoading(false);
  }

  const submitSearchForm = (e) => {
    e.preventDefault();
    search(query);
  }

  const searchTag = (tag) => {
    const searchText = `#${tag}`;
    setQuery(searchText);
    search(searchText);
  }

  let datasets, datasetNames;
  if(data !== null) {
    datasetNames = Object.keys(data.scores);
    switch(display) {
      case 'all':
        datasets = data.scores;
        break;
      case 'average':
        const dataset = [];
        const inputDatasets = [];
        for(const datasetName in data.scores) {
          inputDatasets.push(data.scores[datasetName]);
        }
        for(let i = 0; i < 7; i++) {
          let score = 0;
          let count = 0;
          let lowTotal = 0;
          let highTotal = 0;
          for(const inputDataset of inputDatasets) {
            const inputPoint = inputDataset[i];
            if(inputPoint.score === undefined) {
              continue;
            }
            score += inputPoint.score * inputPoint.count;
            count += inputPoint.count;
            lowTotal += inputPoint.lowAverage * inputPoint.count;
            highTotal += inputPoint.highAverage * inputPoint.count;
          }
          if(count === 0) {
            dataset.push({ count });
          } else {
            dataset.push({
              score: score / count,
              count,
              lowAverage: lowTotal / count,
              highAverage: highTotal / count
            });
          }
        }
        datasets = { average: dataset }
        break;
      default:
        if(data.scores[display] === undefined) {
          setDisplay('all');
          datasets = data.scores;
        } else {
          datasets = {};
          datasets[display] = data.scores[display];
        }
        break;
    }
  }

  return (
    <main>
      <h1 className="title">Sentiment Analysis</h1>
      <form className="searchForm" onSubmit={submitSearchForm}>
        <input className="searchField" type="text" value={query} onChange={e => setQuery(e.target.value)} disabled={loading} />
        <button className="searchButton" type="submit" disabled={loading}>Search</button>
      </form>
      {data !== null &&
        <>
          <TagDisplay hashtags={data.hashtags} searchTag={searchTag} />
          <select value={display} onChange={(e) => setDisplay(e.target.value)}>
            <option value="all">All</option>
            <option value="average">Average</option>
            {datasetNames.map((datasetName) => (
              <option value={datasetName}>
                {datasetName.charAt(0).toUpperCase()}
                {datasetName.slice(1)}
              </option>))}
          </select>
          <SentimentChart dates={data.dates} datasets={datasets} searchTerm={searched} />
        </>
      }
    </main>
  );
}

export default App;
