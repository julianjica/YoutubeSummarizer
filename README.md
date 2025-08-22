# YouTube Downloader & Summarizer

A simple yet powerful CLI tool to download YouTube videos, transcribe the audio, and generate a comprehensive summary using Google's Gemini AI. Perfect for quickly getting the essence of a video without watching it.

## Features

-   **Download YouTube Videos**: Automatically downloads the audio from any YouTube video as an MP3 file.
-   **Transcribe Audio**: Uses OpenAI's Whisper to generate a full transcript of the video.
-   **Summarize with Gemini**: Leverages the power of Google's Gemini AI to create a detailed and concise summary of the transcript.
-   **Interactive Q&A**: After the summary, you can ask questions about the video in an interactive chat session.
-   **Beautiful CLI**: Uses the `rich` library to provide a beautiful and user-friendly command-line interface.
-   **Lightweight and Efficient**: Designed to run on low-specification machines, even without a dedicated GPU.

## How it Works

The script works in three simple steps:

1.  **Download**: It uses `yt-dlp` to download the audio of the given YouTube video.
2.  **Transcribe**: The downloaded audio is then transcribed into text using the `whisper` model. The base model is used by default, which is lightweight and works well on CPUs.
3.  **Summarize & Chat**: The transcript is then passed to Google's Gemini AI to generate a summary. After the summary, you can ask questions about the video.

## Installation

This project uses `uv` for package management, which is a fast and modern Python package installer.

1.  **Install `uv`** (if you don't have it already):
    ```bash
    pip install uv
    ```

2.  **Create the virtual environment and install dependencies**:
    `uv` can create the virtual environment and install the dependencies from `pyproject.toml` in a single command.
    ```bash
    uv sync
    ```
    This will create a `.venv` directory (if it doesn't exist) and install all the necessary packages.

## Configuration

This script requires a Google Gemini API key.

1.  **Get your API key**: You can get your API key from the [Google AI Studio](https://aistudio.google.com/app/apikey).

2.  **Set the environment variable**: Open your `~/.bashrc` or `~/.zshrc` file and add the following line:
    ```bash
    export GEMINI_API_KEY='YOUR_API_KEY'
    ```
    Replace `YOUR_API_KEY` with your actual API key.

3.  **Apply the changes**: Source your shell configuration file to apply the changes:
    ```bash
    source ~/.bashrc
    # or
    source ~/.zshrc
    ```

## Usage

To run the script, simply execute the `main.py` file:
```bash
python main.py
```
The script will then guide you through the process, asking for the YouTube video URL and providing the summary and chat interface.

## License

This project is licensed under the MIT License.
