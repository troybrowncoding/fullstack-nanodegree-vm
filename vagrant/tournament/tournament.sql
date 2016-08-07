-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE Players
(
	PlayerID serial PRIMARY KEY,
	Player_Name varchar(255)
--	Wins int DEFAULT 0,
--	Matches int DEFAULT 0
);

CREATE TABLE Matches
(
	MatchID serial PRIMARY KEY,
	winner int references Players(PlayerID),
	loser int references Players(PlayerID)
);

CREATE VIEW Wins AS
	SELECT Players.PlayerID, Count(Matches.loser) AS num
	FROM Players
	LEFT JOIN (SELECT * FROM Matches) AS Matches
	ON Players.PlayerID = Matches.winner
	GROUP BY Players.PlayerID;

CREATE VIEW Played AS
	SELECT Players.PlayerID, Count(Matches.loser) AS num 
	FROM Players
	LEFT JOIN (SELECT * FROM Matches) AS Matches
	ON Players.PlayerID = Matches.winner
	OR Players.PlayerID = Matches.loser
	GROUP BY Players.PlayerID;

CREATE VIEW Standings AS
	SELECT Players.PlayerID, Players.Player_Name, Wins.num
	AS wins, Played.num AS matches 
	FROM Players, Wins, Played
	WHERE Players.PlayerID = Wins.PlayerID
	AND Wins.PlayerID = Played.PlayerID;
	