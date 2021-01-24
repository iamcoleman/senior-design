const express = require('express');

const config = require('../config');
const twitter = require('./twitter');
const reddit = require('./reddit');

const app = express();
const port = config.port;

function arrayWithoutDuplicates(inputArray) {
    return Array.from(new Set(inputArray));
}

function extractTwitterTags(twitterPosts) {
    return arrayWithoutDuplicates(twitterPosts.statuses
        .map(status => status.entities.hashtags)
        .reduce((a, b) => a.concat(b), [])
        .map(hashtag => hashtag.text));
}

function extractSubreddits(redditPosts) {
    return arrayWithoutDuplicates(redditPosts.data.children
        .map(post => post.data.subreddit));
}

// This is async because it will be an API call
async function analyzeSentiment(query) {
    return Math.floor(Math.random() * 101);
}

app.get('/sentiment/:query', async (req, res) => {
    const twitterPosts = await twitter.search(req.params.query);
    const date = new Date();
    let dateString = date.toISOString.substring(0, 10);
    const dates = [dateString];
    const sentimentByDate = {}
    sentimentByDate[dateString] = [];
    for(let i = 0; i < 6; i++) {
        date.setDate(date.getDate() - 1);
        dateString = date.toISOString.substring(0, 10);
        dates.push(dateString);
        sentimentByDate[dateString] = [];
    }
    for(let status of twitterPosts.statuses) {
        const tweetDate = new Date(status.created_at).toISOString().substring(0, 10);
        sentimentByDate[tweetDate].push(analyzeSentiment(status.text));
    }
    const scores = await Promise.all(dates.map(async (date) => {
        const values = await Promise.all(sentimentByDate[date]);
        if(values.length === 0) {
            // TODO: ensure this doesn't happen
            return 'no data';
        } else {
            return Math.round(values.reduce((a, b) => a + b) / 100);
        }
    }));
    const response = [];
    for(let i = 0; i < 7; i++) {
        response.push({
            date: dates[i],
            score: scores[i]
        });
    }
    res.send(response);
});

app.get('/tags/:query', async (req, res) => {
    const twitterPromise = twitter.search(req.params.query).then(extractTwitterTags);
    const redditPromise = reddit.search(req.params.query).then(extractSubreddits);
    const [tags, subreddits] = await Promise.all([twitterPromise, redditPromise]);
    res.send({ tags, subreddits });
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
