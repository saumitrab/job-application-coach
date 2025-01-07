import streamlit as st
import requests
import streamlit.components.v1 as components

st.title("Resume Customization Assistant")

job_description = st.text_area("Paste Job Description:", "")
resume_content = st.text_area("Paste Resume:", "")

if st.button("Analyze"):
    if not job_description or not resume_content:
        st.error("Please provide both Job Description and Resume.")
    else:
        payload = {"job_description": job_description, "resume": resume_content}
        try:
            response = requests.post("http://localhost:8000/analyze_job_resume", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.write("Match Score:", data.get("match_score"), "%")
                st.write("Feedback:", data.get("feedback"))
                updated_resume = data.get("updated_resume")
                style = """
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Computer+Modern&display=swap');
                    body {
                        background-color: white;
                        color: black;
                        font-family: 'Computer Modern', serif;
                    }
                </style>
                """
                components.html(style + updated_resume, height=2000, scrolling=True)
            else:
                st.error("Error from server.")
        except Exception as e:
            st.error("Could not reach the backend.")