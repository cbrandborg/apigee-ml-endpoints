import os
import whisper
import base64
from flask import Flask, request
from dataclasses import asdict


from helper_functions import *

app = Flask(__name__)

@app.route("/whisper/audio", methods=["POST"])
def postWhisper():
    
    segments_required = request.args.get('getSegments', False)

    # Parsing request as object
    envelope = request.get_json()

    verify_request(envelope)

    payload = Payload(envelope)

    transcription_values = whisper_transcribe(payload)

    transcription = Transcription(*transcription_values, segments_required)

    response = asdict(transcription)
    
    return (response, 200)


@app.route("/whisper/models", methods=["GET"])
def getModels():
    
    available_models = whisper.available_models()

    return (available_models, 200)

@app.route("/whisper/models/<model_id>", methods=["GET"])
def getModelById(model_id):
    
    model = Model(model_id)

    response = asdict(model)

    return (response, 200)


# curl -X POST https://reqbin.com/echo/post/json 
#    -H "Content-Type: application/json"
#    -d '{"productId": 123456, "quantity": 100}'