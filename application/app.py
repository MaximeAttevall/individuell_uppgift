from flask import Flask, render_template, request
# importera in datum och tid, Timedelta class is used for calculating differences between dates and represents a duration. The difference can both be positive as well as negative.
# https://www.geeksforgeeks.org/python-datetime-timedelta-class/
from datetime import datetime, timedelta
import pandas as pd
import requests
import json

app = Flask(__name__)


@app.route("/")
def index():

    return render_template('index.html')


@app.route("/form")
def form():
    return render_template('form.html', headline="please fill in the form")



@app.route("/api", methods=["POST"])
def api_post():
    # Get
    year = request.form["year"]
    month = request.form["month"]
    day = request.form["day"]
    price_range = request.form["price_range"]

    # Get the current date
    current_date = datetime.now().date()

    try:
        year = int(year)
        month = int(month)
        day = int(day)
    except ValueError:
        return render_template('form.html', headline="Invalid date format. Please use numbers for year, month, and day.")

    # Create a date object from the user input
    user_date = datetime(year, month, day).date()

    # Calculate the allowed date range (current day, previous day, and next day)
    allowed_dates = [current_date, current_date - timedelta(days=1), current_date + timedelta(days=1)]

    # Check if the user's date is within the allowed range
    if user_date not in allowed_dates:
        return render_template('form.html', headline="Invalid date. Please select the current day, the previous day, or the next day.")

    # Continue with your code to fetch data using the validated date
    url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_range}.json"
    response = requests.get(url)
    el_list = json.loads(response.text)

    df = pd.DataFrame(el_list)
    table_data = df.to_html(classes="table p-5", justify="left")

    return render_template('test.html', table_data=table_data)



if __name__ == '__main__':
    app.run(debug=True)
