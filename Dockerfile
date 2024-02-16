# Use the official Python image as a parent image
FROM python:3.10-slim-buster

# Set environment variables to control Python output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY . /app/

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the application will run on
EXPOSE 8001

# Set environment variables for your application
ENV MODULE_NAME=app.main
ENV VARIABLE_NAME=app
ENV RELOAD="true"

# Command to run your application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]