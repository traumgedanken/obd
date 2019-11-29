import model


def single_input(colname=None, msg=None):
    if msg:
        print(msg)
    if colname:
        print(f'{colname}=', end='')
    return input()


def single_input(tname, msg):
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


def multiple_input(tname, msg, empty=False):
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
        if empty:
            return {}
        raise Exception('You entered nothing')
    return res


def press_enter():
    input()
