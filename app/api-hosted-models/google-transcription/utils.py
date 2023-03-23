
from dataclasses import dataclass, field, asdict
@dataclass
class Transcription():
    text : str
    language : str
    confidence : float


