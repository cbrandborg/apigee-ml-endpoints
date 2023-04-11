from google.cloud import speech
from utils import *
from fastapi import FastAPI, Request
from dataclasses import asdict

app = FastAPI()


@app.post("/transcribe")
async def transcribeAudio(request: Request, segments_required: bool = False):
    
    envelope = await request.json()

    verify_request(envelope)

    payload = Payload(envelope)

    transcription_values = await google_transcribe(payload)

    transcription = Transcription(*transcription_values, segments_required)

    return (asdict(transcription),200)

