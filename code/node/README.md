# Sentiment Analysis Tool Routing Server

## Setup

Make a copy of `config.template.json` called `config.json` and fill in the API keys. Then run `npm install` to install dependencies and `npm start` to run the server.

## Usage

### Tags

Gather hashtags and subreddits associated with a query.

    GET /tags/:query

**Example response**:

    {
        "tags": [
            "Thanksgiving",
            "auspol",
            "TrumpIsACriminal",
            "News",
            "NYT",
            "FoxNews",
            "Iran"
        ],
        "subreddits": [
            "gifs",
            "worldnews",
            "politics",
            "Documentaries",
            "MurderedByWords",
            "TrueOffMyChest",
            "facepalm",
            "LifeProTips",
            "PoliticalCompassMemes"
        ]
    }

### Sentiment

Find the sentiment associated with a query over time. Scores range from 0 to 100. Dates are all GMT.

    GET /sentiment/query/:query

**Example response**:

    [
        {
            "date": '2020-01-24',
            "score": 68
        },
        {
            "date": '2020-01-23',
            "score": 65
        },
        ...,
        {
            "date": '2020-01-18',
            "score": 62
        }
    ]
