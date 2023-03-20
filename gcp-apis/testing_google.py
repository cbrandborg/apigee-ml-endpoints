from google.cloud import speech

client = speech.SpeechClient()

ops = client.list_operations()

