from chatterbot.trainers import ChatterBotCorpusTrainer

from loader import chatbot

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)
