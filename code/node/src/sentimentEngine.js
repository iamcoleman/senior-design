const fetch = require('node-fetch');

const config = require('../../config');
const { sentimentEngineLocation } = config;

async function createJob(query) {
    let keywords;
    if(query.charAt(0) === '#') {
        keywords = [query];
    } else {
        keywords = query.match(/\S+/g);
    }
    const response = await fetch(`${sentimentEngineLocation}/engine/analysis-request`, {
        method: 'POST',
        body: { keywords }
    });
    const responseBody = await response.json();
    return responseBody.analysis_request_id;
}

function analyzeTweets(analysis_request_id, tweets) {
    return fetch(`${sentimentEngineLocation}/engine/tweets`, {
        method: 'POST',
        body: { analysis_request_id, tweets }
    });
}

async function analyzeRedditPosts(analysis_request_id, redditPosts) {
    // TODO
}

async function analyzeTumblrPosts(analysis_request_id, tumblrPosts) {
    // TODO
}

async function completeJob(analysis_request_id) {
    // TODO
}

module.exports = { createJob, analyzeTweets, analyzeRedditPosts, analyzeTumblrPosts, completeJob }
