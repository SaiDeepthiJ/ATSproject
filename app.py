from flask import Flask, request, render_template
import os
from ats_checker import extract_text_from_file, calculate_match

app = Flask(__name__)


# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')


# Route for handling file upload and resume/job description comparison
@app.route('/upload', methods=['POST'])
def upload():
    resume_file = request.files['resume']
    job_description = request.form['job_description']

    if resume_file:
        # Save the uploaded resume file
        filepath = os.path.join("uploads", resume_file.filename)
        resume_file.save(filepath)

        # Extract text from the uploaded resume
        resume_text = extract_text_from_file(filepath)

        # Calculate match score and missing keywords using ats_checker
        match_score, missing_keywords = calculate_match(
            resume_text, job_description)

        # Return the results to the user
        return f"Match Score: {match_score}%<br>Missing Keywords: {', '.join(missing_keywords)}"

    return "Error: Please upload a valid resume and job description."


if __name__ == "__main__":
    # Ensure that the uploads folder exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Run the Flask application
    app.run(debug=True)