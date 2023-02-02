import sqlite3
from flask import jsonify
from API.DBManager import DBManager
import random, string
import datetime as dt
import json as j


def parse_timestamp(timestamp: int) -> dt.datetime:
    date = dt.datetime.fromtimestamp(timestamp)
    return date


class MicroServiceTracker:
    def __init__(self):
        """Class that handles all the requests"""
        self.db = DBManager(db_path=r"C:\Users\LUIS G\OneDrive\Documents\Python Projects\Microservice Tracker\db.db")

    def session_exists(self, session_id) -> bool:
        """checks in the database if the session_id exists"""
        sessions_df = self.db.get_sessions()
        ids = list(sessions_df["sessionId"])
        return session_id in ids

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
                                    start_at=date)
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


if __name__ == '__main__':
    mst = MicroServiceTracker()
    print(mst.session_exists(session_id='32342-24s-42343'))
