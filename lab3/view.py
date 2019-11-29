COLUMN_WIDTH = 30


def print_entities(tname, data):
    print(f'Working with table "{tname}"', end='\n\n')
    if not data:
        print('List is empty')
        return

    entities = data
    cols = data[0].__columns__
    separator_line = '-' * COLUMN_WIDTH * len(cols)

    print(separator_line)
    print(''.join([f'{col}     |'.rjust(30, ' ') for col in cols]))
    print(separator_line)

    for entity in entities:
        print(''.join([f'{getattr(entity, col)}     |'.rjust(30, ' ') for col in cols]))

    print(separator_line)
