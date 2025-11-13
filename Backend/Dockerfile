# Use a slim Python image
FROM python:3.11-slim

# Set environment variable to include the app root in PYTHONPATH for imports
ENV PYTHONPATH=/usr/src/app

# Set the working directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /usr/src/app/public/logos

COPY public/logos/ /usr/src/app/public/logos/

# Copy application source code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the application
CMD [ "python", "api/app.py" ]