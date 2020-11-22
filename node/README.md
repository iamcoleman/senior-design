# Sentiment Analysis Tool Routing Server

## Setup

Make a copy of `config.template.json` called `config.json` and fill in the API keys. Then run `npm install` to install dependencies and `npm start` to run the server.

## Usage

Right now, making a get request to `/:query` will return hashtags associated with the text you entered. For instance, this request:

    GET http://localhost:3000/politics

will retrieve a response like this:

    {
        "tags": [
            "Thanksgiving",
            "auspol",
            "TrumpIsACriminal",
            "News",
            "NYT",
            "FoxNews",
            "Iran"
        ]
    }
