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

    menu = SelectionMenu(tables + ['Custom SQL query'], subtitle=err,
                         title="Select a table to work with:")
    menu.show()

    index = menu.selected_option
    if index < len(tables):
        tname = tables[index]
        show_table_menu(tname)
    elif index == len(tables):
        custom_query()
    else:
        print('Bye! Have a nice day!')


def show_table_menu(tname, subtitle=''):
    opts = ['Get all', 'Get by atrribute', 'Insert', 'Update', 'Delete']
    steps = [get_all, get_by_attr, insert,
             update, delete]

    if tname == 'Game':
        opts += ['Get games by stadium has cover',
                 'Full text search in game document']
        steps += [get_games_hascover, fts]
    elif tname == 'Team':
        opts += ['Get teams by sport type', 'Create 10_000 random teams']
        steps += [get_team_sporttype, create_random_team]
    steps += [show_start_menu]

    menu = SelectionMenu(
        opts, subtitle=subtitle,
        title=f'Selected table "{tname}"', exit_option_text='Go back',)
    menu.show()
    index = menu.selected_option
    steps[index](tname=tname)


@handle_error
def get_all(tname):
    data = model.get(tname)
    view.print_entities(tname, data)
    reader.press_enter()
    show_table_menu(tname)


@handle_error
def get_by_attr(tname):
    query = reader.multiple_input(tname, 'Enter requested fields:')
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


@handle_error
def get_games_hascover(tname):
    query = reader.specified_input(
        'hasCover', 'Enter hasCover value:'
    ).lower() in ['true', 't', 'yes', 'y', '+']
    data = model.get_games_by_stadium_hascover(query)
    view.print_entities(f'Games with hasCover={query}', data)
    reader.press_enter()
    show_table_menu(tname)


@handle_error
def get_team_sporttype(tname):
    types = []
    query = reader.specified_input(
        msg='Enter your queries for sportype:').lower()
    while query:
        types.append(query)
        query = reader.specified_input().lower()

    data = model.get_teams_by_sporttype(types)
    view.print_entities(
        f'Teams which played at least one of this games: {types}', data)
    reader.press_enter()
    show_table_menu(tname)


@handle_error
def fts(tname):
    query = reader.specified_input(
        'query', 'Enter your query to search in document:')
    contains = reader.specified_input(
        msg='Query word shoul be in document?'
    ).lower() in ['true', 't', 'yes', 'y', '+']
    data = model.fts(query, contains)
    view.print_entities(
        f'Documents corresponding to query={query} ({"" if contains else "not "}contains)', data)
    reader.press_enter()
    show_table_menu(tname)


@handle_error
def create_random_team(tname):
    model.create_random_teams()
    show_table_menu(tname, '10_000 random teams were successfully added')


def custom_query():
    try:
        sql = reader.multiline_input('Enter your SQL query')
        data = model.execute(sql)
        view.print_entities('Custom query result', data)
        reader.press_enter()
        show_start_menu()
    except Exception as e:
        show_start_menu(err=str(e))
