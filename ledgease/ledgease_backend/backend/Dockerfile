FROM python:3.12-slim

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project
COPY . .

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 