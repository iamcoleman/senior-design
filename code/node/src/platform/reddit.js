const fetch = require('node-fetch');
const FormData = require('form-data');

const analyzeSentiment = require('../helper/analyzeSentiment');
const config = require('../../config');
const authRequestParams = {
    method: 'POST',
    headers: {
        Authorization: `Basic ${
            Buffer.from(`${config.reddit.clientId}:${config.reddit.clientSecret}`)
                .toString('base64')}`
    },
    body: new FormData()
};
authRequestParams.body.append('grant_type', 'client_credentials');

const requestParams = {
    headers: {}
};

let tokenExpirationTime;

async function search(query, options) {
    if(!tokenExpirationTime || tokenExpirationTime < process.uptime()) {
        const authResponse = await fetch('https://www.reddit.com/api/v1/access_token', authRequestParams);
        const credentials = await authResponse.json();
        tokenExpirationTime = process.uptime() + credentials.expires_in;
        requestParams.headers.Authorization = `Bearer ${credentials.access_token}`;
    }

    const url = new URL('https://oauth.reddit.com/search/.json');
    url.searchParams.append('q', `self:yes ${query}`);
    for(let key in options) {
        url.searchParams.append(key, options[key]);
    }
    if(options.limit === undefined) {
        url.searchParams.append('limit', 100);
    }

    const data = await fetch(url, requestParams);
    return data.json();
}

async function scoreWeek(query, dates) {
    const searchPromise = search(query, {
        limit: 70,
        t: 'week'
    });
    const scoresByDate = {};
    for(const date of dates) {
        scoresByDate[date] = [];
    }
    const posts = await searchPromise;
    for(const post of posts.data.children) {
        const date = new Date(post.data.created * 1000).toISOString().substring(0, 10);
        if(scoresByDate[date] !== undefined) {
            scoresByDate[date].push(analyzeSentiment(post.data.selftext));
        }
    }
    const scores = [];
    for(const date of dates) {
        const scorePromises = scoresByDate[date];
        if(scorePromises.length === 0) {
            scores.push('no data');
        } else {
            const dateScores = await Promise.all(scorePromises);
            scores.push(Math.round(dateScores.reduce((a, b) => a + b) / dateScores.length));
        }
    }
    return scores;
}

module.exports = { search, scoreWeek };
