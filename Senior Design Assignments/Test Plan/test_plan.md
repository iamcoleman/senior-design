# Project Test Plan

This project requires a lot of integration testing due to all the services that must be tied together - Twitter API, Reddit API, Node.js server, Python Flask server, etc...

Integration testing with all the services is pretty straight forward. Basic calls will be made to the service being tested, then we will confirm if a response is received and if that response is correct. For example, a simple GET call can be made to the Twitter API. If a list of Tweets is received within a certain time limit, then we know that the Twitter API service is working as expected.

Another area of the project that will require lots of testing is the Sentiment Analysis Engine. Unlike the integration testing mentioned above, we will instead use unit tests to confirm functions, scripts, packages, etc. are working as intended.

Finally, some behavior driven tests will be used on the front-end. These tests will be designed from the end user's point of view - things like, "If I press the submit button, am I correctly redirected to the results page?" Or, "Is the sentiment graph displaying the correct values for my query?"
