# Microservice-Tracker
Assignment coding challenge

The following API works by using the `Flask` libray in `python3.9` with a `sqlite` database.

In order to start the server one must run the script `"main.py"`

The APIs folder has two main classes, DBManager (which contains all the methods to access the SQLite database) and MicroserviceTracker (which contains all the methods for storing the requests made to the server)

# API Endpoints:
- ## Start Session: `/start_session`
  Method: `POST` \
  Example:
  ```json
  {
    "userId": "asfla-asdf-asdfa",
    "machineId": "2343-asdf-fads",
    "startAt": "timestamp",
    "orgId": 11232
  }
  ```
  Returns: `"request received"`

- ## Add Event: `/add_event`
  Method: `POST` \
  Example:
  ```json
  {
    "sessionId": "aslk-234-009",
    "events": [
      {
      "eventAt": "timestamp",
      "eventType": "{event_type}",
      "payload": {}
      }
    ]
  }
  ```
  Returns: `"request received"`
- ## End Session: `/end_session`
  Method: `POST` \
  Example: 
  ```json
  {
    "sessionId": "32342-234s-42343",
    "endAt": "timestamp"
  }

  ```
  Returns: `"request received"`
- ## Get Session: `/get_session`
  Method: `POST` \
  Example: 
  ```json
  {
    "sessionId": "y25v9-jbyr-kyigb"
  }
  ```
  Returns: 
  ```json
  {
    "endAt": "2023-02-02 16:22:15",
    "events": [
      {
        "eventAt": "2023-02-02 16:22:15",
        "eventType": "applicationStarted",
        "payload": {
          "info": "someInfo"
        }
      },
      {
        "eventAt": "2023-02-09 01:08:55",
        "eventType": "exe",
        "payload": {
          "info": "someInfo"
        }
      },
      {
        "eventAt": "2023-02-09 01:05:23",
        "eventType": "data",
        "payload": {
          "info": "someInfo"
        }
      }
    ],
    "machineId": "2343-asdf-fads",
    "orgId": 11232,
    "sessionId": "y25v9-jbyr-kyigb",
    "startAt": "2023-02-02 16:22:15",
    "userId": "asfla-asdf-asdfa"
  }
  ```
- ## Get Machine Events: `/get_machine_events`
  Method: `POST` \
  Example: 
  ```json
  {
    "machineId":"2343-asdf-fads"
  }
  ```
  Returns: 
  ```json
  {
    "events": [
      {
        "eventAt": "2016-01-01 11:20:05.123",
        "eventType": "eventType",
        "payload": {
          "info": "some info"
        },
        "sessionId": "32342-234s-42343"
      },
      {
        "eventAt": "2023-02-02 16:22:15",
        "eventType": "applicationStarted",
        "payload": {
          "info": "someInfo"
        },
        "sessionId": "y25v9-jbyr-kyigb"
      },
      {
        "eventAt": "2023-02-09 01:08:55",
        "eventType": "exe",
        "payload": {
          "info": "someInfo"
        },
        "sessionId": "y25v9-jbyr-kyigb"
      },
      {
        "eventAt": "2023-02-09 01:05:23",
        "eventType": "data",
        "payload": {
          "info": "someInfo"
        },
        "sessionId": "y25v9-jbyr-kyigb"
      }
    ],
    "machineId": "2343-asdf-fads"
  }
  ```
  
# Database Structure:
The database was made with `sqlite`. It consists of two tables: `sessions` & `events`. The name of the file is `"db.db"`
- ## Sessions Table:
  `session`
  | sessionId        	| userId           	| orgId 	| startAt                 	| endAt               	| machineId      	|
  |------------------	|------------------	|-------	|-------------------------	|---------------------	|----------------	|
  | 32342-234s-42343 	| asfla-asdf-asdfa 	| 11232 	| 2016-01-01 10:20:05.123 	| 2023-02-02 16:22:15 	| 2343-asdf-fads 	|
  | y25v9-jbyr-kyigb 	| asfla-asdf-asdfa 	| 11232 	| 2023-02-02 16:22:15     	| 2023-02-02 16:22:15 	| 2343-asdf-fads 	|
  
- ## Events Table:
  | sessionId        	| eventType          	| eventAt             	| payload              	|
  |------------------	|--------------------	|---------------------	|----------------------	|
  | y25v9-jbyr-kyigb 	| applicationStarted 	| 2023-02-02 16:22:15 	| `{"info": "someInfo"}` 	|
  | y25v9-jbyr-kyigb 	| exe                	| 2023-02-09 01:08:55 	| `{"info": "someInfo"}` 	|
  
  

