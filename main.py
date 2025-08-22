from google import genai
import os
from yt_dlp import YoutubeDL
import whisper

# Configuring the API (set as ENV variable)
def mp3_downloader():
    """
    This function asks for the url of the Youtube video and then downloads the
    mp3 file associated with that video.
    """
    print("="*50)
    print("STEP 1: Downloading Audio from YouTube")
    print("="*50)

    # We make the output directory if it does not already exist
    os.makedirs("output", exist_ok=True)

    # And then download the audio
    url = input("Please enter the YouTube video URL: ")
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
        print("\nDownloading...")
        ydl.download([url])
    print("\nDownload complete!")

def transcribe_video(size = "base"):
    """
    This function takes the output/output.mp3 and uses a whisper-ai model (by
    default base) to get the transcribe of the recently downloaded video.

    :size: (string) name of the model
    :returns: (string) transcription of the video
    """
    print("\n" + "="*50)
    print("STEP 2: Transcribing Audio to Text")
    print("="*50)
    print(f"Using whisper model: '{size}'")
    print("Transcribing... This may take a moment.")
    model = whisper.load_model(size)
    result = model.transcribe("output/output.mp3", verbose = True)
    print("Transcription complete!")
    return result["text"]

def gemini_chat(transcript):
    """
    This function takes the video's transcript and starts a conversation with
    the user about the video by first providing a summary of it, and then it
    receives and answer questions the user may have about the video.

    :transcript: (string) transcript of the video
    """
    print("\n" + "="*50)
    print("STEP 3: Summarizing and Chatting")
    print("="*50)

    # Setting Client with GEMINI_API_KEY
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    # Prompt adapted from
    # https://www.reddit.com/r/ChatGPTPro/comments/13n55w7/highly_efficient_prompt_for_summarizing_gpt4/
    first_prompt = """ As a professional summarizer, create a concise and
    comprehensive summary of the provided text from a video transcript, while
    adhering to these guidelines:

    Craft a summary that is detailed, thorough, in-depth, and complex, while
    maintaining clarity and conciseness.

    Incorporate main ideas and essential information, eliminating extraneous
    language and focusing on critical aspects.

    Rely strictly on the provided text, without including external information.

    Format the summary in paragraph form for easy understanding.

    Say nothing else besides the summary. Below is the transcript\n"""

    # We create the chat environment
    chat = client.chats.create(model="gemini-2.0-flash-001")
    # and send the transcript to be summarized
    print("\nGenerating summary...")
    summary = chat.send_message(first_prompt + transcript).text
    print("\n--- VIDEO SUMMARY ---")
    print(summary)
    print("--- END OF SUMMARY ---")

    # Questions loop
    print("\nYou can now ask questions about the video.")
    user_input = ""
    while user_input != "/quit":
        user_input = input("\nYour question (/quit to exit) > ")
        if user_input != "/quit":
            print("\n...Thinking...")
            print(chat.send_message(user_input).text)

if __name__ == "__main__":
    try:
        mp3_downloader()
        transcript = transcribe_video()
        gemini_chat(transcript)
        print("\n" + "="*50)
        print("Session finished. Thank you for using the YouTube Summarizer!")
        print("="*50)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
