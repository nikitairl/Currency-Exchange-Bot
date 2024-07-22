from redis import Redis

REDIS_CLIENT = Redis(host="localhost", port=6379, db=0)
