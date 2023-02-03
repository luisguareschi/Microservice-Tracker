import sqlite3
import pandas as pd


class DBManager:
    def __init__(self, db_path: str):
        """Class that takes care of interacting with the Database
        db_path: is the location of the database to witch the object connects to"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cur = self.conn.cursor()

    def get_sessions(self) -> pd.DataFrame:
        """returns a df with the sessions table"""
        query = "SELECT * FROM sessions"
        df = pd.read_sql(query, con=self.conn)
        return df

    def get_events(self) -> pd.DataFrame:
        """returns a df with all the events"""
        query = "SELECT * FROM events"
        df = pd.read_sql(query, con=self.conn)
        return df

    def add_session(self, session_id: str, user_id: str, org_id: int, start_at, machine_id: str):
        """records a session to the database"""
        query = f"INSERT INTO sessions VALUES ('{session_id}', '{user_id}', '{org_id}', '{start_at}', NULL, '{machine_id}')"
        self.cur.execute(query)
        self.conn.commit()
        print("session added succesfully")

    def end_session(self, session_id: str, end_at):
        """sets the value for the 'endAt' column for a specific session"""
        query = f"UPDATE sessions SET endAt = '{end_at}' WHERE sessionId = '{session_id}'"
        self.cur.execute(query)
        self.conn.commit()

    def add_event(self, session_id: str, event_type: str, event_at, payload: str):
        """records an event in the database"""
        query = f"INSERT INTO events VALUES ('{session_id}', '{event_type}', '{event_at}', '{payload}')"
        self.cur.execute(query)
        self.conn.commit()


if __name__ == '__main__':
    db = DBManager(db_path=r"C:\Users\LUIS G\OneDrive\Documents\Python Projects\Microservice Tracker\db.db")
    # db.add_session(session_id="test", user_id="1234", org_id=4321, start_at="timestamp")
    # db.end_session(session_id="test", end_at="date")
    # db.add_event(session_id='lol', event_type='app_used', event_at='some', payload='lmao')
    db.get_events()
    print()
    db.get_sessions()

