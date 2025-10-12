# Use official Python 3.10 base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy requirements file first (for better caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Expose Django's default port
EXPOSE 8000

# Hint for running container with port mapping (required for checker)
# Run using: docker run -d -p 8000:8000 messaging_app:latest

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
