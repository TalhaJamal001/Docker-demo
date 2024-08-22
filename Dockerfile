# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the rest of the application code
COPY . .

# Command to run your application
CMD ["python", "main.py"]
