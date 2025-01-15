import datetime
import os
from typing import List
from urllib.request import Request

from fastapi import APIRouter, HTTPException
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from schemas.v1.CalendarHub import Event

router = APIRouter()

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def authenticate_google():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_calendar_events():
    creds = authenticate_google()
    service = build("calendar", "v3", credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    return [
        Event(
            id=event["id"],
            summary=event["summary"],
            start=event["start"].get("dateTime"),
            end=event["end"].get("dateTime"),
        )
        for event in events
    ]


@router.get("/calendar/events", response_model=List[Event], status_code=200)
def get_events():
    try:
        events = get_calendar_events()
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
