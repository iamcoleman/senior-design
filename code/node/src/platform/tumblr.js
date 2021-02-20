const fetch = require('node-fetch');

const analyzeSentiment = require('../helper/analyzeSentiment');
const config = require('../../config');
const computeDataPoint = require('../helper/computeDataPoint');
const apiKey = config.tumblr.consumerKey;

async function searchTag(tag, options) {
    const url = new URL('https://api.tumblr.com/v2/tagged');
    url.searchParams.append('tag', tag);
    url.searchParams.append('api_key', apiKey);
    for(let key in options) {
        url.searchParams.append(key, options[key]);
    }
    if(options.filter === undefined) {
        url.searchParams.append('filter', 'text');
    }

    const data = await fetch(url);
    return data.json();
}

async function scoreDateByTag(tag, date, dayAfter) {
    const options = {
        count: 10
    };
    if(dayAfter !== undefined) {
        options.before = new Date(dayAfter).getTime() / 1000;
    }
    const posts = await searchTag(tag, options);
    const scorePromises = [];
    for(let response of posts.response) {
        const postDate = response.date.substring(0, 10);
        if(postDate !== date) {
            break;
        }
        if(response.body) {
            scorePromises.push(analyzeSentiment(response.body));
        }
    }

    return computeDataPoint(await Promise.all(scorePromises));
}

function scoreWeekByTag(tag, dates) {
    const scorePromises = [];
    for(let i = 0; i < 7; i++) {
        scorePromises.push(scoreDateByTag(tag, dates[i], dates[i + 1]));
    }
    return Promise.all(scorePromises);
}

module.exports = { searchTag, scoreWeekByTag };
