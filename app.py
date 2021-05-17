"""
source code: https://blog.heptanalytics.com/flask-plotly-dashboard/
"""
from flask import Flask, render_template
from scripts.main import OwidData

app = Flask(__name__)

fig_data = OwidData()


@app.route("/")
def index():
    daily_doses = fig_data.daily_doses()
    total_doses = fig_data.total_doses()
    remaining_pop, remaining_days, last_ma, total_pop = fig_data.last_update()
    return render_template(
        "index.html",
        plot1=daily_doses,
        plot2=total_doses,
        remaining_pop=remaining_pop,
        remaining_days=remaining_days,
        last_ma=last_ma,
        total_pop=total_pop,
    )


if __name__ == "__main__":
    app.run(debug=False)
