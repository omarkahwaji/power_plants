# Use the official Python image
FROM python:3.11-bullseye

# Set the working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the rest of the code
COPY . .

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
