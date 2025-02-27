# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
