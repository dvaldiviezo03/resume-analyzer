# for running
from flask import Flask, render_template, request, jsonify
from preprocessing import extract_pdf_text, extract_contact_info
from database import create_db
from ai_module import compare_texts, gen_feedback
import logging
import fitz
import sqlite3
import re
import os

# this initializes flask peruse
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Save the db
def save_to_db(email, phone, linkedin, resume_text):
    try:
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        c.execute('''INSERT INTO resumes (email, phone, linkedin, resume_text) 
                     VALUES (?, ?, ?, ?)''', (email, phone, linkedin, resume_text))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error saving to DB: {e}", exc_info=True)

# Home route
@app.route('/')
def home():
    logger.info("Home route accessed.")
    return render_template('frontpage.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload_resume():
    logger.info("Attempting to upload resume.")
    try:

        file = request.files.get('resume')
        if not file:
            logger.warning("No file received in the request.")
            return jsonify({"error": "No file uploaded."}), 400
        # form from the html file
        job_description = request.form.get('job_description', '').strip()
        if not job_description:
            logger.warning("No job description given.")
            return jsonify({"error": "No job description given."}), 400

        os.makedirs('./upload', exist_ok=True) #creates directory when it doesnt exist yet
                                        
        # temporaily save file
        file_path = f"./upload/{file.filename}"
        file.save(file_path)

        # extract resume text
        resume_text = extract_pdf_text(file_path)
        logger.info(f"Extracted Resume Text:\n{resume_text}")
        if not resume_text:
            return jsonify ({"error": "Could not extract text from resume."}), 500

        # extract contact info
        contact_info = extract_contact_info(resume_text)

        match_result = compare_texts(resume_text, job_description)
        detailed_feedback = gen_feedback(resume_text, job_description)
        
        #save to db
        save_to_db(contact_info["Email"], contact_info["Phone"], contact_info["LinkedIn"], resume_text)

        return render_template('results.html', 
                               score=match_result["similarity_score"], 
                               match=match_result["match"], 
                               feedback=detailed_feedback)
    
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error."}), 500

# initialize db
try:
    create_db()
except Exception as e:
    logger.error(f"DB initialization failed: {e}", exc_info=True)
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
