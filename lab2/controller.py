from consolemenu import SelectionMenu

from config import TABLES
import model
import view

class Menu:
    def show(self):
        self._show_start_menu()

    def _show_start_menu(self, *args):
        tables = list(TABLES.keys())

        menu = SelectionMenu(tables, "Select a table to work with:")
        menu.show()

        try:
            tname = tables[menu.selected_option]
            self._show_table_menu(tname)
        except IndexError:
            print('Good bye!')

    def _show_table_menu(self, tname):
        menu = SelectionMenu(
            ['Get all', 'Get by atrribute', 'Update', 'Delete'],
            f'Selected table "{tname}"', exit_option_text='Go back',)
        menu.show()

        index = menu.selected_option
        steps = [self._get_all, self._get_one, self._update,
                 self._delete, self._show_start_menu]
        steps[index](tname)

    def _get_all(self, tname):
        entities = model.get(tname)
        view.print_entities(tname, entities)
        input()
        self._show_table_menu(tname)

    def _get_one(self):
        pass

    def _update(self):
        pass

    def _delete(self):
        pass


Menu().show()
