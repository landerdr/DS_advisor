from flask.cli import FlaskGroup
from flask import Flask, render_template
import os

app = Flask(__name__)
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)
cli = FlaskGroup(app)


@app.route("/")
def manual():
    return render_template("home.html")


if __name__ == "__main__":
    cli()
