import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

# refactor to use connect() for final version
def dbExecuteWrapper(query_string, extra=None):
    DB = connect()
    c = DB.cursor()
    c.execute(query_string, extra)
    DB.commit()
    DB.close()


def dbExecuteRetrievalWrapper_allrows(query_string):
    DB = connect()
    c = DB.cursor()
    c.execute(query_string)
    rows = c.fetchall()
    return rows
    DB.close()


# refactor all queries into a variable that is then passed to execute
def deleteMatches():
    query = """DELETE FROM matches;"""
    dbExecuteWrapper(query)


def deletePlayers():
    query = """DELETE FROM players;"""
    dbExecuteWrapper(query)


def countPlayers():
    DB = connect()
    c = DB.cursor()
    query = "SELECT count(*) FROM players;"
    c.execute(query)
    row = c.fetchone()
    row_item = list(row)
    return int(row_item[0])
    DB.close()


def registerPlayer(name):
    query = ("INSERT INTO players (player_name, wins, matches)"
             "VALUES (%s, %s, %s);")
    dbExecuteWrapper(query, (name, 0, 0))


# Some kind of problem using _allrows with multiline string formatting
def playerStandings():
    query = ("SELECT id, player_name, wins, matches "
             "FROM players ORDER BY wins DESC;")
    return dbExecuteRetrievalWrapper_allrows(query)


def reportMatch(winner, loser):
    query1 = ("INSERT INTO matches VALUES (%s, %s) ;")
    query2 = ("UPDATE players SET wins = wins + 1"
              "FROM matches WHERE players.id = (%s) ;")
    query3 = ("UPDATE players SET matches = matches + 1"
              "FROM matches WHERE players.id = (%s) OR players.id = (%s);")
    dbExecuteWrapper(query1, (winner, loser))
    dbExecuteWrapper(query2, (winner,))
    dbExecuteWrapper(query3, (winner, loser))


def swissPairings():
    query = ("SELECT a.id, a.player_name, b.id, b.player_name "
             "FROM players as a, players as b "
             "WHERE a.wins = b.wins "
             "AND a.player_name != b.player_name "
             "AND a.id < b.id")
    return dbExecuteRetrievalWrapper_allrows(query)
