# 1. Base Image: Use a slim version of Python 3.11 to keep size down
FROM python:3.11-slim

# 2. Environment Variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# PYTHONUNBUFFERED: Ensures logs are flushed directly to terminal (important for Docker logging)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set Working Directory
WORKDIR /app

# 4. Install System Dependencies
# Install nodejs so yt-dlp has a runtime to execute YouTube's JS
RUN apt-get update && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# 5. Install Dependencies
# Copy requirements first to leverage Docker cache layers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Application Code
COPY app ./app

# 7. Expose Port (Documentation only, Cloud Run ignores this but good practice)
EXPOSE 8080

# 8. Start the application
# We use 'app.main:app' because our main.py is inside the 'app' folder
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
