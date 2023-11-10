from flask import Flask, render_template, request
from datetime import datetime, timedelta
# importerar in datetime samt timedelta, för att ta reda på datum och lägga till begränsningar i datum.
# https://www.geeksforgeeks.org/python-datetime-module/
import pytz
# importerar pytz för att primärt calculera om iso 8601
# https://www.geeksforgeeks.org/python-pytz/
from urllib import request as rq
import ssl
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/form")
def form():
    return render_template('form.html', headline="Please fill in the form")

@app.route("/api", methods=["POST"])
def api_post():
    # här får vi  inmatningen från våran from.html
    year = request.form["year"]
    month = request.form["month"]
    day = request.form["day"]
    price_range = request.form["price_range"]

    # Hämta aktuellt datum
    current_date = datetime.now().date()

    # Hanterar vi ogiltigt datumformat
    try:
        year, month, int_day = map(int, (year, month, day))
    except ValueError:
        return render_template('form.html', headline="Invalid date format. Use numbers for year, month, and day.")

    # vi skapar ett objekt med atuellt datum
    user_date = datetime(year, month, int_day).date()

    # Här bestämmer vi/beräknar vi vilket tidsintervall som är tillåtet
    year_ago = current_date - timedelta(days=365)  # year=1 inte tillåtet (vet fortfarande ej varför)
    next_day = current_date + timedelta(days=1)

    # kontrollerar att datumen är inom det tillåtna intervallet
    if year_ago <= user_date <= next_day:

        context = ssl._create_unverified_context()
        url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_range}.json"
        response = rq.urlopen(url, context=context).read()
        el_list = json.loads(response)

        # Extrahera data för att kalla på det i våran result.html senare
        data = []

        # Var tvungen att formattera om till zip, då jag fick felmeddelanden att datan var för stor.

        for time, sek in zip(el_list, el_list):
            # Konvertera ISO 8601 tiden till CET-tidszon
            time_start_iso8601 = time['time_start']
            time_start_cet = datetime.fromisoformat(time_start_iso8601).astimezone(pytz.timezone('CET'))

            # Här tar vi ut bara det vi vill ha från tiden, timmar och minuter
            formatted_time = time_start_cet.strftime("%H:%M")

            # här gräver vi ut priser från API:n
            sek_per_kwh = sek['SEK_per_kWh']

            # Lägg till tid och pris i vår tomma lista, data
            data.append((formatted_time, sek_per_kwh))

        return render_template('result.html', data=data)
    else:
        return render_template('form.html', headline="Ogiltigt datum. Vänligen välj ett datum som antingen är ett år bakåt i tiden eller en dag framåt från idag")

if __name__ == '__main__':
    app.run(debug=True)
