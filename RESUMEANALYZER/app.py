# for running
from flask import Flask, request, jsonify
import logging

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        file = request.files['resume']
        if not file:
            logger.warning("No file received in the request.")
            return jsonify({"error": "No file uploaded."}), 400
        
        # Process the file (you can add the processing functions here)
        logger.info(f"File {file.filename} uploaded successfully.")
        return jsonify({"message": "Upload successful."}), 200
    
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error."}), 500

if __name__ == '__main__':
    app.run(debug=True)
