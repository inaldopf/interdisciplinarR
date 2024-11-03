from .__init__ import r
from mongo.main import ActualMongosCart


def setCart(cpf):
    # pega do mongo o joga no redis
    cartM = ActualMongosCart(cpf)
    if len(r.hgetall(f"Cart:{cpf}").items()) <= 0:
        for cart in cartM["cart"]:
            print(cart)
            cart["_id"] = str(cart["_id"])
            print(cart["item"])
            r.hset(f"Cart:{cpf}", mapping=cart["item"])
            r.expire(f"Cart:{cpf}", 3600)
    response = r.hgetall(f"Cart:{cpf}").items()
    response = list(response)

    return response


def getCart(cpf):
    response = r.hgetall(f"Cart:{cpf}").items()
    response = list(response)
    return response


def updateCart(cpf, produto, quantidade):
    cart = setCart(cpf)
    r.hincrby(f"Cart:{cpf}", produto, quantidade)
    r.expire(f"Cart:{cpf}", 3600)
    cart = getCart(cpf)
    return cart
