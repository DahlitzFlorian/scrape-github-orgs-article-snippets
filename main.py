from flask import Flask
from flask import render_template

from scrape_github_orgs import get_user_orgs

app = Flask(__name__)


@app.route("/")
def index():
    orgs = get_user_orgs("DahlitzFlorian")
    return render_template("index.html", orgs=orgs)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=5000)
