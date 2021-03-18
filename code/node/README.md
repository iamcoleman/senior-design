# Sentiment Analysis Tool Routing Server

## Setup

Make a copy of `config.template.json` called `config.json` and fill in the API keys. Then run `npm install` to install dependencies and `npm start` to run the server.

To run with a production build of the front end, run `npm run build` in `code/site` and then copy the contents of `code/site/build` to `code/node/public`.

## Usage

### Sentiment

**Origin**: Front end

Find the sentiment associated with a query over the past week. Scores range from 0 to 100. Dates are all GMT.

    GET /api/sentiment/query/:query

**Example response**:

    {
        "dates": ["2020-01-18", "2020-01-19", ..., "2020-01-24"],
        "hashtags": ["Thanksgiving", "auspol", ..., "Iran"],
        "scores": {
            "twitter": [68, 65, 58, 59, 67, 61, 62],
            "reddit": [54, 49, 55, 60, 58, 64, 68]
        }
    }

**Example error response**:

    {
        "message": "Sentiment analysis did not complete"
    }

### Results

**Origin**: Sentiment analysis engine API

Send the results of a sentiment analysis. Throws a `404 GONE` error if the job ID is invalid, which will occur if the request
has expired or was never created.

    POST /api/results/:analysisRequestId

**Example request body**: TBD

**Example error response**:

    {
        "message": "Request not found"
    }
