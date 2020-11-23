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

app.get('/:query', async (req, res) => {
    const twitterPromise = twitter.search(req.params.query).then(extractTwitterTags);
    const redditPromise = reddit.search(req.params.query).then(extractSubreddits);
    const [tags, subreddits] = await Promise.all([twitterPromise, redditPromise]);
    res.send({ tags, subreddits });
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
