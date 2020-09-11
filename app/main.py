# coding: utf-8
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin

from app.settings import *
from app.utils import *

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/', methods=['GET']) # To prevent Cors issues
def index():
    return render_template("index.html")

@app.route('/sms', methods=['GET']) # To prevent Cors issues
@cross_origin(supports_credentials=True)
def sendsms():
    (amount, 
    number) = request.args.get('amount'), request.args.get('number')

    if number is not None and amount is not None:
        proceed(number, amount, True)
        response = { 
            "status":"success", 
            "message": "Amount received successfully !",
            "number": number
        }, 200
    else:
        # Build the response
        response = { 
            "status":"error", 
            "message": "Please provide all required parameters."
        }, 401

    return response

@app.route('/get', methods=['GET']) # To prevent Cors issues
@cross_origin(supports_credentials=True)
def getNumber():
    # Sent in GET requests
    (number, 
    amount, 
    secret_key) = (request.args.get('number'), 
                    request.args.get('amount'), 
                    request.args.get('secret-key'))

    if number is not None and secret_key is not None and amount is not None:
        if gen_hash(secret_key) == gen_hash(SECRET_KEY):
            # Build the response
            # resp = send_money(number, amount)
            proceed(number, amount, False)
            response = { 
                "status":"success", 
                "message": "Request sent and waiting for validation",
                "number": number,
                "secret-key": gen_hash(secret_key)
            }, 200
        else:
            # Build the response
            response = { 
                "status":"error", 
                "message": "Your given secret-key is not valid."
            }, 401
    else:
        # Build the response
        response = { 
            "status":"error", 
            "message": "Please provide all required parameters."
        }, 401

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=1234)
