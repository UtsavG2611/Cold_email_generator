FROM python:3.11-slim

# Install build-essential for compiling dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make setup.sh executable
RUN chmod +x setup.sh

# Create directory for vector database
RUN mkdir -p /var/data/vectorstore

# Expose port
EXPOSE 8501

# Run setup script and start the application
CMD ["bash", "-c", "./setup.sh && streamlit run main.py"]
