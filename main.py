import ast
from flask import Flask, request, jsonify
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


@app.route("/get_session", methods=["POST"])
def get_session():
    session_id = request.json["sessionId"]
    if not mst.session_exists(session_id):
        return "sessionId not found"
    sessions_df = mst.db.get_sessions()
    sessions_df = sessions_df[sessions_df["sessionId"] == session_id]
    events_df = mst.db.get_events()
    events_df = events_df[events_df["sessionId"] == session_id]
    events = []
    for index in events_df.index:
        event_info = {
            "eventType": events_df["eventType"][index],
            "eventAt": events_df["eventAt"][index],
            "payload": ast.literal_eval(events_df["payload"][index])
        }
        events.append(event_info)
    response = {
        "sessionId": session_id,
        "userId": sessions_df["userId"][sessions_df.index[0]],
        "orgId": int(sessions_df["orgId"][sessions_df.index[0]]),
        "startAt": sessions_df["startAt"][sessions_df.index[0]],
        "endAt": sessions_df["endAt"][sessions_df.index[0]],
        "events": events
    }
    return jsonify(response)


app.run(debug=True)

if __name__ == '__main__':
    pass
