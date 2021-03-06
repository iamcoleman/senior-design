# Sentiment Analysis Tool Routing Server

## Setup

Make a copy of `config.template.json` called `config.json` and fill in the API keys. Then run `npm install` to install dependencies and `npm start` to run the server.

To run with a production build of the front end, run `npm run build` in `code/site` and then copy the contents of `code/site/build` to `code/node/public`.

## Usage

### Sentiment

Start the sentiment analysis associated with a query over the past week and retrieve associated hashtags.

    POST /api/sentiment/query/:query

**Example response**:

    {
        "analysisRequestId": 175,
        "hashtags": ["Thanksgiving", "auspol", ..., "Iran"]
    }

### Results

Get the results of a sentiment analysis job. Scores range from 0 to 100. Dates are all GMT.

    GET /api/results/:analysisRequestId

**Example response**:

    {
        "dates": ["2020-01-18", "2020-01-19", ..., "2020-01-24"].
        "twitter": [
            {
                "score": 49.7,
                "count": 10,
                "lowerQuartile": 34.95,
                "upperQuartile": 64.45
            },
            ...
            {
                "score": 45.875,
                "count": 8,
                "lowerQuartile": 33.5625,
                "upperQuartile": 58.1875
            }
        ],
        "reddit": [
            {
                "score": 58.111111111111114,
                "count": 9,
                "lowerQuartile": 46.68055555555556,
                "upperQuartile": 67.25555555555556
            },
            ...
            {
                "score": 53.5,
                "count": 2,
                "lowerQuartile": 53.25,
                "upperQuartile": 53.75
            }
        ],
        "tumblr": [
            {
                "score": 45.125,
                "count": 8,
                "lowerQuartile": 42.25,
                "upperQuartile": 67.25
            },
            ...
            {
                "score": 51.5,
                "count": 4,
                "lowerQuartile": 50.25,
                "upperQuartile": 52.75
            }
        ]
    }
