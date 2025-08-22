from google import genai
import os
from yt_dlp import YoutubeDL

# Configuring the API (set as ENV variable)
def mp3_downloader():
    """
    This function asks for the url of the Youtube video and then downloads the
    mp3 file associated with that video.
    """
    # We make the output directory if it does not already exist
    os.makedirs("output", exist_ok=True)

    # And then download the audio
    url = input("Please type the url of the video > ")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'output/output',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
if __name__ == "__main__":
    mp3_downloader()
