import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import boto3

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_QUEUES = [os.getenv("AWS_Q1"), os.getenv("AWS_Q2"), os.getenv("AWS_Q3")]

sqs = boto3.client('sqs', region_name=AWS_REGION)

def create_app():
    app = Flask(__name__)
    @app.route("/")
    def home():
        # print(f"{AWS_REGION} {AWS_QUEUES[0]}")
        return render_template('index.html')

    @app.post("/")
    def send_data_to_SQS():
        data = request.json

        print(data.get("title"), type(data.get("title")))

        if data.get("title") is None or data.get("desc") is None or data.get("prio") is None:
            return "Invalid message", 400

        if int(data.get("prio")) < 0 or int(data.get("prio")) > 2:
            return "Invalid priority", 400

        response = create_Response(data)
        # print(response)
        return response, 200

    return app

def create_Response(data):
    priority = data.get("prio")
    print(AWS_QUEUES[priority])
    message_body =\
        {
            'title': f"{data.get("title")}",
            'desc': f"{data.get("desc")}",
            'prio': int(data.get("prio")),
        }
    return sqs.send_message(
        QueueUrl=AWS_QUEUES[priority],
        MessageBody=(
            str(message_body)
        )
    )

if __name__ == '__main__':
    app = create_app()
    app.run()
