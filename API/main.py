from mongo.main import getCol
from Predis.main import getId
from flask import Flask

# print(getId(itens))
# itens = getCol()["ids"]


app = Flask(__name__)


@app.route("/get/<id>")
def get(id):
    return getId(id)


app.run(debug=True)
