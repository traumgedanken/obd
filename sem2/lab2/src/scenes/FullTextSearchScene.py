from prompt_toolkit.validation import Validator, ValidationError

from src import constants, Message
from src.scenes.BaseScene import BaseScene
from src.scenes.FoundMessagesViewerScene import FoundMessagesViewerScene


class QueryValidator(Validator):
    def validate(self, document):
        if not len(str(document.text).strip()):
            raise ValidationError(
                message='Query cannot be empty',
                cursor_position=len(document.text))  # Move cursor to end


class FullTextSearchScene(BaseScene):
    def __init__(self, session, redis):
        super().__init__([
            {
                'type': 'input',
                'name': 'query',
                'message': 'Your query',
                'validate': QueryValidator
            }
        ])
        self.redis = redis
        self.chat = session['chat']
        self.thread = None
        self.session = session

    def enter(self):
        query = self.ask().get('query').lower()
        keys = {'%s:%s' % (constants.WORDS_STORAGE, word)
                for word in query.split()}
        results = self.redis.sinter(keys)
        messages = [Message.load(key, self.redis)
                    for key in results]
        FoundMessagesViewerScene(query, messages).enter()
