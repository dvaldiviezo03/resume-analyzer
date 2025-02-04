# use this for initlaization of flask
# use for logging - will help with debugging
# come back for routes LATER

from flask import Flask, request, jsonify
import logging

app=Flask(__name__)

logging.basicConfig(level=logging.INFO)

# logger instance
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    logger.info("Home route accessed.") # logs home route is being accessed3
    return "Resume Tool is running."

@app.route('/upload', methods=['POST'])
def upload_resume():
    logger.info("Attempting to upload resume.") # logs upload process start
    try:
        file = request.files['resume']
        if not file:
            logger.warning("No file recieved in the request.")
            return jsonify({"error": "No file uploaded."}), 400
        
        # process the file
        logger.info(f"File {file.filename} uploaded successfully.")
        return jsonify({"message": "Upload successfull."}), 200
    
    except Exception as e:
        logger.error(f"Error during fiel upload: {str(e)}", exc_info=True)
        return jsonify({"error", "Internal server error."}), 500