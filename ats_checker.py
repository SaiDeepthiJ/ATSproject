# ats_checker.py

import spacy
from rapidfuzz import fuzz
from PyPDF2 import PdfReader
from docx import Document

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined list of technical terms (expand as needed)
TECHNICAL_TERMS = {
    'python', 'java', 'javascript', 'html', 'css', 'sql', 'c++', 'c#', 'ruby', 'go', 'swift', 'typescript', 'angular', 'react', 'nodejs',
    'database', 'cloud', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'devops', 'machine learning', 'deep learning', 'data science',
    'big data', 'tensorflow', 'pytorch', 'scikit-learn', 'flask', 'django', 'apache', 'nginx', 'api', 'json', 'xml', 'graphql', 'microservices',
    'rest', 'soap', 'redis', 'mongodb', 'postgresql', 'mysql', 'nosql', 'git', 'github', 'bitbucket', 'jenkins', 'automation', 'linux', 'windows',
    'unix', 'security', 'penetration testing', 'firewall', 'encryption', 'ssl', 'sockets', 'data analysis', 'data visualization', 'etl', 'spark', 'hadoop',
    'docker', 'virtualization', 'ci/cd', 'agile', 'scrum', 'kanban', 'jira', 'testing', 'qa', 'deployment', 'scrum', 'graphql', 'typescript', 'restful'
}

# Function to extract text from PDF or DOCX files
def extract_text_from_file(filepath):
    if filepath.endswith('.pdf'):
        reader = PdfReader(filepath)
        return " ".join([page.extract_text() for page in reader.pages])
    elif filepath.endswith('.docx'):
        doc = Document(filepath)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        return ""

# Function to extract keywords (technical terms) from the text
def extract_keywords(text):
    doc = nlp(text)
    return [token.text.lower() for token in doc if token.is_alpha and token.text.lower() in TECHNICAL_TERMS]

# Function to calculate the match score and missing technical keywords
def calculate_match(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    # Use rapidfuzz to calculate match score based on keyword overlap
    match_score = fuzz.partial_ratio(" ".join(resume_keywords), " ".join(job_keywords))

    # Find keywords in the job description that are missing in the resume
    missing_keywords = set(job_keywords) - set(resume_keywords)

    return match_score, missing_keywords
