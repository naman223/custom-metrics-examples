import prometheus_client as prom
import random
import time
from threading import Thread

from flask import Flask, request
from flask_prometheus import monitor

req_summary = prom.Summary('python_my_req_example', 'Time spent processing a request')


@req_summary.time()
def process_request(t):
    time.sleep(t)


app = Flask("pyProm")

counter = prom.Counter('python_my_counter', 'This is my counter')

@app.route('/', methods=["GET", "POST"])
def hi():
    if request.method == "GET":
        counter.inc(1)
        return "OK", 200, None

    return "Bad Request", 400, None


monitor(app, port=8080)
app.run(host="0.0.0.0", port=80)
