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
	Player_Name varchar(255),
	Wins int DEFAULT 0,
	Matches int DEFAULT 0
);