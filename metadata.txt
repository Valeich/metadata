import pypdf
import base64
import io

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

if __name__ == "__main__":
    try:
        with open("testing.txt", "r") as file:
            base64_pdf = file.read().strip()
        
        result = extract_metadata_from_base64(base64_pdf)
        
        if "error" in result:
            print(result["error"])
        else:
            print("Metadata extracted:")
            if isinstance(result["metadata"], dict):
                for key, value in result["metadata"].items():
                    print(f"{key}: {value}")
            else:
                print(result["metadata"])
    except FileNotFoundError:
        print("Error: testing.txt not found. Ensure the base64 file exists.")
