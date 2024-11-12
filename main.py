######
# install this library the after run  
pip install yt-dlp ffmpeg-python pydub tqdm
pip install ffmpeg-python

#################################################
# locally run on vs code 
import ffmpeg
import io
from yt_dlp import YoutubeDL, DownloadError
from pydub import AudioSegment
from tqdm import tqdm
from pydub.playback import play
def youtube_to_audio_stream(youtube_url):
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        'age_limit': 18,  
    }   
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            audio_url = info['url']  
    except DownloadError as e:
        print(f"Error: {e}")
        return None
    process = (
        ffmpeg
        .input(audio_url)
        .output('pipe:', format='mp3')
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )
    audio_buffer = io.BytesIO()
    total_size = 0  
    chunk_size = 1024  
    with tqdm(total=100, desc="Processing Audio", unit="%", dynamic_ncols=True) as pbar:
        while True:
            in_bytes = process.stdout.read(chunk_size)
            if not in_bytes:
                break
            audio_buffer.write(in_bytes)
            total_size += len(in_bytes)
            pbar.update(len(in_bytes) / total_size * 100 if total_size > 0 else 0)
    audio_buffer.seek(0)
    try:
        audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
        return audio_segment
    except Exception as e:
        print(f"Error processing audio chunk: {e}")
        return None
youtube_url = "Enter your youtube video url"
audio_segment = youtube_to_audio_stream(youtube_url)
if audio_segment:
    print("Audio segment loaded successfully")
    # #if you save this video then after check   
    # audio_segment.export("output_audio.wav", format="wav")
    # print("Audio saved to output_audio.wav")
    #Optionally play the audio
    play(audio_segment)
else:
    print("Failed to load audio segment")

