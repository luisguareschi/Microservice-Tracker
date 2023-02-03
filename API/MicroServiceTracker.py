import ast
import sqlite3
from flask import jsonify
from API.DBManager import DBManager
import random, string
import datetime as dt
import json as j
import os


def parse_timestamp(timestamp: int) -> dt.datetime:
    date = dt.datetime.fromtimestamp(timestamp)
    return date


class MicroServiceTracker:
    def __init__(self):
        """Class that handles all the requests"""
        # get the path of the directory folder
        API_folder = os.path.dirname(__file__)
        directory_folder = os.path.dirname(API_folder)
        self.db = DBManager(db_path=os.path.join(directory_folder, "db.db"))

    def session_exists(self, session_id) -> bool:
        """checks in the database if the session_id exists"""
        sessions_df = self.db.get_sessions()
        ids = list(sessions_df["sessionId"])
        return session_id in ids

    def machine_id_exists(self, machine_id) -> bool:
        """checks in the database if the machine_id exists"""
        sessions_df = self.db.get_sessions()
        ids = list(sessions_df["machineId"])
        return machine_id in ids

    def start_session(self, json: dict):
        """handles the request to record a session to the database"""
        # convert timestamp to datetime object
        date = parse_timestamp(json["startAt"])
        while True:
            # create a random session id
            session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=14)).lower()
            session_id = f"{session_id[0:5]}-{session_id[5:9]}-{session_id[9:len(session_id)]}"
            try:
                self.db.add_session(session_id=session_id, user_id=json["userId"], org_id=json["orgId"],
                                    start_at=date, machine_id=json["machineId"])
                break
            except sqlite3.IntegrityError:  # in case the session_id already exists
                pass

    def end_session(self, json: dict):
        """handles the request to add an end session date to an existing request"""
        if not self.session_exists(json["sessionId"]):
            return
        date = parse_timestamp(json["endAt"])
        self.db.end_session(session_id=json["sessionId"], end_at=date)

    def add_event(self, json: dict):
        """handles the request to add an event to the events table"""
        if not self.session_exists(json["sessionId"]):
            return
        # iterate over the list of events and add each event to the db
        for event in json["events"]:
            print(event)
            date = parse_timestamp(event["eventAt"])
            payload = event["payload"]
            self.db.add_event(
                session_id=json["sessionId"],
                event_type=event["eventType"],
                event_at=date,
                payload=j.dumps(payload)
            )

    def get_session(self, session_id: str) -> dict:
        """Function that gets all the events and info from a session"""
        sessions_df = self.db.get_sessions()
        sessions_df = sessions_df[sessions_df["sessionId"] == session_id]
        events_df = self.db.get_events()
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
            "machineId": sessions_df["machineId"][sessions_df.index[0]],
            "startAt": sessions_df["startAt"][sessions_df.index[0]],
            "endAt": sessions_df["endAt"][sessions_df.index[0]],
            "events": events
        }
        return response

    def get_machine_events(self, machine_id: str) -> dict:
        """Function that gets all the events from a machine"""
        # get the sessions with a specific id
        sessions_df = self.db.get_sessions()
        sessions_df = sessions_df[sessions_df["machineId"] == machine_id]
        sessions_ids = sessions_df["sessionId"].to_list()
        events_df = self.db.get_events()
        events_df = events_df[events_df["sessionId"].isin(sessions_ids)]
        response = {
            "events": [],
            "machineId": machine_id
                    }
        for index in events_df.index:
            data = {
                "sessionId": events_df["sessionId"][index],
                "eventType": events_df["eventType"][index],
                "eventAt": events_df["eventAt"][index],
                "payload": ast.literal_eval(events_df["payload"][index]),
            }
            response["events"].append(data)
        return response


if __name__ == '__main__':
    mst = MicroServiceTracker()
    print(mst.session_exists(session_id='32342-24s-42343'))
