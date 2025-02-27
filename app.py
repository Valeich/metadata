import pypdf
import base64
import io
from flask import Flask, request, jsonify

app = Flask(__name__)

def extract_metadata_from_base64(encoded_pdf: str):
    """Extracts metadata from a base64-encoded PDF."""
    try:
        pdf_bytes = base64.b64decode(encoded_pdf)
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = pypdf.PdfReader(pdf_stream)
        metadata = reader.metadata
        
        return {"metadata": metadata if metadata else "No metadata found"}
    except Exception as e:
        return {"error": f"Error reading PDF: {e}"}

@app.route('/extract-metadata', methods=['POST'])
def extract_metadata():
    """API endpoint to extract metadata from a base64-encoded PDF."""
    try:
        data = request.get_json()
        if not data or 'base64_pdf' not in data:
            return jsonify({"error": "Missing 'base64_pdf' in request"}), 400
        
        result = extract_metadata_from_base64(data['base64_pdf'])
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify service is running."""
    return jsonify({"status": "running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
