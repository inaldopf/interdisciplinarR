from .__init__ import r
from mongo.main import ActualMongosCart


def setCart(cpf):
    # pega do mongo o joga no redis
    r.delete(f"Cart:{cpf}")
    cartM = ActualMongosCart(cpf)
    FinalValue = cartM["FinalValue"]
    if len(r.hgetall(f"Cart:{cpf}").items()) <= 0 and len(cartM) > 0:
        for cart in cartM["cart"]:

            cart["_id"] = str(cart["_id"])

            cart["item"]["id"] = cart["id"]
            r.hset(f"Cart:{cpf}", mapping=cart["item"])

            r.expire(f"Cart:{cpf}", 3600)

        r.hset(f"Cart:{cpf}", "Total", str(round(FinalValue, 2)))
    response = r.hgetall(f"Cart:{cpf}").items()
    response = list(response)

    return response


def getCart(cpf):
    response = r.hgetall(f"Cart:{cpf}").items()
    response = list(response)
    return response


def updateCart(cpf, produto, quantidade, price):
    cart = setCart(cpf)
    r.hincrby(f"Cart:{cpf}", produto, quantidade)
    result = float(price) * float(quantidade)
    r.hincrbyfloat(f"Cart:{cpf}", "Total", round(result, 2))
    r.expire(f"Cart:{cpf}", 3600)
    cart = getCart(cpf)
    return cart
