from consolemenu import SelectionMenu

import model
import view


def show():
    __show_start_menu()


def __process_specified_input(colname=None, msg=None):
    if msg:
        print(msg)
    if colname:
        print(f'{colname}=', end='')
    return input()


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


def __show_start_menu(tname='', err=''):
    tables = list(model.TABLES.keys())

    menu = SelectionMenu(tables + ['Custom SQL query'], subtitle=err,
                         title="Select a table to work with:")
    menu.show()

    index = menu.selected_option
    if index < len(tables):
        tname = tables[index]
        __show_table_menu(tname)
    elif index == len(tables):
        __custom()
    else:
        print('Bye! Have a nice day!')


def __show_table_menu(tname, subtitle=''):
    opts = ['Get all', 'Get by atrribute', 'Insert', 'Update', 'Delete']
    steps = [__get_all, __get_by_attr, __insert,
             __update, __delete]

    if tname == 'Game':
        opts += ['Get games by stadium has cover',
                 'Full text search in game document']
        steps += [__get_games_hascover, __fts]
    elif tname == 'Team':
        opts += ['Get teams by sport type', 'Create 10_000 random teams']
        steps += [__get_team_sporttype, __random_team]
    steps += [__show_start_menu]

    menu = SelectionMenu(
        opts, subtitle=subtitle,
        title=f'Selected table "{tname}"', exit_option_text='Go back',)
    menu.show()
    index = menu.selected_option
    steps[index](tname=tname)


def __get_all(tname):
    try:
        data = model.get(tname)
        view.print_entities(tname, data)
        __press_enter()
        __show_table_menu(tname)
    except Exception as e:
        __show_table_menu(tname, str(e))


def __get_by_attr(tname):
    try:
        query = __process_multiple_input(tname, 'Enter requested fields:')
        data = model.get(tname, query)
        view.print_entities(tname, data)
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


def __get_games_hascover(tname):
    try:
        query = __process_specified_input(
            'hasCover', 'Enter hasCover value:'
        ).lower() in ['true', 't', 'yes', 'y', '+']
        data = model.get_games_by_stadium_hascover(query)
        view.print_entities(f'Games with hasCover={query}', data)
        __press_enter()
        __show_table_menu(tname)
    except Exception as e:
        __show_table_menu(tname, str(e))


def __get_team_sporttype(tname):
    try:
        types = []
        query = __process_specified_input(
            msg='Enter your queries for sportype:').lower()
        while query:
            types.append(query)
            query = __process_specified_input().lower()

        data = model.get_teams_by_sporttype(types)
        view.print_entities(
            f'Teams which played at least one of this games: {types}', data)
        __press_enter()
        __show_table_menu(tname)
    except Exception as e:
        __show_table_menu(tname, str(e))


def __fts(tname):
    try:
        query = __process_specified_input(
            'query', 'Enter your query to search in document:')
        contains = __process_specified_input(
            msg='Query word shoul be in document?'
        ).lower() in ['true', 't', 'yes', 'y', '+']
        data = model.fts(query, contains)
        view.print_entities(
            f'Documents corresponding to query={query} ({"" if contains else "not "}contains)', data)
        __press_enter()
        __show_table_menu(tname)
    except Exception as e:
        __show_table_menu(tname, str(e))


def __random_team(tname):
    try:
        model.random_teams()
        __show_table_menu(tname, '10_000 random teams were successfully added')
    except Exception as e:
        __show_table_menu(tname, str(e))


def __custom():
    try:
        sql = __process_specified_input(msg='Enter your SQL query')
        data = model.execute(sql)
        view.print_entities('Custom query result', data)
        __press_enter()
        __show_start_menu()
    except Exception as e:
        __show_start_menu(err=str(e))
