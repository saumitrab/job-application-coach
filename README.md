---
title: Job Hunt Coach
emoji: 🚀
colorFrom: purple
colorTo: indigo
sdk: docker
app_port: 7860
---

# Job Hunt Coach

This application helps users tailor their resumes to better match job descriptions. By leveraging AI, it analyzes the job description and the user's resume, then provides an updated resume that highlights the most relevant areas, ensuring the best possible match.

## Features
- Analyze job descriptions and resumes
- Generate tailored resumes
- Provide feedback on resume improvements

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Uvicorn
- Streamlit

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/job-application-coach.git
    cd job-application-coach/backend
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the `backend` directory and add your API key:
    ```env
    GROQCLOUD_API_KEY=your_groqcloud_api_key
    ```

### Running the Backend

Start the FastAPI backend using Uvicorn:
```sh
uvicorn fastapi_app:app --reload
```

### Running the Frontend

Navigate to the `frontend` directory and start the Streamlit app:
```sh
cd ../frontend
streamlit run app.py
```

### Running the docker

```
docker build -t coach .
docker run -it -p 7860:7860 coach
```

### Usage

1. Open your browser and navigate to the Streamlit app (usually at `http://localhost:8501`).
2. Enter the job description and your resume.
3. Click the "Analyze" button to receive a tailored resume and feedback.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Groq](https://groq.com/)