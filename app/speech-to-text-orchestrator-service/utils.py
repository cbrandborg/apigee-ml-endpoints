
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
import json, os
import time
import sys
import requests
import base64
from dataclasses import dataclass
import uuid
import wave


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
        file_path = f'output-{unique_id}.mp3'

        print(self.envelope['audio'])

        wav_bytes = base64.b64decode(self.envelope['audio'])

        with open(file_path, "wb") as f:
            f.write(wav_bytes)


def calc_dBFS(file_path):
    # Open the wave file
    with wave.open('example.wav', 'rb') as wav_file:
        # Get the number of frames in the wave file
        num_frames = wav_file.getnframes()
        # Read all the frames into an array
        frames = wav_file.readframes(num_frames)

    # Convert the frames to a numpy array
    samples = np.frombuffer(frames, dtype=np.int16)

    # Calculate the RMS (root mean square) of the samples
    rms = np.sqrt(np.mean(np.square(samples)))

    # Calculate the dBFS (decibels relative to full scale)
    dbfs = 20 * np.log10(rms / 32767)


"""
Helper function to clip audio at the given start and end timestamps and store at {output_file} path
"""
def clip_audio(audio, output_file, start, end):
    # Convert start and end timestamps from seconds to milliseconds
    start_ms = start * 1000
    end_ms = end * 1000
    
    # Get the audio in the specified range
    clipped = audio[start_ms:end_ms]
    
    # Hel
    # # Save the clipped audio to a new file
    start = time.time()
    print('started clipping')
    clipped.export(output_file, format=output_file.split(".")[-1])
    end = time.time()
    print('CLIPPING TIME:', end-start)
    return output_file

"""
This function chunks the original audio file into clips of {clip_length} seconds
This method uses a VAD to detect silences in the audio to optimize the clipping (i.e. to avoid clipping in the middle of a sentence)
Clips are stored in the output directory with the naming convention: clipped-{start}-{end}.mp3
"""
def chunk_audio(audio, clip_length, output_folder, language, model_id, min_clip_length = 90):
    
    if clip_length < min_clip_length:
        print('Clip length must be greater than min clip length!')
        sys.exit()

    # Determine the loudness of the audio file
    dBFS=audio.dBFS
   
    window_start = 0
    window_end = window_start + clip_length

    metadata = []

    # Use a sliding window to clip the audio
    while (window_end <= audio.duration_seconds):
        print('WINDOW START', window_start, 'WINDOW END', window_end)
        print('Started detecting silences')

        # PyDub documentation for this method can be found here: https://github.com/jiaaro/pydub/blob/master/pydub/silence.py
        silences = detect_silence(audio[window_start * 1000:window_end * 1000], min_silence_len=500, silence_thresh=dBFS-16)
        
        print('Finished detecting silences')

        # If there are no silences in the window, increase the window size for the clip and continue
        if len(silences) == 0:
            window_end += clip_length
            continue
        
        last_silence = silences[-1]

        start, stop = last_silence

        # Calculate the middle of the last silence in add silence padding
        middle = start + ((stop - start) / 2)
        
        clip_start = window_start
        clip_end = window_start + (middle/1000)

        # If the clip is too short, increase the window size for the clip and continue
        if (clip_end-clip_start < min_clip_length):
            window_end += clip_length
            continue

        chunk_path = clip_audio(audio, f"{output_folder}/clipped-{clip_start}-{clip_end}.mp3", clip_start, clip_end)
        metadata.append({
            "start": clip_start,
            "end": clip_end
        })

        send_to_pubsub(chunk_path, language, model_id)

                # Call pubsub function

        window_start = clip_end
        window_end = window_start + clip_length

    # Clip remaining audio
    clip_start = window_start
    clip_end = audio.duration_seconds
    chunk_path = clip_audio(audio, f"{output_folder}/clipped-{clip_start}-{clip_end}.mp3", clip_start, clip_end)
    metadata.append({
        "start": clip_start,
        "end": clip_end
    })
    send_to_pubsub(chunk_path, language, model_id)

    open ("metadata.json", "w").write(json.dumps(metadata))

def send_to_pubsub(chunk_path, language, model_id):
    
    url = "http://localhost:8080/whisper/audio"
    with open(chunk_path, "rb") as _file:

        data = _file.read()
    encoded_data = base64.b64encode(data)
    request_body = {"audio": f'{encoded_data}', "model_id": f'{model_id}', "language": f'{language}'}

    requests.post(url, json=request_body)


    