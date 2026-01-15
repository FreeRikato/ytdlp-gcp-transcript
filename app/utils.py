import re

def clean_vtt_text(vtt_content: str) -> list[str]:
    """
    Parses raw VTT content and returns a list of clean text lines.
    Removes headers, timestamps, and style tags.
    """
    lines = vtt_content.split('\n')
    cleaned_lines = []
    
    # Regex to detect timestamps (e.g., 00:00:01.000 --> 00:00:04.000)
    timestamp_pattern = re.compile(r'\d{2}:\d{2}:\d{2}\.\d{3}\s-->\s\d{2}:\d{2}:\d{2}\.\d{3}')
    
    seen_lines = set()

    for line in lines:
        line = line.strip()
        
        # specific filters to ignore non-content lines
        if (not line or 
            line == 'WEBVTT' or 
            line.startswith('NOTE') or
            timestamp_pattern.match(line) or
            '-->' in line):
            continue
            
        # Remove HTML-like tags often found in VTT (e.g., <c.colorE5E5E5>)
        text_only = re.sub(r'<[^>]+>', '', line)
        
        # Deduplicate consecutive identical lines (common in auto-generated subs)
        if text_only and text_only not in seen_lines:
            cleaned_lines.append(text_only)
            seen_lines.add(text_only)
            
    return cleaned_lines
