import json

from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

from loader import chatbot


async def base_train():
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english", "chatterbot.corpus.russian")
    trainer = ListTrainer(chatbot)
    for data in json.load(open('data/faq.json')):
        trainer.train([data['question'], data['answer']])
