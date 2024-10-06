from mongo.main import getColection
from Predis.main import getId
from flask import Flask, jsonify, request
from mongo.main import insertProduct, deleteProduct

app = Flask(__name__)


@app.route("/")
def index():
    return "Foi"


@app.route("/get/<id>")
def get(id):
    return getId(id)


@app.route("/mongo")
def getByMongo():
    mongo = [str(item) for item in getColection()]
    print(mongo)
    return jsonify(mongo)


@app.route("/insert/product")
def insertProductRoute():
    idP = request.args.get("id", type=int)
    name = request.args.get("name", type=str)
    price = request.args.get("price", type=float)
    imageurl = request.args.get("imageurl", type=str)
    typeId = request.args.get("typeId", type=int)
    dressmarker = request.args.get("dressmarker", type=str)
    avaliation = request.args.get("avaliation", type=float)
    return jsonify(
        insertProduct(idP, name, price, imageurl, typeId, dressmarker, avaliation)
    )  # /insert/product?id=10&name=Camiseta&price=49.99&imageurl=http://image.com&typeId=5&dressmarker=Maria&avaliation=4


@app.route("/delete")
def delete():
    idP = request.args.get("id", type=int)

    return jsonify({"Total de produtos deletados": deleteProduct(idP)})


# /delete?id=10


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
