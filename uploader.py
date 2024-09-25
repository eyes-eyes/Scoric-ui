from flask import Flask, render_template, request, flash
import os
from docx import Document
import PyPDF2
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret"

# Function to read .docx file
def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to read .pdf file
def read_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

# Function to read .csv file
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string()

# Handle text or file uploads
@app.route('/', methods=['GET', 'POST'])
def index():
    rubric_text = ""
    student_work_text = ""

    if request.method == 'POST':
        # Rubric Text or File Handling
        if 'rubric_text' in request.form:
            rubric_text = request.form['rubric_text']
        rubric_file = request.files.get('rubric_file')
        if rubric_file and rubric_file.filename != '':
            rubric_file_path = os.path.join(app.config['UPLOAD_FOLDER'], rubric_file.filename)
            rubric_file.save(rubric_file_path)

            if rubric_file.filename.endswith('.docx'):
                rubric_text = read_docx(rubric_file_path)
            elif rubric_file.filename.endswith('.pdf'):
                rubric_text = read_pdf(rubric_file_path)
            elif rubric_file.filename.endswith('.csv'):
                rubric_text = read_csv(rubric_file_path)
            elif rubric_file.filename.endswith('.txt'):
                rubric_text = rubric_file.read().decode('utf-8')

        # Student Work Text or File Handling
        if 'student_work_text' in request.form:
            student_work_text = request.form['student_work_text']
        student_work_file = request.files.get('student_work_file')
        if student_work_file and student_work_file.filename != '':
            student_work_file_path = os.path.join(app.config['UPLOAD_FOLDER'], student_work_file.filename)
            student_work_file.save(student_work_file_path)

            if student_work_file.filename.endswith('.docx'):
                student_work_text = read_docx(student_work_file_path)
            elif student_work_file.filename.endswith('.pdf'):
                student_work_text = read_pdf(student_work_file_path)
            elif student_work_file.filename.endswith('.txt'):
                student_work_text = student_work_file.read().decode('utf-8')

        flash('Files received successfully!')
    return render_template('index.html', rubric_text=rubric_text, student_work_text=student_work_text)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)