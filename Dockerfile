FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.9 \
    python3-pip \
    git \
    nano \
    vim && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy your application code
COPY . /app

# Install Flask and other dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod u+x realesrgan-ncnn-vulkan

EXPOSE 8060

# Run the Flask server
CMD ["python3", "main.py"]