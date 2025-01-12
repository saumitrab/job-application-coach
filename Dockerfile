# Use the official Python image from the Docker Hub
FROM python:3.10

# Install nginx and give permissions to 'user'
# See https://www.rockyourcode.com/run-docker-nginx-as-non-root-user/
USER root

RUN apt-get -y update && apt-get -y install nginx

RUN mkdir -p /var/cache/nginx \
             /var/log/nginx \
             /var/lib/nginx
RUN touch /var/run/nginx.pid

# Install dependencies and build app as non-root
RUN useradd -m -u 1000 user

RUN chown -R user:user /var/cache/nginx \
                       /var/log/nginx \
                       /var/lib/nginx \
                       /var/run/nginx.pid

USER user


ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY --chown=user ./requirements.txt app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r app/requirements.txt

# Copy nginx configuration
COPY --chown=user nginx.conf /etc/nginx/sites-available/default

# Copy the rest of the application code into the container
COPY --chown=user . /app

# Expose the port that app will run on
EXPOSE 7860

# Command to run the Streamlit app

CMD ["bash", "run.sh"]
# CMD ["streamlit", "run", "streamlit_app.py"]
# CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8501"]