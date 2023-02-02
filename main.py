from flask import Flask, request
from API.MicroServiceTracker import MicroServiceTracker

# start the server and the microservice tracker class
app = Flask(__name__)
mst = MicroServiceTracker()


@app.route("/", methods=["GET"])
def test():
    return "request received"


@app.route("/start_session", methods=["POST"])
def start_session():
    mst.start_session(request.json)
    return "request received"


@app.route("/end_session", methods=["POST"])
def end_session():
    mst.end_session(request.json)
    return "request received"


@app.route("/add_event", methods=["POST"])
def add_event():
    mst.add_event(request.json)
    return "request received"


app.run(debug=True)

if __name__ == '__main__':
    pass
