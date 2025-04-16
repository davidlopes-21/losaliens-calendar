import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz
import re

# Timezones
tz_cdmx = pytz.timezone("America/Mexico_City")
tz_lisboa = pytz.timezone("Europe/Lisbon")

# URL da equipa Los Aliens na Kings League
url = "https://kingsleague.pro/en/teams/40-los-aliens-fc"

# Fazer scraping da página
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Criar calendário
cal = Calendar()

# Encontrar todos os blocos de jogos
match_blocks = soup.find_all("div", class_="competition_match")

for block in match_blocks:
    try:
        # Extrair a data (formato: 04/20 - 8:00 PM CDMX)
        date_tag = block.find("div", class_="date")
        if not date_tag:
            continue
        date_raw = date_tag.text.strip()

        # Encontrar os nomes das equipas
        team_names = block.find_all("span", class_="name")
        if len(team_names) != 2:
            continue

        team1 = team_names[0].text.strip()
        team2 = team_names[1].text.strip()

        # Identificar adversário
        opponent = team2 if "Aliens" in team1 else team1

        # Converter string para datetime
        match = re.search(r"(\d{2})/(\d{2}) - (\d{1,2}):(\d{2}) (AM|PM)", date_raw)
        if not match:
            continue

        month, day, hour, minute, period = match.groups()
        hour = int(hour)
        minute = int(minute)

        if period == "PM" and hour != 12:
            hour += 12
        if period == "AM" and hour == 12:
            hour = 0

        game_datetime_cdmx = datetime(2025, int(month), int(day), hour, minute)
        game_datetime_cdmx = tz_cdmx.localize(game_datetime_cdmx)
        game_datetime_lisboa = game_datetime_cdmx.astimezone(tz_lisboa)

        # Criar evento
        event = Event()
        event.name = f"Los Aliens FC vs {opponent}"
        event.begin = game_datetime_lisboa
        event.duration = timedelta(hours=1)
        event.description = "Jogo da Kings League Américas"

        cal.events.add(event)

    except Exception:
        continue

# Guardar o ficheiro ICS
with open("los_aliens_kings_league.ics", "w") as f:
    f.writelines(cal)
