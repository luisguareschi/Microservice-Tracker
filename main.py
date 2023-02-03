import ast
from flask import Flask, request, jsonify
from API.MicroServiceTracker import MicroServiceTracker


class API:
    def __init__(self):
        self.app = Flask(__name__)
        mst = MicroServiceTracker()

        @self.app.route("/", methods=["GET"])
        def test():
            return "request received"

        @self.app.route("/start_session", methods=["POST"])
        def start_session():
            mst.start_session(request.json)
            return "request received"

        @self.app.route("/end_session", methods=["POST"])
        def end_session():
            mst.end_session(request.json)
            return "request received"

        @self.app.route("/add_event", methods=["POST"])
        def add_event():
            mst.add_event(request.json)
            return "request received"

        @self.app.route("/get_session", methods=["POST"])
        def get_session():
            session_id = request.json["sessionId"]
            if not mst.session_exists(session_id):
                return "sessionId not found"
            response = mst.get_session(session_id=session_id)
            return jsonify(response)

        @self.app.route("/get_machine_events", methods=["POST"])
        def get_machine_events():
            machine_id = request.json["machineId"]
            if not mst.machine_id_exists(machine_id):
                return "MachineId not found"
            response = mst.get_machine_events(machine_id=machine_id)
            return jsonify(response)

    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    # start the server and the microservice tracker class
    api = API()
    api.run()


