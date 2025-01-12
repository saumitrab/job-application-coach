#!/bin/bash

service nginx start

# Start the frontend server
streamlit run frontend/streamlit_app.py --server.port 7860 & echo $! > frontend_server.pid

# Start the backend server
uvicorn --app-dir "./backend/" "fastapi_app:app" --port 8501 --host 0.0.0.0

# # Stop the frontend server
# pkill -F frontend_server.pid
# rm frontend_server.pid