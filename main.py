import yt_dlp
import whisper
import torch,time
import os
import glob
def download_audio(url):
    ydl_opts = { #change this for different format
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_title = info['title']
        print(f"Downloading audio: {audio_title}")
        ydl.download([url])
    
    return f"{audio_title}.wav"

def transcribe_audio(audio_file):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = whisper.load_model("base")
    result = model.transcribe(audio_file, fp16=False)

    return result["text"]

def process_youtube_video(url):
    print("Starting download process...")
    for file in glob.glob("*.wav"): #remove any exiting audio in the dir
        os.remove(file)
    audio_file = download_audio(url)
    print(f"Audio downloaded as: {audio_file}")
    time.sleep(1)
    print("Starting transcription process...")

    current_dir = os.getcwd()
    audio_files = glob.glob(os.path.join(current_dir, "*.wav"))  
    if not audio_files:
        raise FileNotFoundError("No audio file found in the current directory.")
    
    full_audio_path = audio_files[0] 
    print(f"Found audio file: {full_audio_path}")
    transcript = transcribe_audio(full_audio_path)
    print("Transcription complete. Saving to file...")
    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)
    print("Transcript saved to transcript.txt")

    return transcript

url = "https://www.youtube.com/..." #your link
transcript = process_youtube_video(url)
