import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Directory paths
    INPUT_DIR = Path(os.getenv("INPUT_DIR", "input_videos"))
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output_text"))
    CACHE_DIR = Path(os.getenv("CACHE_DIR", "temp_files"))

    # FFmpeg paths - updated to match your exact structure
    FFMPEG_DIR = Path(__file__).parent.parent / "ffmpeg" / "ffmpeg-2025-04-21-git-9e1162bdf1-full_build" / "bin"
    FFMPEG_PATH = FFMPEG_DIR / "ffmpeg.exe"
    FFPROBE_PATH = FFMPEG_DIR / "ffprobe.exe"

    # Whisper model
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

    @classmethod
    def setup_dirs(cls):
        """Create required directories"""
        cls.INPUT_DIR.mkdir(exist_ok=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.CACHE_DIR.mkdir(exist_ok=True)

    @classmethod
    def verify_ffmpeg(cls):
        """Verify FFmpeg installation"""
        print(f"Checking FFmpeg at: {cls.FFMPEG_PATH}")  # Debug output
        print(f"Absolute path: {cls.FFMPEG_PATH.absolute()}")  # Debug output
        if not cls.FFMPEG_PATH.exists():
            available = list(cls.FFMPEG_DIR.glob('*')) if cls.FFMPEG_DIR.exists() else []
            print(f"Available files in directory: {available}")  # Debug output
            raise FileNotFoundError(f"FFmpeg not found at: {cls.FFMPEG_PATH}")
        if not cls.FFPROBE_PATH.exists():
            raise FileNotFoundError(f"FFprobe not found at: {cls.FFPROBE_PATH}")

settings = Settings()