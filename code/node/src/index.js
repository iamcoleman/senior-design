const express = require('express');

const config = require('../config');
const twitter = require('./platform/twitter');
const reddit = require('./platform/reddit');
const tumblr = require('./platform/tumblr');

const app = express();
const port = config.port;

app.use(express.static('public'))

app.get('/api/sentiment/query/:query', async (req, res) => {
    const { query } = req.params;
    const date = new Date();
    date.setDate(date.getDate() - 6);
    const dates = [date.toISOString().substring(0, 10)];
    for(let i = 0; i < 6; i++) {
        date.setDate(date.getDate() + 1);
        dates.push(date.toISOString().substring(0, 10));
    }

    let tumblrPromise = null;
    if(query.charAt(0) === '#') {
        tumblrPromise = tumblr.scoreWeekByTag(query.slice(1), dates);
    }
    const redditPromise = reddit.scoreWeek(query, dates);
    const twitterResult = await twitter.scoreWeek(query, dates);

    const response = {
        dates: dates,
        hashtags: twitterResult.hashtags,
        scores: {
            twitter: twitterResult.scores,
            reddit: await redditPromise,
        }
    };
    if(tumblrPromise !== null) {
        response.scores.tumblr = await tumblrPromise;
    }
    res.send(response);
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
