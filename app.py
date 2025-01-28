import os
import dotenv
from flask import Flask, render_template, request
import boto3

AWS_REGION = os.getenv("AWS_REGION")
AWS_QUEUES = [os.getenv("AWS_Q1"), os.getenv("AWS_Q2"), os.getenv("AWS_Q3")]

sqs = boto3.client('sqs', region_name=AWS_REGION)

def create_app():
    app = Flask(__name__)
    @app.route("/")
    def home():
        print(f"{AWS_REGION} {AWS_QUEUES[0]}")
        return render_template('index.html')

    @app.post("/")
    def send_data_to_SQS():
        data = request.json
        #
        # if data.title == None or data.desc == None or data.prio == None:
        #     return "Invalid message", 400

        response = create_Response(data)
        # print(response)
        return response, 200


    return app

def create_Response(data):
    # if data.prio < 0 or data.prio > 3:
    #     return "Invalid priority"
    print(AWS_QUEUES[0])
    message_body = {
        'Title': {
            'DataType': 'String',
            'StringValue': 'Test Title'
        },
        'Desc': {
            'DataType': 'String',
            'StringValue': 'Test Desc'
        },
        'Prio': {
            'DataType': 'Number',
            'StringValue': '0'
        }
    }
    return sqs.send_message(
        QueueUrl=AWS_QUEUES[0],
        MessageBody=(
            str(message_body)
        )
    )

if __name__ == '__main__':
    app = create_app()
    app.run()
