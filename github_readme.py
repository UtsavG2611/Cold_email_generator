import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class GitHubReadmeGenerator:
    def __init__(self):
        self.llm = ChatGroq(
                        model="llama-3.1-8b-instant",
                        temperature=0,
                        max_tokens=None,
                        timeout=None,
                        max_retries=2)
    
    def extract_repo_info(self, repo_url):
        """Extract information from a GitHub repository URL"""
        try:
            # Ensure the URL is a GitHub repository URL
            if 'github.com' not in repo_url:
                raise ValueError("The provided URL is not a GitHub repository URL")
            
            # Modify URL to get the raw content if needed
            if repo_url.endswith('/'):
                repo_url = repo_url[:-1]
                
            # Load the repository page
            loader = WebBaseLoader([repo_url])
            data = loader.load().pop().page_content
            logging.info(f"Successfully loaded data from {repo_url}")
            
            return data
        except Exception as e:
            logging.error(f"Error extracting repo info: {str(e)}")
            raise e
    
    def generate_readme(self, repo_data, repo_url):
        """Generate a README file based on repository data"""
        prompt_readme = PromptTemplate.from_template(
            """
            I will give you information about a GitHub repository. Your task is to generate a comprehensive README.md file for this repository.
            
            The README should include the following sections:
            1. Project Title and Description
            2. Features
            3. Installation Instructions
            4. Usage Examples
            5. Technologies Used
            6. Contributing Guidelines
            7. License Information
            
            Make the README professional, well-structured, and informative. Use proper Markdown formatting.
            
            Repository URL: {repo_url}
            Repository Information: {repo_data}
            
            Generate a complete README.md file:
            """
        )
        
        chain_readme = prompt_readme | self.llm
        response = chain_readme.invoke({"repo_data": repo_data, "repo_url": repo_url})
        
        return response.content