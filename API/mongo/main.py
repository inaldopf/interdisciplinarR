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
