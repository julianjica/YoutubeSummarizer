from google import genai
import os
from yt_dlp import YoutubeDL
import whisper
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Initialize Rich Console
console = Console()

def mp3_downloader():
    """
    This function asks for the url of the Youtube video and then downloads the
    mp3 file associated with that video.
    """
    console.print(Panel("[bold cyan]STEP 1: Downloading Audio from YouTube[/bold cyan]", expand=False))

    # We make the output directory if it does not already exist
    os.makedirs("output", exist_ok=True)

    # And then download the audio
    url = Prompt.ask("[green]Please enter the YouTube video URL[/green]")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'output/output',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True, # To keep the output clean
        'no_warnings': True,
    }
    with console.status("[bold green]Downloading...[/bold green]") as status:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    console.print("[bold green]✔ Download complete![/bold green]")

def transcribe_video(size="base"):
    """
    This function takes the output/output.mp3 and uses a whisper-ai model (by
    default base) to get the transcribe of the recently downloaded video.

    :size: (string) name of the model
    :returns: (string) transcription of the video
    """
    console.print(Panel(f"[bold cyan]STEP 2: Transcribing Audio to Text (using whisper model: '{size}')[/bold cyan]", expand=False))
    
    model = whisper.load_model(size)
    result = model.transcribe("output/output.mp3", verbose = False)
    
    console.print("[bold green]✔ Transcription complete![/bold green]")
    return result["text"]

def gemini_chat(transcript):
    """
    This function takes the video's transcript and starts a conversation with
    the user about the video by first providing a summary of it, and then it
    receives and answer questions the user may have about the video.

    :transcript: (string) transcript of the video
    """
    console.print(Panel("[bold cyan]STEP 3: Summarizing and Chatting[/bold cyan]", expand=False))

    # Setting Client with GEMINI_API_KEY
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    # Prompt adapted from
    # https://www.reddit.com/r/ChatGPTPro/comments/13n55w7/highly_efficient_prompt_for_summarizing_gpt4/
    first_prompt = """As a professional summarizer, create a concise and
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
    
    with console.status("[bold green]Generating summary...[/bold green]"):
        summary = chat.send_message(first_prompt + transcript).text
    
    console.print(Panel(summary, title="[bold yellow]Video Summary[/bold yellow]", border_style="yellow"))

    # Questions loop
    console.print("\n[bold magenta]You can now ask questions about the video.[/bold magenta]")
    while True:
        user_input = Prompt.ask("[bold green]Your question ([/bold green]/quit to exit[bold green])[/bold green]")
        if user_input.lower() == "/quit":
            break
        with console.status("[bold green]...Thinking...[/bold green]"):
            response = chat.send_message(user_input).text
            console.print(f"[bold cyan]Gemini:[/bold cyan] {response}")

if __name__ == "__main__":
    try:
        mp3_downloader()
        transcript = transcribe_video()
        gemini_chat(transcript)
        console.print(Panel("[bold green]Session finished.[/bold green]", expand=False))
    except Exception:
        console.print_exception(show_locals=True)
