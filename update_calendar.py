from ics import Calendar, Event
from datetime import datetime
import pytz

# Timezone Lisboa
tz = pytz.timezone("Europe/Lisbon")

cal = Calendar()

# Exemplo de evento
event = Event()
event.name = "Los Aliens vs Peluche Caligari"
event.begin = tz.localize(datetime(2025, 4, 21, 3, 0))
event.description = "Kings League Américas"
event.duration = {"hours": 1}

cal.events.add(event)

with open("los_aliens_kings_league.ics", "w") as f:
    f.writelines(cal)
