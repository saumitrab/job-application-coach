import streamlit as st
import requests

# Read default job description and resume
try:
    with open('app/samples/sample_job_description.txt', 'r') as file:
        default_job_description = file.read()
except FileNotFoundError:
    default_job_description = "Paste the job description here."

try:
    with open('app/samples/sample_resume.txt', 'r') as file:
        default_resume_content = file.read()
except FileNotFoundError:
    default_resume_content = "Your resume content here."

st.markdown("<h1 style='text-align: center;'>Job Hunt Coach</h1>", unsafe_allow_html=True)

job_description = default_job_description
resume_content = default_resume_content
suggested_questions ="""
Sample questions to ask the coach:
1. How can I improve my resume?"
2. What skills should I add to my resume?
3. How well does my resume match the job description?
4. How can I prepare for this interview?
5. How can I upskill in required skills?
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.write("The Coach is here you help you improve your resume and prepare for job interviews")
    job_description = st.text_area("Paste the job description:", job_description, height=300)
    resume_content = st.text_area("Your Resume:", resume_content, height=300)
    st.write(suggested_questions)
    

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask the coach..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not job_description or not resume_content:
        response = "Please provide both Job Description and Resume."
        st.error(response)
    else:
        payload = {
            "job_description": job_description,
            "resume": resume_content,
            "user_message": prompt
        }
        try:
            api_response = requests.post("http://backend:7860/hey_coach", json=payload)
            if api_response.status_code == 200:
                data = api_response.json()
                coach_message = data.get("coach_message", "No response")
                
                # Display coach response
                with st.chat_message("assistant"):
                    st.markdown(coach_message)
                # Add coach response to chat history
                st.session_state.messages.append({"role": "assistant", "content": coach_message})
            else:
                st.error("Error from server.")
        except Exception as e:
            st.error("Could not reach the backend.")
            st.write(f"Exception: {e}")