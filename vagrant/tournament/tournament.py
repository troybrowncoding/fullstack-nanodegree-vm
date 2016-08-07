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
    QUERY = "DELETE FROM Matches;"
    c.execute(QUERY)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    QUERY = "DELETE FROM Players;"
    c.execute(QUERY)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    QUERY = "SELECT COUNT(PlayerID) FROM Players;"
    c.execute(QUERY)
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
    QUERY = "INSERT INTO Players (Player_Name) VALUES (%s)"
    c.execute(QUERY, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
        A list of tuples, each of which contains (id, name, wins, matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    QUERY = "SELECT * FROM Standings ORDER BY Wins DESC;"
    c.execute(QUERY)
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
    # Add row to Matches table with winner and loser
    QUERY = "INSERT INTO Matches (winner, loser) VALUES (%s, %s);"
    c.execute(QUERY, (winner, loser))
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player
    adjacent to him or her in the standings.

    Returns:
        A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
    """
    players = countPlayers()
    standings = playerStandings() # Order Players by Wins
    pairings = []
    i = 0
    paired = 1 # Keeps track of whether a pair tuple is complete

    while i < players:
        if paired:
            # Create first half of pairing tuple
            first = (standings[i][0], standings[i][1])
            i = i + 1
            paired = 0 # Indicate that a pair is incomplete
        else:
            # Create second half of pairing tuple
            second = (standings[i][0], standings[i][1])
            # Join the halves and add the pair to the list of pairings
            pair = first + second
            pairings.append(pair)
            i = i + 1
            paired = 1 # Indicate that a pair is complete
    return pairings
