# for running
from flask import Flask, request, jsonify
from preprocessing import extract_pdf_text, extract_contact_info
from database import create_db
import logging
import fitz
import sqlite3
import re

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
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
    return "Resume Tool is running."

# Upload route
@app.route('/upload', methods=['POST'])
def upload_resume():
    logger.info("Attempting to upload resume.")
    try:
        file = request.files.get('resume')
        if not file:
            logger.warning("No file received in the request.")
            return jsonify({"error": "No file uploaded."}), 400
        
        # temporaily save file
        file_path = f"./uploads/{file.filename}"
        file.save(file_path)

        # extract resume text
        resume_text = extract_pdf_text(file_path)
        logger.info(f"Extracted Resume Text:\n{resume_text}")
        if not resume_text:
            return jsonify ({"error": "Could not extract text from resume."}), 500

        # extract contact info
        contact_info = extract_contact_info(resume_text)

        #save to db
        save_to_db(contact_info["Email"], contact_info["Phone"], contact_info["LinkedIn"], resume_text)

        return jsonify ({"message": "Resume processed successfully.", "data": contact_info}), 200
    
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error."}), 500

# initialize db
create_db()

if __name__ == '__main__':
    app.run(debug=True)
