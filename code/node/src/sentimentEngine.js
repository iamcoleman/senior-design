const fetch = require('node-fetch');

const config = require('../config');
const { sentimentEngineLocation } = config;
const headers = {
    'Content-Type': 'application/json'
};

async function post(path, body, retrieveBody = true) {
    const promise = fetch(`${sentimentEngineLocation}${path}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(body)
    });
    if(retrieveBody) {
        return (await promise).json();
    }
}

async function get(path) {
    const response = await fetch(`${sentimentEngineLocation}${path}`);
    return response.json();
}

async function createJob(query) {
    let keywords;
    if(query.charAt(0) === '#') {
        keywords = [query];
    } else {
        keywords = query.match(/\S+/g);
    }
    const response = await post('/engine/analysis-request', { keywords });
    return response.analysis_request_id;
}

function analyzePosts(analysis_request_id, postType, posts) {
    return post(`/engine/${postType}`, {
        analysis_request_id,
        [postType == 'tweets' ? 'tweets' : 'posts']: posts
    });
}

function allPostsSent(analysis_request_id, postType) {
    return post(`/engine/${postType}/loading-complete`, { analysis_request_id }, false);
}

async function getStatus(analysis_request_id) {
    const responseBody = await get(`/engine/analysis-request/${analysis_request_id}/status`);
    return responseBody.status;
}

async function getResults(analysis_request_id) {
    const responseBody = await get(`/engine/analysis-request/${analysis_request_id}/results`);
    return responseBody.results;
}

module.exports = { createJob, analyzePosts, allPostsSent, getStatus, getResults }
