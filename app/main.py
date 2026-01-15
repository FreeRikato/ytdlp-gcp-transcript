import os
import uvicorn
from fastapi import FastAPI
from .service import fetch_youtube_data

app = FastAPI(
    title="YouTube Subtitles API",
    description="Serverless API to fetch subtitles without file storage",
    version="2.0.0"
)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "youtube-subtitles-api"}

@app.get("/api/subtitles")
def get_subtitles(url: str):
    """
    Fetches English subtitles for a given YouTube URL.
    """
    if not url:
        return {"error": "URL parameter is required"}
        
    result = fetch_youtube_data(url)
    return {"success": True, **result}

# Entry point for running directly (for debugging)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
