# Start with a lightweight Python base image
FROM python:3.11-slim

# Update package lists and install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency definition files
COPY pyproject.toml ./

# Install uv, our package manager
RUN pip install uv

# Install the Python dependencies using uv
RUN uv sync

# Copy the rest of the application code into the container
COPY . .

# Set the command to run when the container starts
CMD ["uv", "run", "python", "main.py"]
