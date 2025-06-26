# resume-analyzer
A Flask web application that analyzes resumes against job descriptions using OpenAI's API and gives ai feedback.

# features
- Upload PDF resume
- Exctracts contact info(email, phone, Linkedln)
- Matches resume to job description using NLP
- Generates personalized bullet-point feedback using AI
- Stores daat in SQLite
- Clean, responsive UI with Flask and HTML/CSS

# tech stack
- Python
- Flask
- SQLite3
- OpenAI API
- PyMuPDF (from 'fitz')
- HTML/CSS

# what I learned
- Implmenting openAI API
- Integrating NLP sentence transformers model for sentecne comparison
- Database creation using python's SQL library
- Frontend div uses and css styling

# what could be imporved
- Runtime issues, the program is slow to start up and slow to analyze. It could be reworked in the future for better time complexity.
- Newer more visually appealing UX design. Is an easy fix but works nonetheless.
- File type upload. Right now only PDF files are accepted to eb analyzed, but a future update could allow for all types of files to be parced. 

# installation
git clone https://github.com/username/resume-analyzer.git
cd resume-analyzer/RESUMEANALYZER
python -m venv venv
sorce venv/bin/activate
pip install -r requirements.txt

# create .env file in root directory and add your OpenAI key like so
OPENAI_API_KEY = your_api_key

# then run
python app.py
