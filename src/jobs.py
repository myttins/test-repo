import requests
from rq import Queue
from redis import Redis
import os


def health_check():
    response = requests.get(os.getenv("APP_URL") + "/api/health")
    if response.status_code != 200:
        requests.post(os.getenv("SLACK_WEBHOOK_URL"), json={'text': "health check to NBA predictor has failed!"})

# setup queue
conn = Redis.from_url(os.getenv("REDIS_URL"))
q = Queue(connection=conn)
q.enqueue(health_check)
