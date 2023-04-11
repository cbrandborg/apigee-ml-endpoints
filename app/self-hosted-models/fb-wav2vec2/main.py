from utils import *
from fastapi import FastAPI, Request

app = FastAPI()

@app.post('/transcribe')
async def transcribeAudio(request: Request):
    
    envelope = await request.form()
    # verify_request(envelope)
    
    payload = Payload(envelope=envelope)
    response = await evaluate_text(payload=payload)

    return (response,200)

