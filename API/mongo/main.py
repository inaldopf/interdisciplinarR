from .__init__ import db
import json

colecao = db.get_collection("order")

# print(dict(colecao.find_one()))


def getColection():
    order = db["order"]
    order = order.find()
    orders = []
    for i in order:
        orders.append(i)
    return orders


def insertProduct(id, name, price, imageurl, typeId, dressmarker, avaliation):
    product = db["product"]
    status = product.insert_one(
        {
            "id": id,
            "name": name,
            "price": price,
            "imageUrl": imageurl,
            "typeId": typeId,
            "dressMarkerName": dressmarker,
            "avaliation": avaliation,
        }
    ).inserted_id
    return str(status)
