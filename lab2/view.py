from model import TABLES

COLUMN_W = 30


def print_entities(tname, entities):
    separator_line = '-' * COLUMN_W * len(TABLES[tname])

    print(f'Working with table "{tname}"', end='\n\n')
    print(separator_line)
    print(''.join([f'{col}     |'.rjust(30, ' ') for col in TABLES[tname]]))
    print(separator_line)

    for entity in entities:
        print(''.join([f'{col}     |'.rjust(30, ' ') for col in entity]))
    print(separator_line)
