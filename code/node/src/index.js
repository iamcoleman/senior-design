const express = require('express');

const config = require('../config');
const twitter = require('./platform/twitter');
const reddit = require('./platform/reddit');
const tumblr = require('./platform/tumblr');
const sentimentEngine = require('./sentimentEngine');

const HTTP_STATUS = {
    GONE: 410,
    SERVER_ERROR: 500
}

const app = express();
const { port, requestExpirationMillis } = config;

app.use(express.static('public'));

const activeJobs = {};

app.get('/api/sentiment/query/:query', async (req, res) => {
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

    let tumblrPromise = null;
    if(query.charAt(0) === '#') {
        tumblrPromise = tumblr.scoreWeekByTag(analysisRequestId, query.slice(1), dates);
    }
    const redditPromise = reddit.scoreWeek(analysisRequestId, query, dates);
    const hashtags = await twitter.scoreWeek(analysisRequestId, query, dates);
    await tumblrPromise;
    await redditPromise;
    activeJobs[analysisRequestId] = { res, hashtags, dates };
    sentimentEngine.completeJob(analysisRequestId);
    setTimeout(() => {
        const job = activeJobs[analysisRequestId];
        if(job !== undefined) {
            job.res.status(HTTP_STATUS.SERVER_ERROR).send({
                message: 'Sentiment analysis did not complete'
            });
        }
    }, requestExpirationMillis);
});

app.post('/api/results/:analysisRequestId', async (req, res) => {
    const { analysisRequestId } = req.params;
    const job = activeJobs[analysisRequestId];
    if(job === undefined) {
        return res.status(HTTP_STATUS.GONE).send({
            message: 'Request has expired'
        });
    }
    res.send();
    const { hashtags, dates } = job;
    const scores = req.body;
    job.res.send({ dates, hashtags, scores });
    delete activeJobs[analysisRequestId];
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
