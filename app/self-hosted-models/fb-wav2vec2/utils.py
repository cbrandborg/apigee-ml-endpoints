import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from dataclasses import dataclass
from scipy.io import wavfile
import soundfile as sf


@dataclass
class Payload():
    envelope: object
    audio: str = None
    model_id: str = None
    language: dict = None

    def __post_init__(self):
        self.audio = self.envelope["file"].filename
        if 'language' in self.envelope:
            self.language = self.envelope['language']


@dataclass
class Transcription():
    text: list
    language: str
    segments: str = None
    segments_required: bool = False

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


async def evaluate_text(payload: object):

    # Load pretrained models
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    input_audio, sampling_rate = librosa.load(payload.audio, sr=16000)

    input_values = processor(
        input_audio, sampling_rate=sampling_rate, return_tensors="pt").input_values
    logits = model(input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    text = ' '.join(processor.batch_decode(predicted_ids))

    return text