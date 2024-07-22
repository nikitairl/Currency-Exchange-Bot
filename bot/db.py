from redis import Redis

REDIS_CLIENT = Redis(host="redis", port=6379, decode_responses=True)
