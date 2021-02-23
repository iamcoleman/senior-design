# All the code for the Sentiment Analysis Tool

## Four sub-folders
1. **engine_api**
    - holds the code for the Python Flask API that allows the Node.js server and the Python Sentiment Analysis Engine to communicate.
2. **node**
    - holds the code for the Node.js server
3. **sentiment-analysis**
    - holds the code for the Python Sentiment Analysis Engine
4. **site**
    - holds the code for the React site
   
---
    
## Code Setup

### Python Virtual Environment

Make sure you have initialized the virtual environment `venv` for the application under `senior-design/code/`. This virtual environment is used for **both the `engine_api` and the `sentiment-analysis` code**.
1. Go to the `senior-design/code/` folder in terminal/cmd
2. Create a virtual environment named `venv`
    - on macOS and Linux use: `python3 -m venv venv`
    - on Windows use: `py -m venv venv`
3. Activate the virtual environment
    - on macOS and Linux use: `source venv/bin/activate`
    - on Windows CMD use: `.\venv\Scripts\activate.bat`
    - on Windows PowerShell use: `.\venv\Scripts\Activate.ps1`
4. Install packages from the `requirements.txt` file in `senior-design/code/`
    - use: `pip install -r requirements.txt`
