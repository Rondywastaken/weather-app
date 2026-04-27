from flask import *
from livereload import Server
from api import *

app = Flask(__name__)

@app.route("/")
def index():
    location = request.args.get("location")
    if not location:
        return render_template("index.html")

    try:    
        data, country, city = get_weather(location)
    except Exception as e:
        return render_template("index.html", error=e)

    return render_template(
        "index.html",
        location=location,
        weather_temp=data["hourly"]["temperature_2m"][0],
        country=country,
        city=city,
    )

if __name__ == "__main__":
    app.debug = True
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("static/styles")
    server.watch("app.py")
    server.serve(port=5000)