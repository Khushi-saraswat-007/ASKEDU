import subprocess
import os
import whisper

def extract_transcript_from_video(video_path):
    try:
        # Output audio path
        audio_path = video_path.replace(".mp4", ".mp3")

        # Use ffmpeg to extract audio
        command = ['ffmpeg', '-y', '-i', video_path, '-q:a', '0', '-map', 'a', audio_path]
        subprocess.run(command, check=True)

        # Transcribe using whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)

        # Cleanup
        os.remove(audio_path)

        return result["text"]

    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        return None
