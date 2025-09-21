# Use Python 3.10 base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app code into container
COPY . .

# Expose port 8000 (Django default)
EXPOSE 8000

# Command to run the app (adjust if different)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "-p"]

