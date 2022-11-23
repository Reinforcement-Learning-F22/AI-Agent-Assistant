from environs import Env
from pydantic import BaseModel


class Bot(BaseModel):
    """
    Bot configuration
    """
    token: str
    admins: list
    name: str
    storage_adapter: str


class Database(BaseModel):
    """
    Database configuration
    """
    host: str
    port: int
    username: str = None
    password: str = None
    database: str


class Config(BaseModel):
    """
    Configuration model
    """
    bot: Bot
    db: Database = None


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        bot=Bot(
            token=env.str("BOT_TOKEN"),
            admins=env.list("ADMINS"),
            name=env.str("BOT_NAME"),
            storage_adapter=env.str("STORAGE_ADAPTER"),
            logic_adapters=[
                {
                    'import_path': env.str("LOGIC_ADAPTER"),
                    'default_response': 'I am sorry, but I do not understand.',
                    'maximum_similarity_threshold': 0.90
                },
            ],
        ),
        db=Database(
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
            username=env.str("DB_USERNAME"),
            password=env.str("DB_PASSWORD"),
            database=env.str("DB_DATABASE"),
        ),
    )
