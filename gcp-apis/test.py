from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.cloud import storage

app = FastAPI()

@app.post("/transcribe")
async def transcribe(request: Request):
    data = await request.json()
    uri = data.get("uri")
    if not uri:
        raise HTTPException(status_code=400, detail="URI not found in request body")

    # Instantiate a GCS client
    storage_client = storage.Client()

    # Get the GCS bucket and object names from the GCS URI
    _, _, bucket_name, object_name = uri.split("/", 3)

    # Get the GCS object
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    # Download the audio file from GCS to local file system
    filename = "/tmp/audio.wav"
    blob.download_to_filename(filename)

    # Perform speech recognition using the Google Cloud Speech-to-Text client library
    client = speech_v1.SpeechClient()
    language_code = "en-US"
    config = {
        "language_code": language_code,
        "audio_channel_count": 2,
        "enable_separate_recognition_per_channel": True,
        "model": "default",
    }
    with open(filename, "rb") as f:
        content = f.read()
    audio = {"content": content}
    response = client.recognize(config, audio)

    # Return the transcribed text
    transcribed_text = ""
    for result in response.results:
        transcribed_text += result.alternatives[0].transcript
    return {"transcribed_text": transcribed_text}