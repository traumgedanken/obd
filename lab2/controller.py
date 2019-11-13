from consolemenu import SelectionMenu

import model
import view


def show():
    __show_start_menu()


def __process_single_input(tname, msg):
    print(msg)
    print('(use format <attribute>=<value>)')
    print(f'({"/".join(model.TABLES[tname])})', end='\n\n')

    while True:
        data = input()
        if not data or data.count('=') != 1:
            print('Invalid input, try one more time')
            continue

        data = data.split('=')
        col, val = data[0].strip(), data[1].strip()
        if col.lower() in [tcol.lower() for tcol in model.TABLES[tname]]:
            return col, val
        else:
            print(f'Invalid column name "{col}" for table "{tname}"')


def __process_multiple_input(tname, msg):
    print(msg)
    print('(use format <attribute>=<value>)')
    print(f'({"/".join(model.TABLES[tname])})', end='\n\n')

    res = {}
    while True:
        data = input()
        if not data:
            break
        if data.count('=') != 1:
            print('Invalid input')
            continue

        data = data.split('=')
        col, val = data[0].strip(), data[1].strip()
        if col.lower() in [tcol.lower() for tcol in model.TABLES[tname]]:
            res[col] = val
        else:
            print(f'Invalid column name "{col}" for table "{tname}"')
            
    if not res:
        raise Exception('You entered nothing')
    return res


def __press_enter():
    input()


def __show_start_menu(*args):
    tables = list(model.TABLES.keys())

    menu = SelectionMenu(tables, "Select a table to work with:")
    menu.show()

    try:
        tname = tables[menu.selected_option]
        __show_table_menu(tname)
    except IndexError:
        print('Bye! Have a nice day!')


def __show_table_menu(tname, subtitle=''):
    menu = SelectionMenu(
        ['Get all', 'Get by atrribute', 'Insert', 'Update', 'Delete'],
        f'Selected table "{tname}"', exit_option_text='Go back',
        subtitle=subtitle)
    menu.show()

    index = menu.selected_option
    steps = [__get_all, __get_by_attr, __insert,
             __update, __delete, __show_start_menu]
    steps[index](tname)


def __get_all(tname):
    try:
        entities = model.get(tname)
        view.print_entities(tname, entities)
        __press_enter()
        __show_table_menu(tname)
    except Exception as e:
        __show_table_menu(tname, str(e))


def __get_by_attr(tname):
    try:
        query = __process_multiple_input(tname, 'Enter requested fields:')
        entities = model.get(tname, query)
        view.print_entities(tname, entities)
        __press_enter()
        __show_table_menu(tname)
    except Exception as e:
        __show_table_menu(tname, str(e))


def __insert(tname):
    try:
        data = __process_multiple_input(tname, 'Enter new fields values:')
        model.insert(tname, data)
        __show_table_menu(tname, 'Insertion was made successfully')
    except Exception as e:
        __show_table_menu(tname, str(e))


def __update(tname):
    try:
        condition = __process_single_input(
            tname, 'Enter requirement of row to be changed:')
        query = __process_multiple_input(tname, 'Enter new fields values:')

        model.update(tname, condition, query)
        __show_table_menu(tname, 'Update was made successfully')
    except Exception as e:
        __show_table_menu(tname, str(e))


def __delete(tname):
    try:
        query = __process_multiple_input(
            tname, 'Enter requirement of row to be deleted:')

        model.delete(tname, query)
        __show_table_menu(tname, 'Deletion was made successfully')
    except Exception as e:
        __show_table_menu(tname, str(e))
