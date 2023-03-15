import os
from flask import Flask, request

from http_helper_functions import *
# from using_whisper import *

app = Flask(__name__)

@app.route("/whisper", methods=["POST"])
def postWhisper():
    
    # Parsing request as object
    envelope = request.get_json()

    verify_request(envelope)

    print(envelope)

    return (envelope)


@app.route("/whisper", methods=["GET"])
def getWhisper():
    
    print('welcome')

    return ('Welcome', 200)

@app.route("/google", methods=["POST"])
def postGoogle():
    
    # Parsing request as object
    envelope = request.get_json()

    verify_request(envelope)

    print(envelope)

    return (envelope)


# curl -X POST https://reqbin.com/echo/post/json 
#    -H "Content-Type: application/json"
#    -d '{"productId": 123456, "quantity": 100}'