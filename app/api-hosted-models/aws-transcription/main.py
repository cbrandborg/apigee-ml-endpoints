import boto3
from fastapi import FastAPI, Request
from dataclasses import asdict
from utils import *

app = FastAPI()


@app.post("/transcribe")
async def transcribeAudio(request: Request, segments_required: bool = False):
    envelope = await request.json()
    verify_request(envelope)

    payload = Payload(envelope=envelope)

    transcription_job = transcribe_audio(payload=payload)
    # transcription = Transcription(transcription_job,segments_required)
    # response = asdict(transcription)

    return (transcription_job, 200)


@app.get("/models")
async def getAllLanguageModels():

    client = boto3.client('transcribe')
    response = client.list_language_models()

    return response['Models']


@app.get("/objects/{object_id}")
async def getObject(object_id: str):
    credentials = json.loads(os.environ.get('CREDS'))
    s3_client = boto3.client(
        's3',
        aws_access_key_id=credentials['Access_key_ID'],
        aws_secret_access_key=credentials['Secret_access_key'],
        region_name="eu-west-1")
    
    transcribe_response = s3_client.get_object(
        Bucket='jk-bucket-aws-transcribe',
        Key=str(object_id)
    )
    return json.load(transcribe_response['Body'])['results']['transcripts'][0]
