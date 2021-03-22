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

async function getResults(analysis_request_id) {
    return {
        "code": 200,
        "body": {
            "twitter": [
                {
                    "score": 49.7,
                    "count": 10,
                    "lowAverage": 34.95,
                    "highAverage": 64.45
                },
                {
                    "score": 53.6,
                    "count": 10,
                    "lowAverage": 44.55,
                    "highAverage": 67.175
                },
                {
                    "score": 39.8,
                    "count": 10,
                    "lowAverage": 30.099999999999998,
                    "highAverage": 49.5
                },
                {
                    "score": 52.4,
                    "count": 10,
                    "lowAverage": 39.6,
                    "highAverage": 65.2
                },
                {
                    "score": 42.75,
                    "count": 8,
                    "lowAverage": 35.975,
                    "highAverage": 54.041666666666664
                },
                {
                    "score": 49.1,
                    "count": 10,
                    "lowAverage": 39.38333333333333,
                    "highAverage": 63.675
                },
                {
                    "score": 45.875,
                    "count": 8,
                    "lowAverage": 33.5625,
                    "highAverage": 58.1875
                }
            ],
            "reddit": [
                {
                    "score": 58.111111111111114,
                    "count": 9,
                    "lowAverage": 46.68055555555556,
                    "highAverage": 67.25555555555556
                },
                {
                    "score": 42.61538461538461,
                    "count": 13,
                    "lowAverage": 32.24519230769231,
                    "highAverage": 59.207692307692305
                },
                {
                    "score": 60.625,
                    "count": 8,
                    "lowAverage": 51.2125,
                    "highAverage": 76.3125
                },
                {
                    "score": 62.5,
                    "count": 8,
                    "lowAverage": 49.75,
                    "highAverage": 70.15
                },
                {
                    "score": 35.1,
                    "count": 10,
                    "lowAverage": 24.96666666666667,
                    "highAverage": 50.3
                },
                {
                    "score": 48.9,
                    "count": 10,
                    "lowAverage": 36.28333333333333,
                    "highAverage": 67.825
                },
                {
                    "score": 53.5,
                    "count": 2,
                    "lowAverage": 53.25,
                    "highAverage": 53.75
                }
            ]
        }
    };
}

module.exports = { createJob, analyzePosts, allPostsSent, getResults }
