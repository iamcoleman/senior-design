# Test Case Descriptions

## Test Plan Summary
Our approach to testing for this project will encompass all parts of the application: the front-end, the API and the node server. We will be utilizing a combination of black box and white box testing as well as a combination of abnormal and normal testing. First, we will focus on testing each component individually in the development environment. Once that is functional, we will move to testing the project as a whole in the production environment when all the components are connected. Below are the ten test cases that we plan to utilize to ensure our final product is both functional and stable.

### Test Case #0

**Purpose:** Template

**Description:** aaa

**Inputs:** aaa

**Expected Output:** aaa 

**Test Details:**
- [normal] [abnormal] [boundary] 
- [black box] [white box]
- [functional] [performance]
- [unit] [integration]

-----

### Test Case #1 - Twitter API Integration

**Purpose:** Confirm the Node.js server is able to retrieve Tweets through Twitter's API

**Description:** Test the connection between our Node.js server and Twitter's API. The test will query Twitter's API with a simple GET command that includes no parameters or filtering.

**Inputs:** N/A

**Expected Output:** A list of Tweets that were posted within the last 7 days 

**Test Details:**
- Normal
- White Box
- Functional
- Integration

-----

### Test Case #2 - Reddit API Integration

**Purpose:** Confirm the Node.js server is able to retrieve Reddit posts and comments through Reddit's API

**Description:** Test the connection between our Node.js server and Reddit's API. The test will query Reddit's API with a simple GET command that includes no parameters or filtering.

**Inputs:** N/A

**Expected Output:** A Reddit post with a collection of the post's comments 

**Test Details:**
- Normal
- White Box
- Functional
- Integration

-----

### Test Case #3 - Twitter API Filtering

**Purpose:** Confirm that the Node.js server is receiving correctly filtered Tweets from Twitter's API

**Description:** The Node.js server needs to be able to query the Twitter API with a certain number of user specified filters (e.g., filtering out Tweets that don't contain the word "Microsoft"). This test is to confirm that all Tweets returned by the Twitter API have been correctly filtered.

**Inputs:** A single word or list of words that the Tweet must contain (e.g., "Microsoft" and "Azure"). We will have one test for a single word search and another test for a multi-word search.

**Expected Output:** A list of Tweets that contain all of the input words (e.g., Tweets that contain the words "Microsoft" and "Azure")

**Test Details:**
- Normal
- White Box
- Functional
- Integration

-----

### Test Case #4 - Reddit API Filtering

**Purpose:** Confirm that the Node.js server is receiving correctly filtered posts and comments from Reddit's API

**Description:** The Node.js server needs to be able to query the Reddit API with a certain number of user specified filters (e.g., filtering out comments that don't contain the word "Amazon"). This test is to confirm that all posts and comments returned by the Reddit API have been correctly filtered.

**Inputs:** A single word or list of words that the Tweet must contain (e.g., "Amazon" and "AWS"). We will have one test for a single word search and another test for a multi-word search.

**Expected Output:** A list of posts and comments that contain all of the input words (e.g., posts/comments that contain the words "Amazon" and "AWS")

**Test Details:**
- Normal
- White Box
- Functional
- Integration

-----

### Test Case #5 - Twitter API Performance Test

**Purpose:** Test the time it takes the Twitter API to gather and return a list of filtered Tweets

**Description:** Query the Twitter API for filtered Tweets and record the amount of time that elapses between when the query is sent from the Node.js server and when the Tweets are received. 

**Inputs:** A list of words to filter for

**Expected Output:** A list of Tweets

**Test Details:**
- Normal
- White Box
- Performance
- Integration

-----

### Test Case #6 - Reddit API Performance Test

**Purpose:** Test the time it takes the Reddit API to gather and return a list of filtered posts and comments

**Description:** Query the Reddit API for filtered posts/comments and record the amount of time that elapses between when the query is sent from the Node.js server and when the posts/comments are received. 

**Inputs:** A list of words to filter for

**Expected Output:** A list of posts/comments

**Test Details:**
- Normal
- White Box
- Performance
- Integration

-----

### Test Case #7 - Front-end Search Results

**Purpose:** To determine if a user submitted query from the front-end will lead to the correct sentiment analysis results being displayed on the front-end

**Description:** When a search is submitted on the front-end, we want the user to be redirected to a "waiting page" while the sentiment analysis is performed. Once the results are ready, we want this "waiting page" to load and display the results correctly.

**Inputs:** A user submitted query through the front-end

**Expected Output:** A results page on the front-end that matches the user submitted query

**Test Details:**
- Normal
- Black Box
- Functional
- Integration

-----

### Test Case #8 - Sentiment Analysis Engine, Correct Results

**Purpose:** Confirm that the Sentiment Analysis Engine is producing the correct results for a piece of text

**Description:** A predefined snippet of text will be processed through the Sentiment Analysis Engine. Then the results will be compared against the already known correct results.

**Inputs:** A snippet of text

**Expected Output:** The sentiment analysis results for the input text

**Test Details:**
- Normal
- White Box
- Functional
- Unit

-----

### Test Case #9 - Sentiment Analysis Engine Performance

**Purpose:** Test the speed of the Sentiment Analysis Engine

**Description:** A large piece of text (i.e., something much larger than the Tweets or Reddit posts that will normally be used) will be sent into the Sentiment Analysis Engine. The time will be recorded from when the text is submitted to when the results are returned. 

**Inputs:** A large piece of predefined text

**Expected Output:** The time that elapsed during the sentiment analysis

**Test Details:**
- Normal
- White Box
- Performance
- Unit

-----

### Test Case #10 - Sentiment Score Graph Functionality

**Purpose:** Test the correctness of the "Sentiment Score" graph that is displayed on the results page

**Description:** There will be a graph that assigns a "sentiment score" to a user submitted query on the results page. This test is to confirm that the generated graph matches the data provided to it. 

**Inputs:** A "sentiment score" dataset

**Expected Output:** A graph on the results page of the front-end

**Test Details:**
- Normal
- Black Box
- Functional
- Unit

-----

## Test Case Matrix
