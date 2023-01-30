async def has_text_youtube_link(text):
    if text:
        if 'youtube' in text:
            return True
        else:
            return False
    else:
        return False
