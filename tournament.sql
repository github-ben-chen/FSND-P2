-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;

CREATE table players (
    player_id    SERIAL PRIMARY     KEY,
    player_name  VARCHAR(40),
	winnings    INTEGER DEFAULT 0
);

CREATE table matches (
    match_id     SERIAL,
	loser_id     INTEGER REFERENCES players(player_id),
	winner_id    INTEGER REFERENCES players(player_id),
	PRIMARY     KEY(match_id)
);