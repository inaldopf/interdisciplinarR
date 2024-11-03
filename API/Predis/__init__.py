import redis
import ssl

ssl_context = ssl.create_default_context()

r = redis.Redis(
    # host="oregon-redis.render.com",
    # db=0,
    # username="red-csh4ud3tq21c73e3kb9g",
    # port=6379,
    # decode_responses=True,
    # password="9MjNV4Fq0uo7luykG7jJnd2qBL82gZcF",
    host="oregon-redis.render.com",
    username="red-csh4ud3tq21c73e3kb9g",
    password="9MjNV4Fq0uo7luykG7jJnd2qBL82gZcF",
    port=6379,
    ssl=True,
    decode_responses=True,
    ssl_ocsp_context=ssl_context,
)
