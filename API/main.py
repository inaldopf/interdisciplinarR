from mongo.main import getColection
from Predis.main import getId
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Foi"


@app.route("/get/<id>")
def get(id):
    return getId(id)

@app.route("/mongo")
def getByMongo():
    return getColection()



if __name__ == "__main__":
    app.run(host="0.0.0.0")
