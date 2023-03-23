import os
import base64
from fastapi import FastAPI, Request
from dataclasses import asdict
from utils import *

app = FastAPI()

@app.post("/assemblyai/audio")
async def postWhisper(request: Request, segments_required: bool = False):
    
    # Parsing request as object
    envelope = await request.json()

    verify_request(envelope)

    payload = Payload(envelope)

    upload_endpoint = "https://api.assemblyai.com/v2/upload"
    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

    transcription_values = assemblyai_transcribe(payload, upload_endpoint, transcript_endpoint)

    transcription = Transcription(*transcription_values, segments_required)

    response = asdict(transcription)

    return (response, 200)

# curl -X POST https://reqbin.com/echo/post/json 
#    -H "Content-Type: application/json"
#    -d '{"productId": 123456, "quantity": 100}'