import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import os
from io import BytesIO
import tempfile

# Page configuration
    st.set_page_config(page_title="JOBIEE", layout="centered")

# Initialize OpenAI API
client = OpenAI()

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'degree' not in st.session_state:
    st.session_state.degree = ''
if 'job_position' not in st.session_state:
    st.session_state.job_position = ''
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = ''
if 'cv_file' not in st.session_state:
    st.session_state.cv_file = None
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0

# Sample data for companies (replace with your data)
companies_data = {
    'Undergraduate': {
        'Junior': [
            {'name': 'Motive', 'Education': 'bachelor AI engineering', 'Degree': 'Undergraduate', 'position': 'Junior', 
             'company_information': "A cutting-edge AI company focusing on developing intelligent systems and AI-based solutions for various industries.",
             'job_description': 'Assist in developing AI models and maintaining AI systems. Candidate must have skill of Python and machine learning concepts. this job is for making AI model by coding  '},
            {'name': 'Adept Tech Solutions', 'Education': 'bachelor AI engineering', 'Degree': 'Undergraduate', 'position': 'Junior', 
             'company_information': "An emerging tech company focused on AI development and providing innovative AI solutions to clients.",
             'job_description': 'Support AI development projects by building and testing models. Candidate must have knowledge of Python, machine learning algorithms, and data preprocessing techniques.this job is for making AI model by coding '},
            {'name': 'Coca cola', 'Education': 'bachelor Business Administration', 'Degree': 'Undergraduate', 'position': 'Internship', 
             'company_information': "A global leader in the beverage industry, known for its iconic soft drinks and extensive product portfolio.",
             'job_description': 'Gain hands-on experience in business operations through assisting various departments. Candidate should be familiar with basic business processes and office software like MS Office.'}
        ],
        'Senior': []
    },
    'Graduate': {
        'Junior': [
            {'name': 'Jazz', 'Education': 'bachelor AI engineering', 'Degree': 'graduate', 'position': 'Junior', 
             'company_information': "Pakistan's largest mobile network and internet services provider formed by the merger of Mobilink and Warid Pakistan.",
             'job_description': 'Support AI development projects by building and testing models. Candidate must have knowledge of Python, machine learning algorithms, and data preprocessing techniques.this job is for making AI model by coding '},
        ],
        'Senior': [
            {'name': 'System', 'Education': 'bachelor Data Science', 'Degree': 'Post Graduate', 'position': 'Senior', 
             'company_information': "A data analytics firm specializing in extracting insights from large datasets to drive business decisions.",
             'job_description': 'Analyze large datasets to derive actionable insights for business improvement. Candidate must be skilled in Python, R, SQL, and data visualization tools.This job is for data analyzes '},
           {'name': 'Increative', 'Education': 'bachelor website development', 'Degree': 'Graduate', 'position': 'Senior', 
             'company_information': "A creative agency specializing in web development and digital marketing solutions for clients globally.",
             'job_description': 'Lead web development projects, ensuring functionality and design meet client requirements. Candidate must be proficient in HTML, CSS, JavaScript, and web development frameworks like React or Angular.this job is for website coder'},
            {'name': 'Angro', 'Education': 'bachelor Business Administration', 'Degree': 'Graduate', 'position': 'Senior', 
             'company_information': "A prominent business conglomerate in Pakistan, with interests in various sectors including fertilizers, energy, and consumer goods.",
             'job_description': 'Manage business operations and oversee administrative tasks. Candidate should have strong leadership skills and knowledge of project management.'}
        ]
    },
    'Post Graduate': {
        'Junior': [],
        'Senior': [
            {'name': 'Coding Souls', 'Education': 'bachelor Software Engineering', 'Degree': 'Post Graduate', 'position': 'Senior', 
             'company_information': "A leading software development company specializing in custom software solutions and innovative technology.",
             'job_description': 'Responsible for leading software development teams to create innovative software solutions. Candidate must be proficient in Java, C++, and Python.This job is for making softwares by coding'}
        ]
    }
}

def personal_info():
    
    st.markdown("<h2 style='color: Blue;'>JOBEE</h2>", unsafe_allow_html=True)
    st.header("Personal Information")
    name = st.text_input("Name")
    degree = st.selectbox("Degree", ["Undergraduate", "Graduate", "Post Graduate"])
    job_position = st.selectbox("Job Position", ["Junior", "Senior"])
    education = st.text_input('Education')

    if st.button("Submit"):
        if name and degree and job_position and education:
            st.session_state.name = name
            st.session_state.degree = degree
            st.session_state.job_position = job_position
            st.session_state.education = education
            st.session_state.page += 1
        else:
            st.error("Please fill in all fields before submitting.")

def company_selection():
    st.title("Company Selection")
    
    degree = st.session_state.degree
    job_position = st.session_state.job_position
    education = st.session_state.education

    eligible_companies = []
    for degree_key, position_dict in companies_data.items():
        if degree_key == degree:
            for position_key, company_list in position_dict.items():
                if position_key == job_position:
                    for company in company_list:
                        if company['Education'].lower() in education.lower():
                            eligible_companies.append(company['name'])

    if eligible_companies:
        selected_company = eligible_companies[0]  # Select the first eligible company
        st.write(f"Based on your information, we've selected: {selected_company}")
        st.session_state.selected_company = selected_company
        if st.button("Continue"):
            st.session_state.page += 1
    else:
        st.write("No eligible companies found for your degree and job position.")
        if st.button("Go back"):
            st.session_state.page -= 1

def company_info():
    st.title(f"Company: {st.session_state.selected_company}")
    
    selected_company = st.session_state.selected_company
    
    company_info = None
    job_description = "No description available."
    
    for degree_key, position_dict in companies_data.items():
        for position_key, company_list in position_dict.items():
            for company in company_list:
                if company['name'] == selected_company:
                    company_info = company.get('company_information', 'No information available.')
                    job_description = company.get('job_description', 'No description available.')
                    break
    
    if company_info:
        st.write(f"Information about {selected_company}:\n{company_info}")
    
    st.write(f"Job Description for {selected_company}:\n{job_description}")
    
    cv_file = st.file_uploader("Upload your CV", type=["pdf", "docx", "txt"])
    
    if cv_file is not None:
        st.session_state.cv_file = cv_file
        st.success("CV uploaded successfully!")
        if st.button("Submit and Proceed to Interview"):
            st.session_state.page += 1

def interview_questions():
    st.title("Interview Questions")
    selected_company = st.session_state.selected_company
    job_position = st.session_state.job_position
    job_description = next(
        (company['job_description'] for degree_key, position_dict in companies_data.items()
        for position_key, company_list in position_dict.items()
        for company in company_list if company['name'] == selected_company), "No description available."
    )

    cv_file = st.session_state.cv_file

    coding_related = any(keyword in job_description.lower() for keyword in ['coding', 'python', 'java', 'c++', 'programming', 'developer'])

    difficulty = "easy" if job_position.lower() == "junior" else "medium" if job_position.lower() == "senior" else "hard"

    questions = []

    if coding_related:
        coding_prompt = f"Generate 2 {difficulty} coding interview questions based on the following job description:\n{job_description}"
        if cv_file:
            coding_prompt += f"\n\nAnd the candidate's CV:\n{cv_file.name}"
        
        coding_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": coding_prompt}
            ]
        )
        
        coding_questions = coding_response.choices[0].message.content.strip().split("\n")
        coding_questions = [q.strip() for q in coding_questions if q.strip()][:2]

        general_prompt = f"Generate 3 general interview questions based on the following job description:\n{job_description}"
        if cv_file:
            general_prompt += f"\n\nAnd the candidate's CV:\n{cv_file.name}"
        
        general_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": general_prompt}
            ]
        )
        
        general_questions = general_response.choices[0].message.content.strip().split("\n")
        general_questions = [q.strip() for q in general_questions if q.strip()][:3]

        questions = coding_questions + general_questions

    else:
        general_prompt = f"Generate 5 general interview questions based on the following job description:\n{job_description}"
        if cv_file:
            general_prompt += f"\n\nAnd the candidate's CV:\n{cv_file.name}"
        
        general_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": general_prompt}
            ]
        )
        
        questions = general_response.choices[0].message.content.strip().split("\n")
        questions = [q.strip() for q in questions if q.strip()][:5]

    st.session_state.questions = questions
    st.session_state.current_question_index = st.session_state.get('current_question_index', 0)
    st.session_state.answers = st.session_state.get('answers', [])

    if st.session_state.current_question_index < len(questions):
        question = questions[st.session_state.current_question_index]
        answer = st.text_area(f"{question}")
        st.session_state.answers.append((question, answer))
        
        if st.button("Next Question"):
            # Evaluate the answer
            evaluation_prompt = f"""
            Question: {question}
            User's Answer: {answer}

            Evaluate the user's answer for its accuracy, clarity, and completeness based on the given question. Provide a score from 1 to 10 and specific feedback on how the answer can be improved.
            """
            
            evaluation_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": evaluation_prompt}
                ]
            )
            
            feedback = evaluation_response.choices[0].message.content.strip()
            st.write(f"*Evaluation Feedback:* {feedback}")

            st.session_state.current_question_index += 1

    if st.session_state.current_question_index >= len(questions):
        st.session_state.page += 1

def generate_report():
    st.title("Report")

    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="JOBIEE - Interview Report", ln=True, align="C")
    pdf.ln(10)

    # User Information
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="User Information", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {st.session_state.get('name', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Degree: {st.session_state.get('degree', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Job Position: {st.session_state.get('job_position', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Education: {st.session_state.get('education', 'N/A')}", ln=True)
    pdf.ln(10)

    # Selected Company
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Selected Company", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Company: {st.session_state.get('selected_company', 'N/A')}", ln=True)
    pdf.ln(10)

    # Interview Questions and Answers
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Interview Questions and Answers", ln=True)
    pdf.set_font("Arial", size=12)

    total_score = 0
    num_questions = len(st.session_state.get('answers', []))

    for question, answer in st.session_state.get('answers', []):
        pdf.multi_cell(0, 10, txt=f"Question: {question}")
        pdf.multi_cell(0, 10, txt=f"Answer: {answer}")

        evaluation_prompt = f"""
        Question: {question}
        User's Answer: {answer}

        Evaluate the user's answer for its accuracy, clarity, and completeness based on the given question. Provide a score from 1 to 10 and specific feedback on how the answer can be improved. Start your response with 'Score: X/10' where X is the numeric score.
        """

        evaluation_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": evaluation_prompt}
            ]
        )

        feedback = evaluation_response.choices[0].message.content.strip()
        pdf.multi_cell(0, 10, txt=f"Feedback: {feedback}")
        pdf.ln(5)

        # Extract score from feedback
        try:
            score_text = feedback.split('\n')[0]  # Get the first line
            score = int(score_text.split(':')[1].split('/')[0].strip())
            total_score += score
        except (ValueError, IndexError):
            st.warning(f"Could not parse score for question: {question}")
            num_questions -= 1  # Reduce count if score couldn't be parsed

    # Calculate and add overall score
    overall_score = total_score / num_questions if num_questions > 0 else 0
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Overall Score: {overall_score:.2f}/10", ln=True)

    # Save PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        pdf.output(temp_file.name)
        temp_file.flush()
        temp_file.seek(0)  # Move cursor to the beginning of the file

        # Read the temporary file into a BytesIO object
        pdf_data = temp_file.read()
        pdf_buffer = BytesIO(pdf_data)

    # Provide download link
    st.download_button(
        label="Download Report",
        data=pdf_buffer,
        file_name="interview_report.pdf",
        mime="application/pdf"
    )

def main():

    if  st.session_state.page == 0:
        personal_info()
    elif st.session_state.page == 1:
        company_selection()
    elif st.session_state.page == 2:
        company_info()
    elif st.session_state.page == 3:
        interview_questions()
    elif st.session_state.page == 4:
        generate_report()

if __name__ == "__main__":
    main()