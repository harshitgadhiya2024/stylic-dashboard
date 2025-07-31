FROM python:3.9-slim-buster

WORKDIR /app

RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    git nano vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy your application code
COPY . /app

# Install Flask and other dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8060

ENV NAME World

# Run the Flask server
CMD ["python", "main.py"]