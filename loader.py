from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from chatterbot import ChatBot


from config import load_config
from utils.database import MongoDB

config = load_config()
bot = Bot(token=config.bot.token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = MongoDB()
bot = ChatBot(
    name='RL AIOGram chatbot',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb://localhost:27017/chatterbot-database',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        },
    ],
)