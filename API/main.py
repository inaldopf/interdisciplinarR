from mongo.main import getCol
from Predis.main import getId
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Foi"
    
@app.route("/get/<id>")
def get(id):
    return getId(id)

if __name__ == "__main__"
    app.run()
