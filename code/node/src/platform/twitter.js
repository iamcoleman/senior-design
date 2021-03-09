const fetch = require('node-fetch');

const analyzeSentiment = require('../helper/analyzeSentiment');
const config = require('../../config');
const computeDataPoint = require('../helper/computeDataPoint');
const { bearerToken } = config.twitter;

const requestParams = {
    headers: {
        Authorization: `Bearer ${bearerToken}`
    }
};

async function search(query, options = {}) {
    const url = new URL('https://api.twitter.com/1.1/search/tweets.json');
    url.searchParams.append('q', query);
    url.searchParams.append('lang', 'en');
    for(let key in options) {
        url.searchParams.append(key, options[key]);
    }
    if(options.count === undefined) {
        url.searchParams.append('count', 100);
    }

    const data = await fetch(url, requestParams);
    return data.json();
}

async function scoreDate(query, date, dayAfter) {
    const options = {
        count: 10
    };
    if(dayAfter !== undefined) {
        options.until = dayAfter;
    }
    const posts = await search(query, options);
    const scorePromises = [];
    const hashtags = new Set();
    for(let status of posts.statuses) {
        const postDate = new Date(status.created_at).toISOString().substring(0, 10);
        if(postDate !== date) {
            break;
        }
        scorePromises.push(analyzeSentiment(status.text));
        for(tag of status.entities.hashtags) {
            hashtags.add(tag.text);
        }
    }

    const dataPoint = computeDataPoint(await Promise.all(scorePromises));
    return { dataPoint, hashtags };
}

async function scoreWeek(query, dates) {
    const scorePromises = [];
    for(let i = 0; i < 7; i++) {
        scorePromises.push(scoreDate(query, dates[i], dates[i + 1]));
    }
    const scores = [];
    const lowercaseHashtags = new Set();
    const hashtags = [];
    for(const scorePromise of scorePromises) {
        const result = await scorePromise;
        scores.push(result.dataPoint);
        for(const tag of result.hashtags) {
            const lowerText = tag.toLowerCase();
            if(!lowercaseHashtags.has(lowerText)) {
                lowercaseHashtags.add(lowerText);
                hashtags.push(tag);
            }
        }
    }
    return { scores, hashtags };
}

module.exports = { search, scoreWeek };
