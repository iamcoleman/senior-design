const express = require('express');

const config = require('../config');
const twitter = require('./platform/twitter');
const reddit = require('./platform/reddit');
const tumblr = require('./platform/tumblr');
const sentimentEngine = require('./sentimentEngine');

const app = express();
const { port } = config;

app.use(express.json());
app.use(express.static('public'));

app.post('/api/sentiment/query/:query', async (req, res) => {
    const { query } = req.params;
    const jobPromise = sentimentEngine.createJob(query);

    const date = new Date();
    date.setDate(date.getDate() - 6);
    const dates = [date.toISOString().substring(0, 10)];
    for(let i = 0; i < 6; i++) {
        date.setDate(date.getDate() + 1);
        dates.push(date.toISOString().substring(0, 10));
    }

    const analysisRequestId = await jobPromise;

    if(query.charAt(0) === '#') {
        tumblr.scoreWeekByTag(analysisRequestId, query.slice(1), dates);
    } else {
        sentimentEngine.allPostsSent(analysisRequestId, 'tumblr');
    }
    reddit.scoreWeek(analysisRequestId, query, dates);
    const hashtags = await twitter.scoreWeek(analysisRequestId, query, dates);
    res.send({ analysisRequestId, hashtags });
});

const platforms = ['twitter', 'reddit', 'tumblr'];

async function getResults(analysisRequestId) {
    const results = await sentimentEngine.getResults(analysisRequestId);
    results.sort((a, b) => a.result_day.localeCompare(b.result_day));
    const dates = [];
    const scores = {};
    for(const platform of platforms) {
        scores[platform] = [];
    }
    for(const result of results) {
        dates.push(result.result_day);
        for(const platform of platforms) {
            scores[platform].push({
                score: result[`${platform}_median`] * 100,
                lowerQuartile: result[`${platform}_lower_quartile`] * 100,
                upperQuartile: result[`${platform}_upper_quartile`] * 100
            });
        }
    }
    return { dates, scores };
}

app.get('/api/results/:analysisRequestId', async (req, res) => {
    const { analysisRequestId } = req.params;
    const status = await sentimentEngine.getStatus(analysisRequestId);
    console.log(status);
    switch(status) {
        case 'READY':
            res.send(await getResults(analysisRequestId));
            break;
        case 'FAILURE':
            res.status(500).send({ message: 'Sentiment analysis failed' });
            break;
        default:
            res.send({ pending: true });
            break;
    }
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
