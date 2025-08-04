import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import logging

# Import custom modules
from chains import Chain  # Handles LLM interactions
from portfolio import Portfolio  # Manages portfolio data and queries
from utils import clean_text  # Text preprocessing utility

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cold Email Generator")
    st.write("Enter a job posting URL to generate a cold email")
    url_input = st.text_input("Enter a URL: ")
    submit_button = st.button("Submit")

    if submit_button:
        if not url_input:
            st.warning("Please enter a valid URL")
            return
            
        try:
            with st.spinner("Loading job posting data..."):
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                logging.info(f"Successfully loaded and cleaned data from {url_input}")
            
            with st.spinner("Loading portfolio data..."):
                portfolio.load_portfolio()
                logging.info("Successfully loaded portfolio data")
            
            with st.spinner("Extracting job details..."):
                jobs = llm.extract_jobs(data)
                logging.info(f"Successfully extracted {len(jobs)} job(s)")
            
            st.subheader("Generated Cold Emails:")
            for i, job in enumerate(jobs):
                with st.spinner(f"Generating email {i+1}..."):
                    skills = job.get("skills", [])
                    portfolio_urls = portfolio.query_links(skills)
                    email = llm.write_email(job, portfolio_urls)
                    st.markdown(f"**Email {i+1}:**")
                    st.code(email, language="markdown")
                    logging.info(f"Successfully generated email {i+1}")

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            st.error(f"An Error Occurred: {str(e)}")
            st.info("Please check the URL and try again. Make sure it's a valid job posting.")


if __name__ == "__main__":
    try:
        # Initialize components
        logging.info("Initializing application components")
        
        # Check for required environment variables
        import os
        if not os.environ.get('GROQ_API_KEY'):
            logging.warning("GROQ_API_KEY environment variable not set. Using .env file if available.")
        
        # Initialize chain and portfolio
        chain = Chain()
        
        # Use environment variable for portfolio file path if available
        portfolio_path = os.environ.get('PORTFOLIO_PATH', './sample_portfolio.csv')
        portfolio = Portfolio(file_path=portfolio_path)
        
        # Configure Streamlit page
        st.set_page_config(
            layout="wide", 
            page_title="Cold Email Generator",
            page_icon="✉️"
        )
        
        # Start the application
        logging.info("Starting Cold Email Generator application")
        create_streamlit_app(chain, portfolio, clean_text)
        
    except Exception as e:
        logging.error(f"Application startup error: {str(e)}")
        st.error(f"Application Error: {str(e)}")
        st.info("Please check your configuration and try again.")
        if os.environ.get('RENDER'):
            # Additional logging for Render deployment
            logging.error(f"Render deployment error: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())