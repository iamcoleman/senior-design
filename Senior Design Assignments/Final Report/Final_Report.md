# Sentiment Analysis Tool Final Report

Table of contents:

<!-- no toc -->
1. [Project Description](#project-description)
2. [User Interface Specification](#user-interface-specification)
3. [Test Plan and Results](#test-plan-and-results)
4. [User Manual](#user-manual)
5. [Spring Final PPT Presentation](#spring-final-ppt-presentation)
6. [Final Expo Poster](#final-expo-poster)
7. [Assessments](#assessments)
   1. [Tim Initial Assessment](#tim-initial-assessment)
   2. [Jeet Initial Assessment](#jeet-initial-assessment)
   3. [Coleman Initial Assessment](#coleman-initial-assessment)
   4. [Tim Final Assessment](#tim-final-assessment)
   5. [Jeet Final Assessment](#jeet-final-assessment)
   6. [Coleman Final  Assessment](#coleman-final--assessment)
8. [Summary of Hours and Justification](#summary-of-hours-and-justification)
   1. [Tim](#tim)
   2. [Jeet](#jeet)
   3. [Coleman](#coleman)


## Project Description

This project analyzes the sentiment of social media data to display trends in public opinion. Users search for a set of keywords, then data from the past week is analyzed from Twitter, Reddit, and Tumblr and displayed on a graph.

## User Interface Specification

![A screenshot of our UI](screenshot.svg)

There is a search bar at the top, and users can search for a topic or a hashtag. Below that, they can see related hashtags, and then they can select which social media platforms to view sentiment data for. At the bottom there is a graph, showing public sentiment regarding their search over time.

## Test Plan and Results

## User Manual

[Check out our Wiki](https://github.com/iamcoleman/senior-design/wiki)

## Spring Final PPT Presentation

Click to view the slideshow:
[![First slide of presentation](slide.svg)](https://docs.google.com/presentation/d/e/2PACX-1vSB2f5EmLQstvDX6cM-xhBO_IanveuJXXeG774muA54aI8dtPCy0KtDyA8qk8toqs74GH8hlmvUt5CB/pub?start=false&loop=false&delayms=60000)

Click to view the video presentation:
[![First slide of video](video-slide.svg)](https://drive.google.com/file/d/1Su3Yq4Rba4fsAbJfgN-FgTi4CQBxjAUy/view?usp=sharing)

## Final Expo Poster

![Our poster](Poster.svg)

## Assessments

### Tim Initial Assessment

My group's senior design project is a sentiment analysis platform. It will use social media data to assess public opinion of a topic or brand. It will allow users to view sentiment over time and assess how public perception has changed. This project combines natural language processing and artificial intelligence with API design and web development. It will require well-designed algorithms, smart caching, and scalable design to work efficiently. The result will be accessible as a website and potentially as a public API.

This project will use Python, which we learned in CS 2021 - Python Programming. It will also require concepts from CS 4071 - Design and Analysis of Algorithms, as we will need to efficiently sort and manipulate data. CS 5168, which I am currently taking, will likely be useful. Neural networks are highly parallel, and natural language processing often uses neural networks. I am also taking CS 5154 - Information Retrieval, which will provide insight on how to search social media and parse basic information from the text. This course will also help me to mathematically assess how accurate our results are.

While working at Siemens PLM Software I learned about the basics of back-end development and about frameworks for front-end development. This will be useful for developing the web interface for the application. I also worked with Jeet at this job, so we have already established rapport. At Worldpay/FIS, I have learned much more about API design and building maintainable code. This will keep the project manageable and prevent us from creating unworkable code. I have also learned how to review code well and how to manage collaboration, especially between front-end and back-end developers.

I am excited to work on this project because it broadens my horizons while capitalizing on my skills. I am not very familiar with natural language processing or with Python. That said, I have a lot of experience with web development and API design. I am also excited to collaborate with Jeet and Coleman. They have different backgrounds than I do - both focusing more on data science than web development. I think this difference will help us be more productive and learn from each other, as well as establish roles for each of us in the project so we're not all working on the same parts of the code at the same time.

We will likely start by building engines to read text and determine whether it matches keywords and what sentiment is behind it. We will then scale this out by integrating social media APIs to gather data and building an API to share the data. Then we will build a site that uses the API and aggregates the data. We are planning to use Python for the back end and React for the front end. The MVP will be a site where you can enter keywords and get a graph of public perception over time. Once this is done, we will continue to add features while time allows. I will self-evaluate based on how well the web interface is done, as this is the part of the project that I will likely be the most involved in. I will also evaluate how well I was able to adapt and learn the data science aspects of the project.

### Jeet Initial Assessment

### Coleman Initial Assessment

### Tim Final Assessment

Most of my work was related to the Node server and React front end. I created the Node server and integrated it with all of the APIs. This includes the search endpoints for Twitter and Reddit, as well as the hashtag search endpoint for Tumblr. I had the server extract the hashtags and parse the text data from the results to send to the Python API. All of these requests were asynchronous, and I took care to ensure that nothing that didn’t need to block other processes was blocking. I then added an endpoint to the server to retrieve the results from the Python API, if available, and transform them for usage by the front end. I also set up the React site, which included a graphical display of the data from the Node server. On the site, you can view related hashtags and see the weekly trends for sentiment, along with the range of the 60th and 40th percentiles.
I did not get as much of an opportunity as I had hoped to work on the sentiment analysis portion of the project. However, I worked on my web development experience, and this will help me in the future as a full-stack developer. By challenging myself to ensure that all of the requests and processing were asynchronous, I developed my ability to think in terms of concurrency and avoid race conditions.

### Jeet Final Assessment

### Coleman Final  Assessment

## Summary of Hours and Justification

### Tim

| Task | Hours |
| - | - |
| Setting up Node server | 5 |
| Integrating with Twitter API | 7 |
| Integrating with Reddit API | 7 |
| Integrating with Tumblr API | 7 |
| Integrating with Python engine API | 12 |
| Extracting hashtags | 3 |
| Setting up front end | 4 |
| Styling front end | 4 |
| Integrating with Node server | 7 |
| Creating graph | 9 |
| Adding percentile display | 8 |
| Adding platform selection dropdown | 5 |
| Adding related hashtags | 3 |

### Jeet

### Coleman
