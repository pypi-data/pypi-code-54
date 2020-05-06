from icalendar import Calendar, Event
from datetime import datetime, timedelta
from icalendar import vCalAddress, vText



def create_ics(name, email, dt_assignment, task_name, organizer_email, offset_days=0):
    ical = None
    try:
        cal = Calendar()
        cal.add('prodid', '-//My calendar product//mxm.dk//')
        cal.add('version', '2.0')

        organizer = vCalAddress('MAITO:%s' % organizer_email)
        organizer.params['cn'] = vText(organizer_email)
        event = Event()
        event.add('summary', task_name)

        dt_assignment = dt_assignment + timedelta(days=offset_days)
        month = dt_assignment.month
        day = dt_assignment.day
        year = dt_assignment.year
        event.add('dtstart', datetime(year,month,day,18,30,0))
        event.add('dtend', datetime(year,month,day,20,30,0))
        event['organizer'] = organizer

        attendee = vCalAddress('MAILTO:%s' % email)
        event.add('attendee', attendee)

        cal.add_component(event)
        ical = cal.to_ical()
    except Exception as e:
        print("ERROR!!" + e)
    finally:
        return ical