import pypdf
import base64
import io
import os
import logging
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def extract_metadata_from_base64(encoded_pdf: str):
    """Extracts metadata from a base64-encoded PDF."""
    try:
        # Try to decode the base64 string
        try:
            pdf_bytes = base64.b64decode(encoded_pdf)
        except Exception as e:
            logger.error(f"Base64 decoding error: {e}")
            return {"error": f"Invalid base64 encoding: {e}"}
        
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = pypdf.PdfReader(pdf_stream)
        metadata = reader.metadata
        
        # Convert metadata to a serializable dictionary if it exists
        if metadata:
            metadata_dict = {k: str(v) for k, v in metadata.items()} if metadata else {}
            return {"metadata": metadata_dict}
        else:
            return {"metadata": "No metadata found"}
            
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        return {"error": f"Error reading PDF: {e}"}

@app.route('/extract-metadata', methods=['POST'])
def extract_metadata():
    """API endpoint to extract metadata from a base64-encoded PDF."""
    try:
        data = request.get_json()
        if not data or 'base64_pdf' not in data:
            logger.warning("Missing 'base64_pdf' in request")
            return jsonify({"error": "Missing 'base64_pdf' in request"}), 400
        
        logger.info("Processing PDF metadata extraction request")
        result = extract_metadata_from_base64(data['base64_pdf'])
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Unexpected error in request handling: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify service is running."""
    logger.debug("Health check request received")
    return jsonify({"status": "running"}), 200

if __name__ == '__main__':
    # Get port from environment variable or default to 8080
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port)
