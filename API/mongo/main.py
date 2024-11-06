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
    if product.find_one({"name": name}) is None:
        status = product.insert_one(
            {
                "id": Proxid,
                "name": name,
                "price": price,
                "imageUrl": imageurl,
                "category": typeId,
                "id_dressmaker": dressmarker,
                "avaliation": avaliation,
                "description": description,
                "size": size,
            }
        ).inserted_id
    else:
        status = "Product already exists"
    return status


def editProduct(
    id,
    name: None | str,
    price: None | float,
    imageurl: None | str,
    typeId: None | int,
    dressmarker: None | str,
    avaliation: None | float,
    description: None | str,
    size: None | str,
):
    infos = {}
    product = db["product"]
    if name is not None:
        infos["name"] = name
    if price is not None:
        infos["price"] = price
    if imageurl is not None:
        infos["imageUrl"] = imageurl
    if typeId is not None:
        infos["typeId"] = typeId
    if dressmarker is not None:
        infos["dressMarkerName"] = dressmarker
    if avaliation is not None:
        infos["avaliation"] = avaliation
    if description is not None:
        infos["description"] = description
    if size is not None:
        infos["size"] = size
    status = product.update_one({"id": id}, infos).upserted_ids()
    return status


def getCategorys():
    category = db["productType"]
    categorys = category.find({})
    categoryList = []
    for i in categorys:
        categoryList.append(i)
    return categoryList


def deleteProduct(id):
    product = db["product"]
    status = product.delete_one({"id": id}).deleted_count
    return status


def getProductByName(name):
    product = db["product"]
    return product.find({"name": name})


def getProductByCategory(category):
    product = db["product"]
    print(str(category).capitalize())
    return product.aggregate(
        [
            {
                "$lookup": {
                    "from": "productType",
                    "localField": "category",
                    "foreignField": "id",
                    "as": "types",
                }
            },
            {"$unwind": "$types"},
            {"$match": {"types.category": str(category).capitalize()}},
        ]
    )


def getHistory(cpf):
    order = db["order"]
    if cpf == "1":
        response = order.find({})
    else:
        response = order.find({"userCpf": cpf})
    return response


def getOrderByCpf(cpf):
    order = db["order"]
    response = order.aggregate(
        [
            {
                "$lookup": {
                    "from": "cart",
                    "localField": "cart_id",
                    "foreignField": "id",
                    "as": "cart",
                }
            },
            {"$match": {"userCpf": cpf}},
        ]
    )
    return response


def ActualMongosCart(cpf):
    order = db["order"]
    try:
        response = order.aggregate(
            [
                {
                    "$lookup": {
                        "from": "cart",
                        "localField": "cart_id",
                        "foreignField": "id",
                        "as": "cart",
                    }
                },
                {"$match": {"userCpf": cpf, "status": "Pendente"}},
                {"$project": {"_id": 0, "userCpf": 1, "cart": 1, "FinalValue": 1}},
            ]
        ).next()
    except StopIteration:
        response = []
    return response


def updateCartMongo(cpf, actualReidsCart):
    mongoCart = ActualMongosCart(cpf)
    cartId = mongoCart["cart"][0]["id"]
    cart = db["cart"]

    mongoCartActual = mongoCart["cart"][0]["item"]

    for item in actualReidsCart:
        if item not in mongoCartActual:
            print(item)
            cart.update_one({"id": cartId}, {"$set": {f"item.{item[0]}": int(item[1])}})


def getProductByDressmarker(dressmarker):
    product = db["product"]
    product = list(product.find({"dressMarkerName": dressmarker}))
    for item in product:
        item["_id"] = str(item["_id"])
    return product


def alterStatsus(cpf, status):
    order = db["order"]
    response = order.update_one(
        {"userCpf": cpf}, {"$set": {"status": status}}
    ).upserted_ids()
    return response


def addForms(body):
    forms = db["forms"]
    response = forms.insert_one(body).inserted_id
    return response


def getLastForms():
    forms = db["forms"]
    response = list(forms.find().sort("_id", -1).limit(1))
    return response


def createOrder(body):
    order = db["order"]
    cart = db["cart"]

    Proxid = order.find_one(sort=[("id", -1)])
    Proxid = Proxid["id"] + 1
    body["id"] = Proxid
    Proxid = cart.find_one(sort=[("id", -1)])
    Proxid = Proxid["id"] + 1
    body["cart_id"] = Proxid
    cartResponse = cart.insert_one({"id": Proxid, "item": {}})
    response = order.insert_one(body).inserted_id

    return response
