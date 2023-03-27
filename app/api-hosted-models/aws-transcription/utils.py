import os
import time
import json
import boto3
import botocore
from dataclasses import dataclass


@dataclass
class Payload():
    envelope: dict
    job_name: str = None
    audio: str = None
    language: str = None

    def __post_init__(self):
        self.audio = self.envelope['audio']
        self.job_name = self.envelope['job_name']
        if 'language' in self.envelope:
            self.language = self.envelope['language']


@dataclass
class Transcription():
    text: botocore.response.StreamingBody
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


def transcribe_audio(payload: object):
    json_credentials = json.loads(os.environ.get('CREDS'))

    client = boto3.client('transcribe',
                          aws_access_key_id=json_credentials['Access_key_ID'],
                          aws_secret_access_key=json_credentials['Secret_access_key'],
                          region_name="eu-west-1")

    transcribe_config = {
        'TranscriptionJobName': str(payload.job_name),
        'Media': {'MediaFileUri': "{0}".format(payload.audio)},
        'LanguageCode': str(payload.language),
        'OutputBucketName': "jk-bucket-aws-transcribe"
    }

    response = client.start_transcription_job(**transcribe_config)

    transcribed_response = getTranscribedAudio(response,json_credentials)

    return transcribed_response, payload.language


def getTranscribedAudio(transcription_job, json_credentials):
    aws_client = boto3.client('transcribe',
                              aws_access_key_id=json_credentials['Access_key_ID'],
                              aws_secret_access_key=json_credentials['Secret_access_key'],
                              region_name="eu-west-1")

    while transcription_job['TranscriptionJob']['TranscriptionJobStatus'] != "COMPLETED":
        print("Checking whether the Transcription Job has completed...")
        if transcription_job['TranscriptionJob']['TranscriptionJobStatus'] == "FAILED":
            print("Transcription job has failed")
            return transcription_job['FailureReason']
        elif transcription_job['TranscriptionJob']['TranscriptionJobStatus'] == "COMPLETED":
            print("Transcription Job completed! Retrieving transcription")
            s3_client = boto3.client('s3')
            transcribe_response = s3_client.get_object(
                Bucket='jk-bucket-aws-transcribe',
                Key='{0}'.format(transcription_job['TranscriptionJob']['TranscriptionJobName'])+'.json'
                )
            response = json.load(transcribe_response['Body'])
            return response['results']['transcripts'][0]
        time.sleep(10)
        transcription_job = aws_client.get_transcription_job(
            TranscriptionJobName=transcription_job['TranscriptionJob']['TranscriptionJobName'])
