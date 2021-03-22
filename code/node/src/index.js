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
    }
    reddit.scoreWeek(analysisRequestId, query, dates);
    const hashtags = await twitter.scoreWeek(analysisRequestId, query, dates);
    res.send({ analysisRequestId, hashtags, dates });
});

app.get('/api/results/:analysisRequestId', async (req, res) => {
    const { analysisRequestId } = req.params;
    const response = await sentimentEngine.getResults(analysisRequestId);
    res.status(response.code).send(response.body);
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
