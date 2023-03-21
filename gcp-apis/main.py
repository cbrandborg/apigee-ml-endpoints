from google.cloud import speech
from helper_functions import *
from fastapi import FastAPI, Request
from google.cloud import storage

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
    
    return (printed_response,200)


def print_response(response: speech.RecognizeResponse):
    for result in response.results:
        print_result(result)

def print_result(result: speech.SpeechRecognitionResult):
    best_alternative = result.alternatives[0]
    print("-" * 80)
    print(f"language_code: {result.language_code}")
    print(f"transcript:    {best_alternative.transcript}")
    print(f"confidence:    {best_alternative.confidence:.0%}")


