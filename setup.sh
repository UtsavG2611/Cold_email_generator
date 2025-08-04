#!/bin/bash

# Create streamlit config directory
mkdir -p ~/.streamlit/

# Create credentials file
echo "\
[general]\n\
email = \"your@email.com\"\n\
" > ~/.streamlit/credentials.toml

# Create config file with proper port configuration for Render
echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = ${PORT:-8501}\n\
" > ~/.streamlit/config.toml

# Create directory for vector database if it doesn't exist
mkdir -p ${VECTORSTORE_PATH:-vectorstore2}

# Print setup completion message
echo "Setup completed successfully!"