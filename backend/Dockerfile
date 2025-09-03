# Start with an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=true

# Set the working directory in the container
WORKDIR /code

# Install system dependencies (gcc, etc. for some Python packages)
RUN apt-get update && apt-get -y install gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt /code/

# Install uv and project dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system -r requirements.txt

# Copy the project files into the container
COPY . /code

# Expose the port number that the application will listen on
EXPOSE 8000

# Start the server with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
