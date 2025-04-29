from fastapi import APIRouter, WebSocket, WebSocketDisconnect, UploadFile, File
from pathlib import Path
import json
import shutil
from termcolor import colored
from app.config import settings
from app.core.processor import YouTubeProcessor, FileProcessor

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Save uploaded file to input_videos folder"""
    file_location = settings.INPUT_DIR / file.filename
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "uploaded", "filename": file.filename}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    processor = YouTubeProcessor()
    file_processor = FileProcessor()

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            if payload['type'] == 'youtube':
                try:
                    transcript = processor.process_youtube(payload['url'])
                    await websocket.send_json({
                        'type': 'result',
                        'text': transcript
                    })
                except Exception as e:
                    await websocket.send_json({
                        'type': 'error',
                        'message': f"YouTube processing failed: {str(e)}"
                    })

            elif payload['type'] == 'file':
                try:
                    file_path = settings.INPUT_DIR / payload['filename']
                    transcript = file_processor.process_file(file_path)
                    await websocket.send_json({
                        'type': 'result',
                        'text': transcript
                    })
                except Exception as e:
                    await websocket.send_json({
                        'type': 'error',
                        'message': f"File processing failed: {str(e)}"
                    })

    except WebSocketDisconnect:
        print(colored("Client disconnected", "yellow"))
    except Exception as e:
        await websocket.send_json({
            'type': 'error',
            'message': f"Server error: {str(e)}"
        })
