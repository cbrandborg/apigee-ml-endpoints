from flask import Flask, request, jsonify
from google.cloud import pubsub_v1

app = Flask(__name__)

# Set up Pub/Sub client and topic
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("<PROJECT_ID>", "<TOPIC_NAME>")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Receive audio data from Apigee
    audio_data = request.get_data()

    # Publish audio data to Pub/Sub topic for transcription
    publisher.publish(topic_path, data=audio_data)

    # Return success message
    return jsonify({"message": "Audio data received and sent for transcription."}), 200


@app.route('/receive_transcription', methods=['POST'])
def receive_transcription():
    # Receive transcription from Pub/Sub
    transcription = request.get_json()

    # Process transcription
    # ...

    # Send response back to Apigee
    return jsonify({"transcription": transcription}), 200
