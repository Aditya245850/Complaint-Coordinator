Welcome to Complaint Coorinator!

Complaint Coordinator is a multi-modal complaint organization system developed using Python and Flask. 
This application leverages Google Cloud APIs to analyze and categorize various formats of complaints—voice, image, and video—while using OpenAI for 
processing and categorizing text-based complaints. The system provides a comprehensive interface for users to upload complaints in different formats 
and receive detailed categorizations and sentiment analysis. It also supports generating downloadable reports that include Plotly graphs for prioritizing 
complaints, streamlining the workflow for customer service teams.


How to run:

1) Begin by cloning the repository using the command and entering into the directory

  git clone https://github.com/Aditya245850/complaint-coordinator.git
  cd complaint-coordinator

2) Create a python virtual environment
   python3 -m venv venv
   source venv/bin/activate

3) Install the necessary dependencies
   pip install -t requirements.txt

4) Set up the Database Configuration in DB_CONNECTION.py
   DB_HOST = ''
  DB_NAME = ''
  DB_USER = ''
  DB_PASS = ''
  DB_PORT = ''

5) Set the API KEYS in application.py
   API_KEY = 'your_api_key'

6) Retrieve a JSON key file from your Google Cloud console for the necessary APIs (Speech-to-Text, Vision
   and Video Intelligence)
   
   os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path-to-your-json-file.json"

7) Run the Flask application in application.py

   flask run

8) Visit http://127.0.0.1:5000 to view the application
   
