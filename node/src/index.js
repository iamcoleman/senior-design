const express = require('express');
const fetch = require('node-fetch');

const config = require('../config');

const app = express();
const port = config.port;
const twitterBearerToken = config.twitter.bearerToken;

function arrayWithoutDuplicates(inputArray) {
    return Array.from(new Set(inputArray));
}

app.get('/:query', async (req, res) => {
    const url = new URL('https://api.twitter.com/1.1/search/tweets.json');
    url.searchParams.append('q', req.params.query);
    url.searchParams.append('count', 100);
    url.searchParams.append('lang', 'en');

    const twitterData = await fetch(url, {
        headers: {
            Authorization: 'Bearer ' + twitterBearerToken
        }
    });
    const twitterJson = await twitterData.json();
    const tags = twitterJson.statuses
        .map(status => status.entities.hashtags)
        .reduce((a, b) => a.concat(b), [])
        .map(hashtag => hashtag.text);

    res.send({
        tags: arrayWithoutDuplicates(tags)
    });
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
