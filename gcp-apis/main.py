from google.cloud import speech
from helper_functions import *
from fastapi import FastAPI, Request
from dataclasses import asdict
from helper_functions import *

app = FastAPI()


@app.post("/transcribe")
async def transcribeAudio(request: Request):
    
    envelope = await request.json()

    client = speech.SpeechAsyncClient()
    audio_file = speech.RecognitionAudio(uri="{0}".format(envelope['audio']))
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        # in Format "en-US"
        language_code="{0}".format(envelope['language']),
        enable_automatic_punctuation=True
    )
    
    print(f"Audio: {audio_file}")
    print(f"Language: {envelope['language']}")

    response = await client.recognize(config=config,audio=audio_file)
    printed_response = print_response(response=response)
    
    return (asdict(printed_response),200)


def print_response(response: speech.RecognizeResponse):
    return print_result(response.results[0])


def print_result(result: speech.SpeechRecognitionResult):
    best_alternative = result.alternatives[0]
    language = result.language_code
    text = best_alternative.transcript
    confidence = best_alternative.confidence
    transcription = Transcription(text=text,confidence=confidence,language=language )
    
    return transcription


