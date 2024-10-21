from mongo.main import getColection
from Predis.main import getId
from flask import Flask, jsonify, request
from mongo.main import (
    insertProduct,
    deleteProduct,
    getProductByName,
    getProductByCategory,
    getProductByDressmarker,
    editProduct,
)
import json
from bson import json_util

app = Flask(__name__)


@app.route("/")
def index():
    return "Foi"


@app.route("/get/<id>")
def get(id):
    return getId(id)


@app.route("/mongo")
def getByMongo():
    mongo = list(getColection())
    json_data = json.loads(json_util.dumps(mongo))
    print(json_data)
    return jsonify(json_data)


@app.route("/insert/product")
def insertProductRoute():
    name = request.args.get("name", type=str)
    price = request.args.get("price", type=float)
    imageurl = request.args.get("imageurl", type=str)
    typeId = request.args.get("typeId", type=int)
    dressmarker = request.args.get("dressmarker", type=str)
    avaliation = request.args.get("avaliation", type=float)
    description = request.args.get("description", type=str)
    size = request.args.get("size", type=str)
    return str(
        insertProduct(
            name,
            price,
            imageurl,
            typeId,
            dressmarker,
            avaliation,
            description,
            size,
        )
    )  # /insert/product?&name=Camiseta&price=49.99&imageurl=http://image.com&typeId=5&dressmarker=Maria&avaliation=4


@app.route("/delete")
def delete():
    idP = request.args.get("id", type=int)

    return jsonify({"Total de produtos deletados": deleteProduct(idP)})


# /delete?id=10


@app.route("/update")
def update():
    idP = request.args.get("id", type=int)
    name = request.args.get("name", type=str)
    price = request.args.get("price", type=float)
    imageurl = request.args.get("imageurl", type=str)
    typeId = request.args.get("typeId", type=int)
    dressmarker = request.args.get("dressmarker", type=str)
    avaliation = request.args.get("avaliation", type=float)
    description = request.args.get("description", type=str)
    size = request.args.get("size", type=str)
    return str(
        editProduct(
            idP,
            name,
            price,
            imageurl,
            typeId,
            dressmarker,
            avaliation,
            description,
            size,
        )
    )  # /update?id=10


@app.route("/get/name")
def getByName():
    name = request.args.get("name", type=str)
    products = [str(item) for item in getProductByName(name)]
    json_data = json.loads(json_util.dumps(products))
    print(json_data)
    return jsonify(json_data)


@app.route("/get/category")
def getByCategory():
    category = request.args.get("category", type=str)
    products = [str(item) for item in getProductByCategory(category)]
    json_data = json.loads(json_util.dumps(products))
    print(json_data)
    return jsonify(json_data)


@app.route("/get/dressmarker")
def getByDressmarker():
    dressmarker = request.args.get("dressmarker", type=str)
    products = [str(item) for item in getProductByDressmarker(dressmarker)]
    return jsonify(products)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
