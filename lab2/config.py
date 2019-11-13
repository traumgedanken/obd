TABLES = {
    'Game': ('id', 'ticketsold', 'sporttype', 'date'),
    'Stadium': ('id', 'country', 'seats', 'hascover'),
    'Team': ('id', 'price', 'country', 'name'),
    'Score': ('gamedid', 'teamid', 'points'),
    'Event': ('gameid', 'stadiumid')
}
