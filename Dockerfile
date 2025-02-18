FROM python:3.13
EXPOSE 8080
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]

ENV AWS_REGION=""
ENV AWS_Q1=""
ENV AWS_Q2=""
ENV AWS_Q3=""
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""