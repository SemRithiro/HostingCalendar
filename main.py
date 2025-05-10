from flask import Flask, Response, request
from datetime import datetime
from flask_cors import CORS
import uuid
import pytz

app = Flask(__name__)
CORS(app)

# Local timezone
local_tz = pytz.timezone("Asia/Phnom_Penh")

events = [
    {
        'uid': f'aaaaa@udaya-tech.com',
        'organizer': 'Sem Rithiro',
        'summary': 'Weekly Progress Meeting',
        'description': 'Weekly Progress Meeting',
        'dtimestamp': datetime.now(pytz.utc).strftime('%Y%m%dT%H%M%SZ'),
        'start': local_tz.localize(datetime(2025, 3, 3, 16, 42)).strftime("%Y%m%dT%H%M%S"),
        'end': local_tz.localize(datetime(2025, 3, 3, 17, 0)).strftime("%Y%m%dT%H%M%S"),
        'location': 'HO First Floor',
        'rrule': f'RRULE:FREQ=WEEKLY;BYDAY=MO,SA;UNTIL={local_tz.localize(datetime(2025, 5, 1, 00, 00)).strftime("%Y%m%dT%H%M%S")}',
        'alarm': {
            'action': 'DISPLAY',
            'trigger': '-PT2M',
            'description': 'Reminder - Meeting in 15 minutes'
        }
    }
]

def generate_vevent(event):
    vevent = f"""BEGIN:VEVENT
UID:{event['uid']}
ORGANIZER:{event['organizer']}
DTSTAMP:{event['dtimestamp']}
DTSTART:{event['start']}
DTEND:{event['end']}
SUMMARY:{event['summary']}
CATEGORIES: private
DESCRIPTION:{event['description']}
LOCATION:{event['location']}
{event['rrule']}"""

    if 'alarm' in event:
        vevent = f"""{vevent}

BEGIN:VALARM
ACTION:{event['alarm']['action']}
TRIGGER:{event['alarm']['trigger']}
DESCRIPTION:{event['alarm']['description']}
END:VALARM

END:VEVENT"""

    else:
        vevent = f"""{vevent}
        
END:VEVENT"""
    return vevent
        

def generate_calendar():
    vevents = "\n".join([generate_vevent(event) for event in events])
    
    base_calendar = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//UDAYA//UT-Calendar//EN
CALSCALE:GREGORIAN
X-WR-CALNAME:RMS Default

BEGIN:VTIMEZONE
TZID:Asia/Phnom_Penh
BEGIN:STANDARD
DTSTART:19700101T000000
TZOFFSETFROM:+0700
TZOFFSETTO:+0700
TZNAME:ICT
END:STANDARD
END:VTIMEZONE

{vevents}

BEGIN:VTODO
UID:123456789@example.com
DTSTAMP:20250331T120000Z
DUE:20250402T170000Z
SUMMARY:Complete Project Report
DESCRIPTION:Finish the project report and submit it before the deadline.
STATUS:NEEDS-ACTION
PRIORITY:1
END:VTODO

END:VCALENDAR
"""
    return base_calendar


@app.route("/calendar.ics")
def serve_calendar():
    ics_content = generate_calendar()
    print(ics_content)
    return Response(ics_content, mimetype="text/calendar")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=9000)