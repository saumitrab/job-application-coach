import streamlit as st
import requests
import streamlit.components.v1 as components

st.markdown("<h1 style='text-align: center;'>Job Hunt Coach</h1>", unsafe_allow_html=True)

job_description = "Paste the job description here."
resume_content = "Your resume content here."

# Initialize session state to store chat log
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = "Welcome to the chat!\n"

# # Ensure 'current_user_message' is initialized before widget is created
# if 'current_user_message' not in st.session_state:
#     st.session_state.current_user_message = ""

# Define a custom HTML template with a script to scroll the text area
scroll_script = f"""
<script>
var e = document.querySelector('[aria-label="Chat Log"]');
e.scrollTop = e.scrollHeight
</script>
"""


col1, col2 = st.columns(2)

with col1:
    job_description = st.text_area("Paste the job description:", job_description, height=300)
    resume_content = st.text_area("Your Resume:", resume_content, height=300)

with col2:
    st.subheader("Talk to the coach")
    # Chat log display
    st.text_area("Chat Log", value=st.session_state.chat_log, height=300, disabled=True, key="chat_log_area")


    # User input and send button
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Your Message", key="user_input")
        submitted = st.form_submit_button("Send")
        
        if submitted and user_input.strip():
            if not job_description or not resume_content:
                st.error("Please provide both Job Description and Resume.")
            else:
                payload = {"job_description": job_description, "resume": resume_content, "user_message": user_input}
                try:
                    response = requests.post("http://localhost:8000/hey_coach", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        coach_message = data.get("coach_message", "No response")
                        
                        # Append user input and coach message to chat log
                        st.session_state.chat_log += f"User: {user_input}\nCoach: {coach_message}\n"
                        
                        # Clear input and rerun
                        st.rerun()
                    else:
                        st.error("Error from server.")
                except Exception as e:
                    st.error("Could not reach the backend.")
                    st.write(f"Exception: {e}")