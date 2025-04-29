from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.config import settings
from app.routes import api
from termcolor import colored
from app.core.utils import check_dependencies
import subprocess
import socket
from contextlib import closing


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Setup directories
        settings.setup_dirs()

        # Verify FFmpeg
        try:
            subprocess.run(
                [str(settings.FFMPEG_PATH), '-version'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(colored("✓ FFmpeg verified and working", "green"))
        except Exception as e:
            print(colored(f"✗ FFmpeg verification failed: {str(e)}", "red"))
            raise

        # Check other dependencies
        check_dependencies()
        print(colored("✓ System ready", "green"))
        yield

    except Exception as e:
        print(colored(f"Startup error: {str(e)}", "red"))
        raise
def is_port_in_use(port: int) -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        return s.connect_ex(('localhost', port)) == 0


app = FastAPI(lifespan=lifespan)
app.include_router(api.router)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    if is_port_in_use(8000):
        print("Port 8000 is already in use!")
    else:
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)