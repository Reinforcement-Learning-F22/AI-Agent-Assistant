import bson
from motor import motor_asyncio

from config import load_config

config = load_config()


class MongoDB:
    def __init__(self):
        # _url = "mongodb://{}:{}@{}:{}".format(config.db.username, config.db.password, config.db.host, config.db.port)
        _url = "mongodb://localhost:27017"
        self.client = motor_asyncio.AsyncIOMotorClient(_url)
        self.url = f'{_url}/{config.db.database}'
        self.db = self.client[config.db.database]

    async def add_some_data(self):
        self.db.test.insert_one({"name": "test"})

    # adding user message text and return id
    async def add_user_message(self, user_id, message_text):
        return await self.db.user_messages.insert_one({"user_id": user_id, "message_text": message_text})

    # getting user message text by id
    async def get_user_message(self, message_id):
        return await self.db.user_messages.find_one({"_id": bson.ObjectId(message_id)})
