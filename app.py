import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import boto3

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_QUEUES = [os.getenv("AWS_Q1"), os.getenv("AWS_Q2"), os.getenv("AWS_Q3")]
sqs = boto3.client('sqs', region_name=AWS_REGION)

PORT = os.getenv("PORT") if os.getenv("PORT") is not None else 5000

def create_app():
    app = Flask(__name__)
    @app.route("/")
    def home():
        return render_template('index.html', PORT=PORT), 200

    # http://localhost:5000/health
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status":"Healthy"}), 200

    @app.post("/")
    def send_data_to_SQS():
        try:
            data = request.json
        except Exception as e:
            return "Invalid data format",400, e

        # print(data.get("title"), type(data.get("title")))

        if data.get("title") is None or data.get("desc") is None or data.get("prio") is None:
            return "Invalid message", 400

        if data.get("title") == "" or data.get("desc") == "" or data.get("prio") == "":
            return "Invalid message", 400

        if int(data.get("prio")) < 0 or int(data.get("prio")) > 2:
            return "Invalid priority", 400

        response = create_response(data)
        return response, 200

    return app

def create_response(data):
    priority = int(data.get("prio"))
    # print(AWS_QUEUES[priority])
    message_body = {
            'title': f"{data.get('title')}",
            'desc': f"{data.get('desc')}",
            'prio': priority,
        }
    return sqs.send_message(
        QueueUrl=AWS_QUEUES[priority],
        MessageBody=(
            str(message_body)
        )
    )

#Docker: docker run --env-file ./.env -p 8080:8080 front-end-flask-app
if __name__ == '__main__':
    app = create_app()
    app.run()
else:
    app = create_app()
