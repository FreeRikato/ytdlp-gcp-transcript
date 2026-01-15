# 1. Base Image: Use a slim version of Python 3.11 to keep size down
FROM python:3.11-slim

# 2. Environment Variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# PYTHONUNBUFFERED: Ensures logs are flushed directly to terminal (important for Docker logging)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set Working Directory
WORKDIR /app

# 4. Install Dependencies
# Copy requirements first to leverage Docker cache layers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Application Code
COPY app ./app

# 6. Expose Port (Documentation only, Cloud Run ignores this but good practice)
EXPOSE 8080

# 7. Start the application
# We use 'app.main:app' because our main.py is inside the 'app' folder
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
