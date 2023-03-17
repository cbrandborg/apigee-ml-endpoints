import whisper
import base64
import wave
import uuid 
from whisper.tokenizer import LANGUAGES
from dataclasses import dataclass, field, asdict

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

@dataclass
class Model():
    model_id : str
    model_dimensions : dict = field(init=False)
    languages : dict = field(init=False)

    def __post_init__(self):
        self.model_dimensions = { k:v for (k,v) in whisper.load_model(self.model_id).dims.__dict__.items()}
        if ".en" in self.model_id:
            self.languages =  {'en': 'english'}
        else:
            self.languages = LANGUAGES

@dataclass
class Payload():
    envelope : dict
    audio : str = None
    model_id : str = None
    language : dict = None

    def __post_init__(self):
        self.audio = self.read_incoming_b64_str()
        self.model_id = self.envelope['model_id']
        if 'language' in self.envelope:
            self.language = self.envelope['language']

    def read_incoming_b64_str(self):
        unique_id = str(uuid.uuid4())
        file_path = f'output-{unique_id}.wav'

        print(self.envelope['audio'])

        # wav_bytes = base64.b64decode(self.envelope['audio'])

        # with open(file_path, "wb") as f:
        #     f.write(wav_bytes)

        # with open('output.txt', 'rb') as wav_file:
        # # Read the WAV file contents
        #     wav_bytes = wav_file.read()

        # # Decode the Base64-encoded string to bytes
        # #wav_bytes = base64.b64decode(self.envelope['audio'])
        # wav_bytes = base64.b64decode(wav_bytes)
        # unique_id = str(uuid.uuid4())
        # file_path = f'output-{unique_id}.wav'
            
        # # Open a new WAV file for writing
        # with wave.open(file_path, 'wb') as wav_file:
        #     # Set the WAV file parameters
        #     wav_file.setnchannels(1)  # Mono
        #     wav_file.setsampwidth(2)  # 16-bit
        #     wav_file.setframerate(44100)  # 44.1 kHz

        #     # Write the WAV file contents
        #     wav_file.writeframes(wav_bytes)
        
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


def whisper_transcribe(payload: object):

    model = whisper.load_model(payload.model_id)

    print(payload)

    # If a language is not provided, Whisper will attempt to infer it from the audio
    if payload.language is None:
        
        result = model.transcribe(payload.audio)
        text = result["text"]
        segments = result["segments"]
        language = result["language"]

    # Else Whisper will use the provided language
    else:

        result = model.transcribe(payload.audio, language=payload.language)
        text = result["text"]
        segments = result["segments"]
        language = payload.language
    
    return text, language, segments



# def whisper_transcribe(audio_data, model_id, known_language=None):

#     model = whisper.load_model(model_id)

#     # load audio and pad/trim it to fit 30 seconds
#     audio = whisper.load_audio(audio_data)

#     # make log-Mel spectrogram and move to the same device as the model
#     mel = whisper.log_mel_spectrogram(audio).to(model.device)

#     if known_language is None:

#         # detect the spoken language
#         _, probs = model.detect_language(mel)
#         print(f"Detected language: {max(probs, key=probs.get)}")

#         # decode the audio
#         options = whisper.DecodingOptions(fp16 = False)
#         result = whisper.decode(model, mel, options)

#     else:

#         # decode the audio
#         options = whisper.DecodingOptions(fp16 = False, language=known_language)
#         result = whisper.decode(model, mel, options)

#     transcription = result.text

#     return transcription