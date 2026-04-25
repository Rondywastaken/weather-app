from flask import *
from livereload import Server

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("app.py")
    server.serve(port=5000)