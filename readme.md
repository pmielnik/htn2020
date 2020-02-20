# Hack the North 2020 Backend Challenge

## Table of Contents
 * [Hack the North 2020 Backend Challenge](#hack-the-north-2020-backend-challenge)
      * [Setup](#setup)
      * [GET method endpoints](#get-method-endpoints)
         * [GET all users](#get-all-users)
         * [GET user by id](#get-user-by-id)
         * [GET user by location range](#get-user-by-location-range)
         * [GET all events](#get-all-events)
         * [GET event by id](#get-event-by-id)
         * [GET event attendees by id](#get-event-attendees-by-id)
      * [POST method endpoints](#post-method-endpoints)
         * [POST event attendee by id](#post-event-attendee-by-id)
     * [Next Steps](#next-steps)

## Setup
In order to run this server, navigate to the directory containing the main file and run
`export FLASK_APP=main`, then run `flask run`. You can now make calls to the server!

At any point in time, you can go to `http://127.0.0.1:5000/help` for a quick overview of
available endpoints.

## GET method endpoints

### GET all users
*Link:* `http://127.0.0.1:5000/users`

Returns a list of all users in the htn2020 database.

**Response Format:**
```json
[
    {
        "user": {
            "attended_events": [
                str,
                ...
            ],
            "company_name": str,
            "id": int,
            "latitude": float,
            "longitude": float,
            "name": str,
            "phone": str,
            "picture": str
        }
    },
    ...
]
```

### GET user by id
*Link:* `http://127.0.0.1:5000/users/<user_id>`

Returns the information for a single user given their ID.

**Response Format:**
```json
{
    "user": {
        "attended_events": [
            str,
            ...
        ],
        "company_name": str,
        "id": int,
        "latitude": long,
        "longitude": long,
        "name": str,
        "phone": str,
        "picture": str
    }
}
```

### GET user by location range
*Link:* `http://127.0.0.1:5000/location?latitude=<lat>&longitude=<long>&range=<range>`

Returns a list of user objects within the given location range (lat +- range, long +- range).
Please ensure that latitude, longitude, and range are all float values.

**Response Format:**
```json
[
    {
        "id": int,
        "name": str
    },
    ...
]
```

### GET all events
*Link:* `http://127.0.0.1:5000/events`

Returns a list of all event objects.

**Response Format:**
```json
[
     {
        "event": {
            "id": int,
            "name": str,
            "user_ids": [
                int,
                ...
            ]
        }
    },
    ...
]
```

### GET event by id
*Link:* `http://127.0.0.1:5000/events/<event_id>`

Returns an event object with the given id.

**Response Format:**
```json
{
    "attendees": [
        {
            "attended_events": str,
            "company_name": str,
            "id": int,
            "latitude": float,
            "longitude": float,
            "name": str,
            "phone": str,
            "picture": str
        },
        ...
    ],
    "id": int,
    "name":str
}
```

### GET event attendees by id
*Link:* `http://127.0.0.1:5000/events/<event_id>/attendees`

Returns an event object with the given id.

**Response Format:**
```json
[
    {
        "attendee": {
            "name": str,
            "user_id": int
        }
    },
    ...
]
```

## POST method endpoints

### POST event attendee by id
*Link:* `http://127.0.0.1:5000/events/<event_id>/attendees`

Regeisters a user as an event attendee.

**Request Format:**
```json
{
    "user_id":int
}
```

## Next Steps
* add POST endpoints to allow API cals to create and update database information
* create more specific GET endpoints for events, users, companies, and locations to find things by id or by name
* host this server online instead of locally
* add more information to events table in db, for example time, location, and facilitators
* add more information to locations table in db, for example a more general location of city/country
* add more information to companies in db