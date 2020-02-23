COLUMN_WIDTH = 30


def print_entities(tname, data):
    entities, cols = data

    separator_line = '-' * COLUMN_WIDTH * len(cols)

    print(f'Working with table "{tname}"', end='\n\n')
    print(separator_line)
    print(''.join([f'{col}     |'.rjust(30, ' ') for col in cols]))
    print(separator_line)

    for entity in entities:
        print(''.join([f'{col}     |'.rjust(30, ' ') for col in entity]))
    print(separator_line)
