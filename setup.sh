#!/bin/bash

# Create streamlit config directory
mkdir -p ~/.streamlit/

# Create credentials file
cat > ~/.streamlit/credentials.toml << EOL
[general]
email = "your@email.com"
EOL

# Create config file with proper port configuration for Render
cat > ~/.streamlit/config.toml << EOL
[server]
headless = true
enableCORS = false
port = ${PORT:-8501}
EOL

# Create directory for vector database if it doesn't exist
mkdir -p ${VECTORSTORE_PATH:-vectorstore2}

# Print setup completion message
echo "Setup completed successfully!"