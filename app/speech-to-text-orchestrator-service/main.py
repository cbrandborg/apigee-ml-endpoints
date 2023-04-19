import base64
from fastapi import FastAPI, Request
from dataclasses import asdict
from utils import *
from pydub import AudioSegment


app = FastAPI()

@app.post("/audiosplit")
async def postWhisper(request: Request):
    
    # Parsing request as object
    envelope = await request.json()

    payload = Payload(envelope)

    audio = AudioSegment.from_file(payload.audio, "mp3")

    chunk_audio(audio=audio, clip_length=10, output_folder='test', language=payload.language, model_id=payload.model_id, min_clip_length=5)

    response = envelope
    
    return (response, 200)
