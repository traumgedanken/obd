from consolemenu import SelectionMenu

import model
import view
import reader


def handle_error(func):
    def wrapper(tname):
        try:
            func(tname)
        except Exception as e:
            show_table_menu(tname, str(e))

    return wrapper


def show_start_menu(tname='', err=''):
    tables = list(model.TABLES.keys())

    menu = SelectionMenu(tables, subtitle=err,
                         title="Select a table to work with:")
    menu.show()

    index = menu.selected_option
    if index < len(tables):
        tname = tables[index]
        show_table_menu(tname)
    else:
        print('Bye! Have a nice day!')


def show_table_menu(tname, subtitle=''):
    opts = ['Get', 'Insert', 'Update', 'Delete']
    steps = [get, insert, update, delete, show_start_menu]

    menu = SelectionMenu(
        opts, subtitle=subtitle,
        title=f'Selected table "{tname}"', exit_option_text='Go back', )
    menu.show()
    index = menu.selected_option
    steps[index](tname=tname)


@handle_error
def get(tname):
    query = reader.multiple_input(tname, 'Enter requested fields:', empty=True)
    data = model.get(tname, query)
    view.print_entities(tname, data)
    reader.press_enter()
    show_table_menu(tname)


@handle_error
def insert(tname):
    data = reader.multiple_input(tname, 'Enter new fields values:')
    model.insert(tname, data)
    show_table_menu(tname, 'Insertion was made successfully')


@handle_error
def update(tname):
    condition = reader.single_input(
        tname, 'Enter requirement of row to be changed:')
    query = reader.multiple_input(tname, 'Enter new fields values:')

    model.update(tname, condition, query)
    show_table_menu(tname, 'Update was made successfully')


@handle_error
def delete(tname):
    query = reader.multiple_input(
        tname, 'Enter requirement of row to be deleted:')

    model.delete(tname, query)
    show_table_menu(tname, 'Deletion was made successfully')

