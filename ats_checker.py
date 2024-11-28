import spacy
from rapidfuzz import fuzz
from PyPDF2 import PdfReader
from docx import Document

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined list of technical terms (expand as needed)
TECHNICAL_TERMS = {
    'python', 'java', 'javascript', 'html', 'css', 'sql', 'c++', 'c#', 'ruby',
    'go', 'swift', 'typescript', 'angular', 'react', 'nodejs', 'database',
    'cloud', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'devops',
    'machine learning', 'deep learning', 'data science', 'big data',
    'tensorflow', 'pytorch', 'scikit-learn', 'flask', 'django', 'apache',
    'nginx', 'api', 'json', 'xml', 'graphql', 'microservices', 'rest', 'soap',
    'redis', 'mongodb', 'postgresql', 'mysql', 'nosql', 'git', 'github',
    'bitbucket', 'jenkins', 'automation', 'linux', 'windows', 'unix',
    'security', 'penetration testing', 'firewall', 'encryption', 'ssl',
    'sockets', 'data analysis', 'data visualization', 'etl', 'spark', 'hadoop',
    'docker', 'virtualization', 'ci/cd', 'agile', 'scrum', 'kanban', 'jira',
    'testing', 'qa', 'deployment', 'scrum', 'graphql', 'typescript', 'restful'
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
    return [
        token.text.lower() for token in doc
        if token.is_alpha and token.text.lower() in TECHNICAL_TERMS
    ]


# Function to calculate the match score and missing technical keywords
def calculate_match(resume_text, job_description):
    # Extract relevant keywords from resume and job description
    resume_keywords = set(extract_keywords(resume_text))
    job_keywords = set(extract_keywords(job_description))

    # Apply fuzzy matching to improve keyword matching
    matched_keywords = set()
    for job_kw in job_keywords:
        for resume_kw in resume_keywords:
            if fuzz.partial_ratio(
                    job_kw, resume_kw) > 80:  # Adjust threshold as needed
                matched_keywords.add(job_kw)

    match_count = len(matched_keywords)
    total_keywords = len(job_keywords)

    # Calculate match percentage using ternary operator
    match_percentage = (match_count / total_keywords *
                        100) if total_keywords > 0 else 0

    # Find missing keywords
    missing_keywords = job_keywords - matched_keywords

    return round(match_percentage, 2), list(missing_keywords)


# Example usage
resume_text = "I am a software developer with expertise in JavaScript, Node.js, and React."
job_description = "Looking for a candidate with experience in JavaScript, React.js, and Angular2+."

match_score, missing_keywords = calculate_match(resume_text, job_description)
print(f"Match Score: {match_score}%")
print(f"Missing Keywords: {', '.join(missing_keywords)}")
