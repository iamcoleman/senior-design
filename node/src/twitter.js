const fetch = require('node-fetch');

const config = require('../config');
const { bearerToken } = config.twitter;

const requestParams = {
    headers: {
        Authorization: `Bearer ${bearerToken}`
    }
};

async function search(query) {
    const url = new URL('https://api.twitter.com/1.1/search/tweets.json');
    url.searchParams.append('q', query);
    url.searchParams.append('count', 100);
    url.searchParams.append('lang', 'en');

    const data = await fetch(url, requestParams);
    return data.json();
}

module.exports = { search };
