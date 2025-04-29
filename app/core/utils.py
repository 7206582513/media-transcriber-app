import subprocess
import shutil
from pathlib import Path
from termcolor import colored
import logging
from app.config import settings

logger = logging.getLogger(__name__)

def check_dependencies():
    """Verify required system dependencies"""
    settings.verify_ffmpeg()
    required = ['ffmpeg', 'ffprobe']
    for dep in required:
        if not shutil.which(dep):
            raise RuntimeError(colored(f"{dep} not found in system PATH", "red"))

def convert_to_mp3(input_path: Path, output_path: Path):
    """Convert any audio/video file to MP3 using ffmpeg"""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    command = [
        str(settings.FFMPEG_PATH),
        '-i', str(input_path),
        '-vn',
        '-acodec', 'libmp3lame',
        '-q:a', '2',
        '-y',
        str(output_path)
    ]

    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        logger.debug("FFmpeg output: %s", result.stderr)
    except subprocess.CalledProcessError as e:
        logger.error("FFmpeg command failed: %s", e.stderr)
        raise RuntimeError(f"Audio conversion failed: {e.stderr}")

def clean_temp_files():
    """Clean temporary files directory"""
    for file in settings.CACHE_DIR.glob('*'):
        try:
            file.unlink()
        except Exception as e:
            logger.warning(f"Error deleting {file}: {str(e)}")

# Add this new function for WAV conversion
def convert_to_wav(input_path: Path, output_path: Path):
    """Convert any audio/video file to WAV using ffmpeg"""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    command = [
        str(settings.FFMPEG_PATH),
        '-i', str(input_path),
        '-acodec', 'pcm_s16le',
        '-ac', '1',
        '-ar', '16000',
        '-y',
        str(output_path)
    ]

    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg conversion failed: {e.stderr}")
        raise RuntimeError(f"Audio conversion failed: {e.stderr}")