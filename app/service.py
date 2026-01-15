import yt_dlp
import requests
from fastapi import HTTPException
from .utils import clean_vtt_text

def fetch_youtube_data(video_url: str):
    # Configuration to ensure we don't download the video/audio
    ydl_opts = {
        'skip_download': True,        # We only want metadata
        'writesubtitles': True,       # Signal we are interested in subs
        'writeautomaticsub': True,    # Allow auto-generated subs if manual aren't there
        'subtitleslangs': ['en'],     # English only
        'quiet': True,                # Reduce log noise
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 1. Extract info (network call to YouTube)
            info = ydl.extract_info(video_url, download=False)
            
            # 2. Extract Metadata
            metadata = {
                "id": info.get('id'),
                "title": info.get('title'),
                "channel": info.get('uploader'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration')
            }

            # 3. Locate Subtitle URL
            # yt-dlp structures subtitles in two places: 'subtitles' (manual) and 'automatic_captions'
            # 'requested_subtitles' is a helper field yt-dlp creates for the chosen language
            requested_subs = info.get('requested_subtitles')
            
            if not requested_subs or 'en' not in requested_subs:
                raise HTTPException(status_code=404, detail="No English subtitles found for this video.")

            # The direct URL to the VTT file
            vtt_url = requested_subs['en']['url']

            # 4. Fetch the VTT content from the URL (In-Memory)
            response = requests.get(vtt_url)
            response.raise_for_status()
            raw_vtt = response.text

            # 5. Parse
            clean_subs = clean_vtt_text(raw_vtt)

            return {
                "metadata": metadata,
                "subtitles": clean_subs,
                "count": len(clean_subs)
            }

    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL or video unavailable.")
    except Exception as e:
        # Re-raise HTTP exceptions, wrap others
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
