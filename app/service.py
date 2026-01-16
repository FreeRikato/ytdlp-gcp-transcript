import yt_dlp
import shutil
import uuid
import os
import glob
import logging
from yt_dlp.networking.impersonate import ImpersonateTarget
from .utils import clean_vtt_text

logger = logging.getLogger(__name__)

TEMP_DIR_BASE = os.environ.get('TEMP_DIR', '/tmp')
YDLP_TIMEOUT = int(os.environ.get('YDLP_TIMEOUT', '300'))

def fetch_youtube_data(video_url: str):
    request_id = str(uuid.uuid4())
    temp_dir = f"{TEMP_DIR_BASE}/{request_id}"
    os.makedirs(temp_dir, exist_ok=True)

    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'vtt',
        'quiet': True,
        'no_warnings': True,
        'outtmpl': f'{temp_dir}/%(id)s.%(ext)s',
        'impersonate': ImpersonateTarget.from_str('chrome'),
        'js_runtimes': {'node': {}},
        'socket_timeout': YDLP_TIMEOUT,
        'extractor_args': {
            'youtube': {
                'skip': ['dash', 'hls']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            metadata = {
                "id": info.get('id'),
                "title": info.get('title'),
                "channel": info.get('uploader'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration')
            }

            ydl.download([video_url])

            vtt_files = glob.glob(f"{temp_dir}/*.vtt")
            
            if not vtt_files:
                raise ValueError("No English subtitles found.")

            with open(vtt_files[0], 'r', encoding='utf-8') as f:
                raw_vtt = f.read()

            clean_subs = clean_vtt_text(raw_vtt)

            return {
                "metadata": metadata,
                "subtitles": clean_subs,
                "count": len(clean_subs)
            }

    except yt_dlp.utils.DownloadError as e:
        error_str = str(e)
        if "429" in error_str:
            logger.error(f"CRITICAL: IP {request_id} Blocked by YouTube (429).")
            raise ValueError("Server IP blocked by YouTube. Please try again later.")
        raise ValueError("Invalid URL or video unavailable.")
        
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
