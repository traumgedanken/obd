from src.scenes.BaseViewerScene import BaseViewerScene


class FoundMessagesViewerScene(BaseViewerScene):
    def __init__(self, query, messages):
        super().__init__(items_per_page=5)
        self.query = query
        self.messages = [str(m) for m in messages]

    def items_count(self):
        return len(self.messages)

    def fetch(self, start, end):
        return self.messages[start:end]

    def print_page(self):
        print(f'Query: `{self.query}`')
        super().print_page()
