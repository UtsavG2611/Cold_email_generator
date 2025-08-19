import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import logging

# Import custom modules
from chains import Chain  # Handles LLM interactions
from portfolio import Portfolio  # Manages portfolio data and queries
from utils import clean_text  # Text preprocessing utility
from github_readme import GitHubReadmeGenerator  # GitHub README generator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def create_email_generator(llm, portfolio, clean_text):
    st.title("Cold Email Generator")
    
    # Add card-like container for input
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 30px;">
        <h3 style="text-align: center; margin-bottom: 20px;">Enter a job posting URL to generate a cold email</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a centered input with better styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        url_input = st.text_input("Enter a URL:", placeholder="https://example.com/job-posting")
        submit_button = st.button("Generate Email", use_container_width=True)

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
            
            st.markdown("<h2 style='text-align: center; color: #1E88E5; margin-top: 30px; margin-bottom: 20px;'>Generated Cold Emails</h2>", unsafe_allow_html=True)
            
            for i, job in enumerate(jobs):
                with st.spinner(f"Generating email {i+1}..."):
                    skills = job.get("skills", [])
                    portfolio_urls = portfolio.query_links(skills)
                    email = llm.write_email(job, portfolio_urls)
                    
                    # Create a card-like container for each email
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                        <h3 style="text-align: center; color: #1E88E5; margin-bottom: 15px;">Email {i+1}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.code(email, language="markdown")
                    logging.info(f"Successfully generated email {i+1}")

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            st.error(f"An Error Occurred: {str(e)}")
            st.info("Please check the URL and try again. Make sure it's a valid job posting.")


def create_github_readme_generator(github_readme_generator):
    st.title("GitHub README Generator")
    
    # Add card-like container for input
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 30px;">
        <h3 style="text-align: center; margin-bottom: 20px;">Enter a GitHub repository URL to generate a README file</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a centered input with better styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        repo_url = st.text_input("Enter a GitHub repository URL:", placeholder="https://github.com/username/repository")
        submit_button = st.button("Generate README", use_container_width=True)

    if submit_button:
        if not repo_url:
            st.warning("Please enter a valid GitHub repository URL")
            return
            
        try:
            with st.spinner("Loading repository data..."):
                repo_data = github_readme_generator.extract_repo_info(repo_url)
                logging.info(f"Successfully loaded data from {repo_url}")
            
            with st.spinner("Generating README file..."):
                readme = github_readme_generator.generate_readme(repo_data, repo_url)
                logging.info("Successfully generated README file")
            
            st.markdown("<h2 style='text-align: center; color: #1E88E5; margin-top: 30px; margin-bottom: 20px;'>Generated README</h2>", unsafe_allow_html=True)
            
            # Create a card-like container for the README
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                <h3 style="text-align: center; color: #1E88E5; margin-bottom: 15px;">README.md</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.code(readme, language="markdown")
            
            # Add a styled container for the download button
            st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
            
            # Add a download button for the README file
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="Download README.md",
                    data=readme,
                    file_name="README.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            st.error(f"An Error Occurred: {str(e)}")
            st.info("Please check the URL and try again. Make sure it's a valid GitHub repository URL.")


def create_selection_page():
    st.title("AI Content Generator")
    st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>Select what you want to generate</h3>", unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("""<style>
        .stButton>button {
            width: 100%;
            height: 50px;
            font-size: 18px;
            margin-top: 10px;
        }
        .card {
            border-radius: 10px;
            padding: 20px;
            background-color: #f8f9fa;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }
        .icon {
            font-size: 40px;
            text-align: center;
            margin-bottom: 15px;
        }
    </style>""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="icon">✉️</div>
            <h3 style="text-align: center;">Cold Email Generator</h3>
            <p style="text-align: center; margin-bottom: 20px;">Generate personalized cold emails based on job postings</p>
        </div>
        """, unsafe_allow_html=True)
        email_button = st.button("Generate Cold Emails")
    
    with col2:
        st.markdown("""
        <div class="card">
            <div class="icon">📝</div>
            <h3 style="text-align: center;">GitHub README Generator</h3>
            <p style="text-align: center; margin-bottom: 20px;">Generate professional README files for GitHub repositories</p>
        </div>
        """, unsafe_allow_html=True)
        readme_button = st.button("Generate GitHub README")
    
    # Add footer
    st.markdown("<div style='text-align: center; margin-top: 50px; color: #6c757d;'>Created by Utsav Gupta</div>", unsafe_allow_html=True)
    
    return email_button, readme_button


if __name__ == "__main__":
    try:
        # Initialize components
        logging.info("Initializing application components")
        
        # Check for required environment variables
        import os
        if not os.environ.get('GROQ_API_KEY'):
            logging.warning("GROQ_API_KEY environment variable not set. Using .env file if available.")
        
        # Configure Streamlit page with modern settings
        st.set_page_config(
            layout="wide", 
            page_title="AI Content Generator",
            page_icon="🤖",
            initial_sidebar_state="collapsed"
        )
        
        # Custom CSS to improve overall UI
        st.markdown("""
        <style>
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 1000px;
            }
            h1 {
                text-align: center;
                color: #1E88E5;
                margin-bottom: 2rem;
                font-weight: 700;
            }
            .stButton button:hover {
                background-color: #1E88E5;
                color: white;
                border: none;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Create session state to track the current page
        if 'page' not in st.session_state:
            st.session_state.page = 'selection'
        
        # Initialize components based on the selected page
        if st.session_state.page == 'email':
            # Initialize chain and portfolio for email generation
            chain = Chain()
            portfolio_path = os.environ.get('PORTFOLIO_PATH', './sample_portfolio.csv')
            portfolio = Portfolio(file_path=portfolio_path)
            create_email_generator(chain, portfolio, clean_text)
            
            # Add a styled back button
            st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Back to Selection", use_container_width=True):
                    st.session_state.page = 'selection'
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
                
        elif st.session_state.page == 'readme':
            # Initialize GitHub README generator
            github_readme_generator = GitHubReadmeGenerator()
            create_github_readme_generator(github_readme_generator)
            
            # Add a styled back button
            st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Back to Selection", use_container_width=True):
                    st.session_state.page = 'selection'
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
                
        else:  # selection page
            # Show the selection page
            email_button, readme_button = create_selection_page()
            
            # Handle navigation based on button clicks
            if email_button:
                st.session_state.page = 'email'
                st.rerun()
            elif readme_button:
                st.session_state.page = 'readme'
                st.rerun()
        
    except Exception as e:
        logging.error(f"Application startup error: {str(e)}")
        st.error(f"Application Error: {str(e)}")
        st.info("Please check your configuration and try again.")
        if os.environ.get('RENDER'):
            # Additional logging for Render deployment
            logging.error(f"Render deployment error: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())