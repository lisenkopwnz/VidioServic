FROM python:3.12-slim-bullseye

# Set up environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

# Set working directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN apt-get update -y && \
    apt-get install -y netcat && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy all files
COPY . .

# Move entrypoint.sh to a directory in $PATH and make it executable
RUN mv /code/entrypoint.sh /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

# Use entrypoint for the container
ENTRYPOINT ["entrypoint.sh"]

# Default command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
