
import base64
import wave
import uuid 
import requests
import os
import time
from dotenv import load_dotenv

from dataclasses import dataclass, field, asdict

load_dotenv()

# If empty, no data is received, respond with 400
def verify_request(envelope):
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    # If not in dict format or does not contain message key, respond with 400
    if not isinstance(envelope, dict):
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    return envelope

# Rewrite to query available languages: https://www.assemblyai.com/docs#supported-languages

# @dataclass
# class Model():
#     model_id : str
#     model_dimensions : dict = field(init=False)
#     languages : dict = field(init=False)

#     def __post_init__(self):
#         self.model_dimensions = { k:v for (k,v) in whisper.load_model(self.model_id).dims.__dict__.items()}
#         if ".en" in self.model_id:
#             self.languages =  {'en': 'english'}
#         else:
#             self.languages = LANGUAGES

@dataclass
class Payload():
    envelope : dict
    audio : str = None
    model_id : str = None
    language : dict = None

    def __post_init__(self):
        self.audio = self.read_incoming_b64_str()
        if 'language' in self.envelope:
            self.language = self.envelope['language']

    def read_incoming_b64_str(self):
        unique_id = str(uuid.uuid4())
        file_path = f'output-{unique_id}.wav'

        wav_bytes = base64.b64decode(self.envelope['audio'])

        with open(file_path, "wb") as f:
            f.write(wav_bytes)

        return file_path
        
@dataclass
class Transcription():
    text : str
    language : str
    segments : str = None
    segments_required : bool = False
    
    def __post_init__(self):
        if self.segments_required == False:
            self.segments = None



# Uploads a file to AAI servers
def upload_file(audio_file, header, upload_endpoint):

    upload_response = requests.post(
        upload_endpoint,
        headers=header, data=_read_file(audio_file)
    )
    return upload_response.json()

def _read_file(filename, chunk_size=5242880):
    with open(filename, "rb") as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


# Request transcript for file uploaded to AAI servers
def request_transcript(upload_url, header, transcript_endpoint, language):

    if language == None:

        transcript_request = {
            "audio_url": upload_url['upload_url'],
            "language_detection": True
        }
    
    else:
        transcript_request = {
            "audio_url": upload_url['upload_url'],
            "language_code": language
        }

    transcript_response = requests.post(
        transcript_endpoint,
        json=transcript_request,
        headers=header
    )
    return transcript_response.json()


# Make a polling endpoint
def make_polling_endpoint(transcript_response, polling_endpoint):

    polling_endpoint += '/'+(transcript_response['id'])
    return polling_endpoint


# Wait for the transcript to finish
def wait_and_retrive_transcription(polling_endpoint, header):
    while True:
        polling_response = requests.get(polling_endpoint, headers=header)
        polling_response = polling_response.json()

        if polling_response['status'] == 'completed':
            break

        time.sleep(5)

        if polling_response['status'] == 'error':
            print('error occured')
            return None
    
    transcription_response = requests.get(polling_endpoint, headers=header)
    response = transcription_response.json()

    text = response['text']
    language = response['language_code']
    segments = response['words']

    return text, language, segments


# # Get the paragraphs of the transcript
# def get_paragraphs(polling_endpoint, header):
#     paragraphs_response = requests.get(polling_endpoint, headers=header)
#     paragraphs_response = paragraphs_response.json()

#     paragraphs = []
#     for para in paragraphs_response['paragraphs']:
#         paragraphs.append(para)

#     return paragraphs


def assemblyai_transcribe(payload: object, upload_endpoint, transcript_endpoint):

    TOKEN = os.environ.get('API_TOKEN')
    header = {
        'authorization': f'{TOKEN}',
        'content-type': 'application/json'
    }

    upload_url = upload_file(payload.audio, header, upload_endpoint)

    transcript_response = request_transcript(upload_url, header, transcript_endpoint, payload.language)

    polling_endpoint = make_polling_endpoint(transcript_response, transcript_endpoint)

    text, language, segments = wait_and_retrive_transcription(polling_endpoint, header)

    return text, language, segments