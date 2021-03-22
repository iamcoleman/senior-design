const fetch = require('node-fetch');

const sentimentEngine = require('../sentimentEngine');
const config = require('../../config');
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

async function scoreDateByTag(analysisRequestId, tag, date, dayAfter) {
    const options = {
        count: 10
    };
    if(dayAfter !== undefined) {
        options.before = new Date(dayAfter).getTime() / 1000;
    }
    const posts = await searchTag(tag, options);
    const postsForEngine = [];
    for(let response of posts.response) {
        const postDate = response.date.substring(0, 10);
        if(postDate !== date) {
            break;
        }
        if(response.body) {
            postsForEngine.push({
                created_at: postDate,
                text: response.body
            });
        }
    }

    return sentimentEngine.analyzePosts(analysisRequestId, 'tumblr', postsForEngine);
}

async function scoreWeekByTag(analysisRequestId, tag, dates) {
    const analysisPromises = [];
    for(let i = 0; i < 7; i++) {
        analysisPromises.push(scoreDateByTag(analysisRequestId, tag, dates[i], dates[i + 1]));
    }
    await Promise.all(analysisPromises);
    sentimentEngine.allPostsSent(analysisRequestId, 'tumblr');
}

module.exports = { searchTag, scoreWeekByTag };
