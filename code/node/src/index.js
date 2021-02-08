const express = require('express');

const config = require('../config');
const twitter = require('./twitter');
const reddit = require('./reddit');

const app = express();
const port = config.port;

app.use(express.static('public'))

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

async function scoreDateTwitter(query, date, dayAfter) {
    const options = {
        count: 10
    };
    if(dayAfter !== undefined) {
        options.until = dayAfter;
    }
    const twitterPosts = await twitter.search(query, options);
    const scorePromises = [];
    const hashtags = new Set();
    for(let status of twitterPosts.statuses) {
        const tweetDate = new Date(status.created_at).toISOString().substring(0, 10);
        if(tweetDate !== date) {
            break;
        }
        scorePromises.push(analyzeSentiment(status.text));
        for(tag of status.entities.hashtags) {
            hashtags.add(tag);
        }
    }
    if(scorePromises.length === 0) {
        return 'no data';
    }
    const scores = await Promise.all(scorePromises);
    return {
        score: Math.round(scores.reduce((a, b) => a + b) / scores.length),
        hashtags: hashtags
    };
}

async function scoreWeekTwitter(query, dates) {
    const scorePromises = [];
    for(let i = 0; i < 7; i++) {
        scorePromises.push(scoreDateTwitter(query, dates[i], dates[i + 1]));
    }
    const scores = [];
    const hashtags = new Set();
    for(let i = 0; i < 7; i++) {
        const result = await scorePromises[i];
        scores.push({
            date: dates[i],
            score: result.score
        });
        for(const tag of result.hashtags) {
            hashtags.add(tag.text);
        }
    }
    return { scores, hashtags };
}

async function scoreWeekReddit(query, dates) {
    const searchPromise = reddit.search(query, {
        limit: 70,
        t: 'week'
    });
    const scoresByDate = {};
    for(const date of dates) {
        scoresByDate[date] = [];
    }
    const redditPosts = await searchPromise;
    for(const post of redditPosts.data.children) {
        const date = new Date(post.data.created * 1000).toISOString().substring(0, 10);
        if(scoresByDate[date] !== undefined) {
            scoresByDate[date].push(analyzeSentiment(post.data.selftext));
        }
    }
    const scores = [];
    for(const date of dates) {
        const scorePromises = scoresByDate[date];
        if(scorePromises.length === 0) {
            scores.push({
                date: date,
                score: 'no data'
            });
        } else {
            const dateScores = await Promise.all(scorePromises);
            scores.push({
                date: date,
                score: Math.round(dateScores.reduce((a, b) => a + b) / dateScores.length)
            });
        }
    }
    return scores;
}

app.get('/api/sentiment/query/:query', async (req, res) => {
    const { query } = req.params;
    const date = new Date();
    date.setDate(date.getDate() - 6);
    const dates = [date.toISOString().substring(0, 10)];
    for(let i = 0; i < 6; i++) {
        date.setDate(date.getDate() + 1);
        dates.push(date.toISOString().substring(0, 10));
    }

    const redditPromise = scoreWeekReddit(query, dates);
    const twitterResult = await scoreWeekTwitter(query, dates);

    const response = {
        twitter: twitterResult.scores,
        reddit: await redditPromise,
        hashtags: [...twitterResult.hashtags]
    };
    res.send(response);
});

app.get('/api/tags/:query', async (req, res) => {
    const twitterPromise = twitter.search(req.params.query).then(extractTwitterTags);
    const redditPromise = reddit.search(req.params.query).then(extractSubreddits);
    const [tags, subreddits] = await Promise.all([twitterPromise, redditPromise]);
    res.send({ tags, subreddits });
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
