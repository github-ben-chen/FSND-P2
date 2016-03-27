#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM matches;"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM players;"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    query1 = "SELECT count(*) FROM players;"
    c.execute(query1)
    db.commit()
    result = c.fetchall()[0][0]
    db.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c  = db.cursor()
    c.execute("INSERT INTO players (player_name, winnings) VALUES (%s, %s);", (name,0))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c  = db.cursor()
    query = '''SELECT players.player_id, players.player_name,players.winnings, count (matches.match_id) 
               FROM Players LEFT JOIN Matches 
               on players.player_id = matches.winner_id or players.player_id = matches.loser_id  
               Group BY players.player_id Order BY players.winnings
            '''
    c.execute(query)
    db.commit()
    rows = c.fetchall()
    db.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c  = db.cursor()
    c.execute("SELECT * FROM players ORDER BY players.winnings")
    c.execute("UPDATE players SET winnings = winnings+1 where player_id =(%s);",(winner,))
    db.commit()
    c.execute("SELECT * FROM players ORDER BY players.winnings")
    db.commit()
    c.execute("INSERT INTO matches (loser_id, winner_id) VALUES (%s,%s);",(loser,winner))
    db.commit()
    db.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c  = db.cursor()
    query = "SELECT player_id,player_name FROM players ORDER BY winnings"
    c.execute(query)
    rows = c.fetchall()
    numPair = len(rows)
    if numPair%2 != 0:
        print "Can't do swiss pariing with odd number of players!"
        return
    swissPair =[]
    for x in range(0,numPair/2):
        thistuple = (rows[2*x][0],rows[2*x][1],rows[2*x+1][0],rows[2*x+1][1])
        swissPair.append(thistuple)

    return swissPair