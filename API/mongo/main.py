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


def insertProduct(
    name, price, imageurl, typeId, dressmarker, avaliation, description, size
):
    product = db["product"]
    Proxid = product.find_one(sort=[("id", -1)])
    Proxid = Proxid["id"] + 1
    status = product.insert_one(
        {
            "id": Proxid,
            "name": name,
            "price": price,
            "imageUrl": imageurl,
            "typeId": typeId,
            "dressMarkerName": dressmarker,
            "avaliation": avaliation,
            "description": description,
            "size": size,
        }
    ).inserted_id
    return status


def deleteProduct(id):
    product = db["product"]
    status = product.delete_one({"id": id}).deleted_count
    return status


def getProductByName(name):
    product = db["product"]
    return product.find({"name": name})


def getProductByCategory(category):
    product = db["product"]
    return product.aggregate(
        [
            {
                "$lookup": {
                    "from": "productType",
                    "localField": "typeId",
                    "foreignField": "id",
                    "as": "type",
                }
            },
            {"$unwind": "$type"},
        ]
    )


def getProductByDressmarker(dressmarker):
    product = db["product"]
    return product.find({"dressMarkerName": dressmarker})
