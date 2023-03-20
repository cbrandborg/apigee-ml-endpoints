import base64
import wave

with open("24syv.mp3", "rb") as f:
    audio_bytes = f.read()
    encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

print(encoded_audio)

with open('24syv.txt', 'w') as output:
# Read the WAV file contents
    output.write(encoded_audio)