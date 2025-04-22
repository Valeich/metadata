import pypdf
import base64
import io
import os
import logging
from flask import Flask, request, jsonify
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def extract_metadata_and_text_from_base64(encoded_pdf: str):
    """Extracts specific metadata fields from a base64-encoded PDF."""
    try:
        pdf_bytes = base64.b64decode(encoded_pdf)
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = pypdf.PdfReader(pdf_stream)
        raw_metadata = reader.metadata or {}

        metadata = {
            "author": raw_metadata.get("/Author"),
            "created_date": raw_metadata.get("/CreationDate"),
            "modified_date": raw_metadata.get("/ModDate"),
            "producer": raw_metadata.get("/Producer"),
            "creator": raw_metadata.get("/Creator")
        }

        return {"metadata": metadata}
    except Exception as e:
        logger.exception("Failed to extract metadata")
        return {"error": f"Error reading PDF: {e}"}

@app.route('/extract-metadata', methods=['POST'])
def extract():
    try:
        data = request.get_json()
        if not data or 'base64_pdf' not in data:
            logger.warning("Missing 'base64_pdf' in request")
            return jsonify({"error": "Missing 'base64_pdf' in request"}), 400
        
        logger.info("Processing PDF extraction request")
        extraction_result = extract_metadata_and_text_from_base64(data['base64_pdf'])
        
        return jsonify(extraction_result)
    except Exception as e:
        logger.error(f"Unexpected error in request handling: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    logger.debug("Health check request received")
    return jsonify({"status": "running"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port)
