const fetch = require('node-fetch');

const sentimentEngine = require('../sentimentEngine');
const config = require('../../config');
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

async function scoreDate(analysisRequestId, query, date, dayAfter) {
    const options = {
        count: 10
    };
    if(dayAfter !== undefined) {
        options.until = dayAfter;
    }
    const posts = await search(query, options);
    const postsForEngine = [];
    const hashtags = new Set();
    for(let status of posts.statuses) {
        const postDate = new Date(status.created_at).toISOString().substring(0, 10);
        if(postDate !== date) {
            break;
        }
        postsForEngine.push({
            created_at: date,
            text: status.text
        });
        for(tag of status.entities.hashtags) {
            hashtags.add(tag.text);
        }
    }

    await sentimentEngine.analyzeTweets(analysisRequestId, postsForEngine);
    return hashtags;
}

async function scoreWeek(analysisRequestId, query, dates) {
    const analysisPromises = [];
    for(let i = 0; i < 7; i++) {
        analysisPromises.push(scoreDate(analysisRequestId, query, dates[i], dates[i + 1]));
    }
    const lowercaseHashtags = new Set();
    const hashtags = [];
    for(const analysisPromise of analysisPromises) {
        const hashtagsForDate = await analysisPromise;
        for(const tag of hashtagsForDate) {
            const lowerText = tag.toLowerCase();
            if(!lowercaseHashtags.has(lowerText)) {
                lowercaseHashtags.add(lowerText);
                hashtags.push(tag);
            }
        }
    }
    return hashtags;
}

module.exports = { search, scoreWeek };
