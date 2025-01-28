import os
import dotenv
from flask import Flask, render_template
import boto3

AWS_REGION = os.getenv("AWS_REGION")
AWS_QUEUES = [os.getenv("AWS_Q1"), os.getenv("AWS_Q2"), os.getenv("AWS_Q3")]

def create_app():
    app = Flask(__name__)
    @app.route("/")
    def home():
        print(f"{AWS_REGION} {AWS_QUEUES[0]}")
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
