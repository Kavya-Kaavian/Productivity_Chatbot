# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install pipenv
RUN pip install pipenv

# Move to the server directory where Pipfile is
WORKDIR /app/server

# Install dependencies defined in Pipfile.lock
RUN pipenv install --deploy --ignore-pipfile

# Expose the port FastAPI will run on
EXPOSE 80

# Run the FastAPI app (main.py must define app = FastAPI())
CMD ["pipenv", "run", "uvicorn", "index:app", "--host", "0.0.0.0", "--port", "80"]
