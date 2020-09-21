Coleman - here are some quick notes for some design choices...

### Client / Front-End
- I've used Angular and Vue.js a lot in the past (would definitely pick Vue over Angular for a project like this though), but heard Tim mention using React. I'm good with whatever, I've never used React but would be willing to learn.

### Server / API
- I have a lot of experience with NodeJS backends. I also heard Jeet mention a Python Flask backend.
- I know some pros for NodeJS that I think are relevant to this project are: better real-time performance, better scalability, asynchronous requests
- Could also see Python having some pros: more of the "data science" language, better performance when doing large computations
- Could do something like a 2 server system 
  - one in NodeJS that is responsible for client-to-server connection, grabbing data from the database then formatting that data for the front-end, calling the API's / doing the web-crawling of whatever sources we're grabbing text from
  - one in Python for doing the actual sentiment analysis, generating reports/metrics, saving the data to the database
  - the pros I see with this setup: NodeJS will be able to asynchronously grab all the text data, think it's a good separation between the data collection/presentation (node) and the data science (python)
  - the cons: obviously more development / more moving parts to keep track of, 
  
### Database
- I think we need to talk more about what we're actually going to save before making any choices here
- we could potentially save nothing and just send all the report data to the user's browser
  - would lose out on historical data though (is that okay for MVP?)
