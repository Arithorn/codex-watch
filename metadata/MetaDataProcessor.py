import json
import time
from hardcover import HardCover


class MetaDataProcessor:
    def __init__(self):
        self.handlers = {
            'author': self.handle_author,
            'book': self.handle_book,
            'series': self.handle_series
        }

    def process(self, message_body):
        try:
            message = json.loads(message_body)
            message_type = message.get('type')
            if handler := self.handlers.get(message_type):
                return handler(message)
            else:
                return self.handle_unknown_type(message)
            time.sleep(2)
        except json.JSONDecodeError:
            return self.handle_invalid_message(message_body)

    def handle_author(self, message):
        # Todo
        print(f"Handling Author Message {message}")
        hardcover = HardCover()
        print(f"Searching for author : {message.get('id')}")
        hardcover.getBooksByAuthor(authorId=message.get('id'))

        pass

    def handle_book(self, message):
        # Todo
        print(f"Handling Book Message {message}")
        pass

    def handle_series(self, message):
        print(f"Handling Series Message {message}")
        # Todo
        pass

    def handle_unknown_type(self, message):
        print(f"Not Handling Unknown Message {message}")
        # Todo
        pass

    def handle_invalid_message(self, raw_message):
        print(f"This Message is invalid {raw_message}")
        # Todo
        pass
