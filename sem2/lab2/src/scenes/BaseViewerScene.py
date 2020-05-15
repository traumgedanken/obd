from .BaseScene import BaseScene
import math
import abc

BACK = '⬅️ prev page'
NEXT = '➡️ next page'
EXIT = '◀️ return'


class BaseViewerScene(BaseScene):
    def __init__(self, items_per_page=25):
        super().__init__([
            {
                'type': 'list',
                'name': 'action',
                'message': 'Navigation',
                'choices': [NEXT, BACK, EXIT]
            }
        ])
        self.items_per_page = items_per_page
        self.cursor = 0

    def load(self):
        items = self.fetch(self.cursor, self.cursor + self.items_per_page)
        if not len(items):
            return []
        else:
            return items

    @abc.abstractmethod
    def fetch(self, start, end):
        pass

    @abc.abstractmethod
    def items_count(self):
        pass

    def next_page(self):
        self.cursor += self.items_per_page
        if self.cursor > self.items_count():
            self.cursor = 0

    def prev_page(self):
        self.cursor -= self.items_per_page
        if self.cursor < 0:
            self.cursor = 0

    def print_page(self):
        print('Page: %i' % math.ceil(self.cursor // self.items_per_page))
        print('Total: %i' % self.items_count())
        print('\n'.join(self.load()))
        answers = self.ask()
        action = answers['action']
        if action == NEXT:
            self.next_page()
        elif action == BACK:
            self.prev_page()
        else:
            raise StopIteration

    def enter(self):
        while True:
            try:
                self.print_page()
            except StopIteration:
                return
