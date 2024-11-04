from flask import Flask, jsonify, request
from mongo.main import (
    insertProduct,
    deleteProduct,
    getProductByName,
    getProductByCategory,
    getProductByDressmarker,
    editProduct,
    getCategorys,
    getHistory,
    ActualMongosCart,
    updateCartMongo,
    alterStatsus,
    addForms,
    getLastForms,
)
from flask_cors import CORS
from Predis.main import setCart, updateCart, getCart
import json
from bson import json_util
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Foi"


@app.route("/insert/product", methods=["POST"])
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


@app.route("/delete", methods=["DELETE"])
def delete():
    idP = request.args.get("id", type=int)

    return jsonify({"Total de produtos deletados": deleteProduct(idP)})


# /delete?id=10


@app.route("/update", methods=["PUT"])
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


@app.route("/get/name", methods=["GET"])
def getByName():
    name = request.args.get("name", type=str)
    products = [dict(item) for item in getProductByName(name)]
    json_data = json.loads(json_util.dumps(products))
    print(json_data)
    return jsonify(json_data)


@app.route("/get/category", methods=["GET"])
def getByCategory():
    category = request.args.get("category", type=str)
    products = [dict(item) for item in getProductByCategory(category)]
    json_data = json.loads(json_util.dumps(products))
    print(json_data)
    return jsonify(json_data)


@app.route("/get/dressmarker", methods=["GET"])
def getByDressmarker():
    dressmarker = request.args.get("dressmarker", type=str)
    products = [dict(item) for item in getProductByDressmarker(dressmarker)]
    return jsonify(products)


@app.route("/category", methods=["GET"])
def getCategory():
    categorys = [dict(item) for item in getCategorys()]
    json_data = json.loads(json_util.dumps(categorys))
    return jsonify(json_data)


@app.route("/historyOrder", methods=["GET"])
def getHistoryOrder():
    cpf = request.args.get("cpf", type=str)
    orders = [dict(item) for item in getHistory(cpf)]
    json_data = json.loads(json_util.dumps(orders))
    return jsonify(json_data)


@app.route("/redisCart", methods=["GET"])
def getRedisCart():
    cpf = request.args.get("cpf", type=str)
    order = setCart(cpf)
    if len(order) is not None:
        orders = []
        for item in order:
            if type(item) is float:
                orders.append(("Total", item))
            else:
                orders.append(tuple(item))

        json_data = json.loads(json_util.dumps(orders))
        return jsonify(json_data)
    else:
        orders = []
        return orders


@app.route("/updateRedisCart", methods=["PUT"])
def updateRedisCart():
    cpf = request.args.get("cpf", type=str)
    quantidade = request.args.get("quantidade", type=int)
    produto = request.args.get("produto", type=str)
    preco = getProductByName(produto)
    preco = [item for item in preco]
    if preco == []:
        response = "Produto não encontrado"

    else:
        preco = preco[0]["price"]
        response = updateCart(cpf, produto, quantidade, preco)
    print("PRECO", preco)
    return jsonify(response)


@app.route("/updateMongoCart", methods=["PUT"])
def updateMongo():
    cpf = request.args.get("cpf", type=str)
    get = getCart(cpf)
    update = updateCartMongo(cpf, get)

    return jsonify(update)


@app.route("/alterStatus", methods=["PUT"])
def alterStatus():
    cpf = request.args.get("cpf", type=str)
    status = request.args.get("status", type=str)
    return jsonify(alterStatsus(cpf, status))


@app.route("/forms", methods=["POST"])
def forms():
    itens = request.get_json()
    response = addForms(itens)
    print({"Total inserted": str(response)})
    return jsonify({"Total inserted": str(response)})


@app.route("/lastForms", methods=["GET"])
def lastForms():
    response = getLastForms()
    return jsonify(list(response))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
