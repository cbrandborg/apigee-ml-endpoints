import base64
import wave
import uuid
from google.cloud import speech
from dataclasses import dataclass, field, asdict


@dataclass
class Payload():
    envelope : dict
    audio : str = None
    model_id : str = None
    language : dict = None

    def __post_init__(self):
        self.audio = self.envelope['audio']
        if 'language' in self.envelope:
            self.language = self.envelope['language']
        
@dataclass
class Transcription():
    text : str
    language : str
    segments : str = None
    segments_required : bool = False
    
    def __post_init__(self):
        if self.segments_required == False:
            self.segments = None


# If empty, no data is received, respond with 400
def verify_request(envelope):
    if not envelope:
        msg = "No Payload received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    # If not in dict format or does not contain message key, respond with 400
    if not isinstance(envelope, dict):
        msg = "Invalid payload format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    return envelope

async def google_transcribe(payload: object):

    client = speech.SpeechAsyncClient()
    audio_file = speech.RecognitionAudio(content="{0}".format(payload.audio))
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        # in Format "en-US"
        language_code="{0}".format(payload.language),
        enable_automatic_punctuation=True
    )

    response = await client.recognize(config=config,audio=audio_file)

    print(response.results)
    text, language, segments = print_result(response.results[0])


    return text, language, segments

def print_result(result: speech.SpeechRecognitionResult):
    best_alternative = result.alternatives[0]
    language = result.language_code
    text = best_alternative.transcript
    words = best_alternative.words
    # Implement confidence later: confidence = best_alternative.confidence
    
    return text, language, words