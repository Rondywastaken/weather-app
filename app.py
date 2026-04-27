from flask import Flask, request, render_template
from livereload import Server
from api import get_weather, get_current_hour_index, get_weather_icon
from collections import defaultdict


app = Flask(__name__)

app.jinja_env.globals["get_weather_icon"] = get_weather_icon

@app.route("/")
def index():
    location = request.args.get("location")
    if not location:
        return render_template("index.html")

    try:    
        data, country, city = get_weather(location)
    except Exception as e:
        return render_template("index.html", error=e)

    current_hour_index = get_current_hour_index(data)
    current_hour_temp = data["hourly"]["temperature_2m"][current_hour_index]
    current_hour = data["hourly"]["time"][current_hour_index].split("T")[1]
    current_day = data["hourly"]["time"][current_hour_index].split("T")[0]
    current_hour_icon = get_weather_icon(data["hourly"]["weather_code"][current_hour_index])

    days = data["daily"]["time"]
    days_temps = data["daily"]["temperature_2m_mean"]
    days_icons = data["daily"]["weather_code"]

    hours = data["hourly"]["time"]
    hours_temps = data["hourly"]["temperature_2m"]
    hours_by_day = defaultdict(lambda: {"hours": [], "temps": []})
    for i, time in enumerate(hours):
        date, hour = time.split("T")
        hours_by_day[date]["hours"].append(hour)
        hours_by_day[date]["temps"].append(hours_temps[i])


    return render_template(
        "index.html",
        location=location,
        weather_temp=data["hourly"]["temperature_2m"][0],
        country=country,
        city=city,
        current_day=current_day,
        current_hour=current_hour,
        current_temp=current_hour_temp,
        current_icon=current_hour_icon,
        days=days,
        days_temps=days_temps,
        days_icons=days_icons,
        hours=hours,
        hours_temps=hours_temps,
        hours_by_day=hours_by_day
    )

if __name__ == "__main__":
    app.debug = True
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("static/styles")
    server.watch("static/scripts")
    server.watch("app.py")
    server.serve(port=5000)
