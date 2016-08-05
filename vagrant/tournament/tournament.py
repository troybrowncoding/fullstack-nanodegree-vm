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
    conn = connect()
    c = conn.cursor()
    #c.execute("DELETE FROM Matches;")
    c.execute("UPDATE Players SET Wins = 0, Matches = 0;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM Players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(PlayerID) FROM Players;")
    count = c.fetchone()
    conn.close()
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO Players (Player_Name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()


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
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM Players ORDER BY Wins DESC;")
    standings = c.fetchall()
    conn.commit()
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM Players WHERE PlayerID = %s", (winner,))
    player = c.fetchone()
    newwins = player[2]
    newwins = newwins + 1
    newmatches = player[3]
    newmatches = newmatches + 1
    c.execute("UPDATE Players SET Wins = %s, Matches = %s WHERE PlayerID = %s", (newwins, newmatches,winner))

    c.execute("SELECT * FROM Players WHERE PlayerID = %s", (loser,))
    player = c.fetchone()
    newmatches = player[3]
    newmatches = newmatches + 1
    c.execute("UPDATE Players SET Matches = %s WHERE PlayerID = %s", (newmatches,loser))
    
    conn.commit()
    conn.close()
 
 
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
    players = countPlayers()
    standings = playerStandings()
    pairings = []
    i = 0
    paired = 1

    while i < players:
        if paired:
            first = (standings[i][0], standings[i][1])
            i = i + 1
            paired = 0
        else:
            second = (standings[i][0], standings[i][1])
            pair = first + second
            pairings.append(pair)
            i = i + 1
            paired = 1
    return pairings