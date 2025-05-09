from flask import Flask
from skywalking import agent, config

config.init(
    service_name='flask-demo',
    backend_service='localhost:11800'
)
agent.start()

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello from Flask with SkyWalking!"
