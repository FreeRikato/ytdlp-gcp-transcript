import functions_framework
from app.service import fetch_youtube_data
import re

@functions_framework.http
def youtube_subtitles(request):
    """HTTP Cloud Function for YouTube subtitles."""
    request_args = request.args
    request_json = request.get_json(silent=True)
    
    url = request_args.get('url') if request_args else None
    if not url and request_json:
        url = request_json.get('url')
    
    if not url:
        return {'error': 'URL parameter is required'}, 400
    
    youtube_pattern = r'^https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}'
    if not re.match(youtube_pattern, url):
        return {'error': 'Invalid YouTube URL format'}, 400
    
    try:
        result = fetch_youtube_data(url)
        return {'success': True, **result}, 200
    except Exception as e:
        return {'error': str(e)}, 500