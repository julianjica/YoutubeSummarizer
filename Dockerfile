# Start with a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency definition files
COPY pyproject.toml ./

# Install uv, our package manager
RUN pip install uv

# Install the Python dependencies using uv
# This creates the virtual environment inside the container
RUN uv sync

# Copy the rest of your application code into the container
COPY . .

# Set the command to run when the container starts
CMD ["uv", "run", "python", "main.py"]
