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

async function scoreDate(query, date, dayAfter) {
    const options = {
        count: 10
    };
    if(dayAfter !== undefined) {
        options.until = dayAfter;
    }
    const twitterPosts = await twitter.search(query, options);
    const scorePromises = [];
    for(let status of twitterPosts.statuses) {
        const tweetDate = new Date(status.created_at).toISOString().substring(0, 10);
        if(tweetDate !== date) {
            break;
        }
        scorePromises.push(analyzeSentiment(status.text));
    }
    if(scorePromises.length === 0) {
        return 'no data';
    }
    const scores = await Promise.all(scorePromises);
    return Math.round(scores.reduce((a, b) => a + b) / scores.length);
}

app.get('/sentiment/:query', async (req, res) => {
    const date = new Date();
    let dateString = date.toISOString().substring(0, 10);
    const dates = [dateString];
    const sentimentByDate = {}
    sentimentByDate[dateString] = [];
    for(let i = 0; i < 6; i++) {
        date.setDate(date.getDate() - 1);
        dateString = date.toISOString().substring(0, 10);
        dates.push(dateString);
        sentimentByDate[dateString] = [];
    }

    const scorePromises = [scoreDate(req.params.query, dates[0])];
    for(let i = 1; i < 7; i++) {
        scorePromises.push(scoreDate(req.params.query, dates[i], dates[i - 1]));
    }

    const response = [];
    for(let i = 0; i < 7; i++) {
        response.push({
            date: dates[i],
            score: await scorePromises[i]
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
