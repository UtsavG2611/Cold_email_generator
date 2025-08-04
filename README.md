# Cold Email Generator

A Streamlit application that generates personalized cold emails based on job postings and your portfolio.

## Features

- Extract job details from a URL
- Match job skills with your portfolio
- Generate personalized cold emails
- Easy-to-use web interface

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```
4. Run the application:
   ```
   streamlit run main.py
   ```

## Deployment on Render

This application is configured for deployment on Render.com.

### Deployment Steps

1. Fork or clone this repository to your GitHub account
2. Sign up for an account on [Render](https://render.com/) if you don't have one
3. From the Render dashboard, click "New" and select "Web Service"
4. Connect your GitHub repository
5. Configure the web service:
   - Name: `cold-email-generator` (or your preferred name)
   - Environment: `Python`
   - Region: Choose the region closest to your users
   - Branch: `main` (or your default branch)
   - Build Command: `./setup.sh && pip install -r requirements.txt`
   - Start Command: `streamlit run main.py`
   - Plan: Free (or choose a paid plan for better performance)

6. Add the following environment variables in the Render dashboard:
   - `GROQ_API_KEY`: Your Groq API key (get one from [Groq](https://console.groq.com/))
   - `VECTORSTORE_PATH`: `/var/data/vectorstore`
   - `PORTFOLIO_PATH`: `/app/sample_portfolio.csv`
   - `PYTHONUNBUFFERED`: `true`
   - `RENDER`: `true`

7. Click "Create Web Service"

### Important Notes

- The first deployment may take several minutes as Render builds the Docker container
- The free tier of Render will spin down after periods of inactivity, causing the first request after inactivity to take longer
- For production use, consider upgrading to a paid plan
- Make sure your Groq API key is valid and has sufficient quota for your expected usage

## Project Structure

- `main.py`: Main Streamlit application
- `chains.py`: LLM interaction handling
- `portfolio.py`: Portfolio data management
- `utils.py`: Text cleaning utilities
- `sample_portfolio.csv`: Sample portfolio data
- `setup.sh`: Setup script for Streamlit configuration
- `render.yaml`: Render deployment configuration

## License

MIT