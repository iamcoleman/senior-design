const fetch = require('node-fetch');
const FormData = require('form-data');

const sentimentEngine = require('../sentimentEngine');
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
        tokenExpirationTime = process.uptime();
        const authResponse = await fetch('https://www.reddit.com/api/v1/access_token', authRequestParams);
        const credentials = await authResponse.json();
        tokenExpirationTime += credentials.expires_in;
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

async function scoreWeek(analysisRequestId, query, dates) {
    const searchPromise = search(query, {
        limit: 70,
        t: 'week'
    });
    const dateSet = new Set(dates);
    const postsForEngine = [];
    const posts = await searchPromise;
    for(const post of posts.data.children) {
        const date = new Date(post.data.created * 1000).toISOString().substring(0, 10);
        if(dateSet.has(date)) {
            postsForEngine.push({
                created_at: date,
                text: post.data.selftext
            });
        }
    }
    await sentimentEngine.analyzePosts(analysisRequestId, 'reddit', postsForEngine);
    sentimentEngine.allPostsSent(analysisRequestId, 'reddit');
}

module.exports = { search, scoreWeek };
