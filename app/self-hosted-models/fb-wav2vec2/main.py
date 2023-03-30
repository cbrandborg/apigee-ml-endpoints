from utils import *
from fastapi import FastAPI, Request
from dataclasses import asdict
from scipy.io import wavfile
import soundfile as sf

app = FastAPI()

@app.post('/transcribe')
async def transcribeAudio(request: Request):
    
    envelope = await request.form()
    # verify_request(envelope)
    
    payload = Payload(envelope=envelope)
    response = await evaluate_text(payload=payload)

    return (response,200)

