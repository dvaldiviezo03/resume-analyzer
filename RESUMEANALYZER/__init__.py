# use this for initlaization of flask
# use for logging - will help with debugging
# come back for routes LATER

from flask import Flask, request, jsonify
import logging

app=Flask(__name__)

logging.basicConfig(level=logging.INFO)

# logger instance
logger = logging.getlogger(__name__)

@app.route('/')
def home():
    logger.info("Home route accessed.") # logs home route is being accessed3
    return "Resume Tool is running."

@app.route('/upload', methods=['POST'])
def upload_resume():
    logger.info("Attempting to upload resume.") # logs upload process start