import os
import whisper
import base64
from fastapi import FastAPI, Request
from dataclasses import asdict
from utils import *

app = FastAPI()

@app.post("/audio")
async def postWhisper(request: Request, segments_required: bool = False):
    
    # Parsing request as object
    envelope = await request.json()

    verify_request(envelope)

    payload = Payload(envelope)

    transcription_values = whisper_transcribe(payload)

    transcription = Transcription(*transcription_values, segments_required)

    response = asdict(transcription)

    print(response['text'])

    return (response, 200)

@app.get("/models")
async def getModels() -> tuple:
    
    available_models = whisper.available_models()

    return (available_models, 200)


@app.get("/models/{model_id}")
async def getModelById(model_id: str) -> tuple:
    
    model = Model(model_id)

    response = asdict(model)

    return (response, 200)


# app = Flask(__name__)

# @app.route("/whisper/audio", methods=["POST"])
# def postWhisper():
    
#     segments_required = request.args.get('getSegments', False)

#     # Parsing request as object
#     envelope = request.get_json()

#     verify_request(envelope)

#     payload = Payload(envelope)

#     transcription_values = whisper_transcribe(payload)

#     transcription = Transcription(*transcription_values, segments_required)

#     response = asdict(transcription)
    
#     return (response, 200)


# @app.route("/whisper/models", methods=["GET"])
# def getModels():
    
#     available_models = whisper.available_models()

#     return (available_models, 200)

# @app.route("/whisper/models/<model_id>", methods=["GET"])
# def getModelById(model_id: str) -> tuple:
    
#     model = Model(model_id)

#     response = asdict(model)

#     return (response, 200)


# curl -X POST https://reqbin.com/echo/post/json 
#    -H "Content-Type: application/json"
#    -d '{"productId": 123456, "quantity": 100}'