# Tournament Results
Creates and maintains a PostgreSQL database in a game tournament using the Swiss pair system.

## Files
* tournament.py -- Functions for running the tournament
* tournament.sql -- Creates database and defines tables
* tournament_test.py -- Test cases for tournament.py

## Usage
Create and connect to database.
```bash
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql
psql (9.3.13)
Type "help" for help.

vagrant=> \i tournament.sql
psql:tournament.sql:9: NOTICE:  database "tournament" does not exist, skipping
DROP DATABASE
CREATE DATABASE
You are now connected to database "tournament" as user "vagrant".
CREATE TABLE
tournament=> \q
```
Run unit tests.
```bash
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py
1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!
```

## Troubleshooting
Contact Troy at troybrowncoding@gmail.com if you have any issues or concerns.
