class RedisConn():
    def __init__(self, redis_host, redis_port, redis_password, redis_db):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.redis_db = redis_db

    def conn(self):
        return redis.StrictRedis(host=self.redis_host, port=self.redis_port, password=self.redis_password, db=self.redis_db)
