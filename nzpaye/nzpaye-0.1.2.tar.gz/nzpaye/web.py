from flask import Flask
from flask import render_template
from flask import request
from nzpaye import paye

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', title='Home')

@app.route("/calculate", methods=["GET"])
def calculate():
    hourly_rate = request.args.get('inputHourlyRate', default=100, type=float)
    hours_worked = request.args.get('inputHoursWorked', default=40, type=float)
    summary = paye.income_summary(hourly_rate, hours_worked)
    return render_template('paye_summary.html', summary=summary)