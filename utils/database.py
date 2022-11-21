from motor import motor_asyncio

from config import load_config

config = load_config()


class MongoDB:
    def __init__(self):
        _url = "mongodb://{}:{}@{}:{}".format(config.db.username, config.db.password, config.db.host, config.db.port)
        # _url = "mongodb://localhost:27017"
        self.client = motor_asyncio.AsyncIOMotorClient(_url)
        self.db = self.client[config.db.database]

    async def add_some_data(self):
        self.db.test.insert_one({"name": "test"})
