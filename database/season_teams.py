# Import the necessary libraries
import psycopg2
import csv
import pandas as pd
import pandas.io.sql as sqlio
from sqlalchemy import create_engine

# The external url of the database
db_url = "postgresql://admin:JVDdki5JwDKlAtHsFAdxL58tO9qQZh5j@dpg-crhvmi5umphs73cag3i0-a.frankfurt-postgres.render.com/football_p8l0"

# Connect to the database
conn = psycopg2.connect(db_url)

cur = conn.cursor()

# Create the table season_teams
cur.execute("""
            CREATE TABLE season_teams(
                country_id integer NOT NULL,
                league_id integer NOT NULL,
                name varchar,
                id integer PRIMARY KEY,
                home_shots_on_target integer,
                away_shots_on_target integer,
                home_wins_streak integer,
                away_wins_streak integer,
                home_losses_streak integer,
                away_losses_streak integer,
                home_goals integer,
                away_goals integer,
                last_10_home_wins integer,
                last_10_away_wins integer,    
                FOREIGN KEY (country_id) REFERENCES countries (id),
                FOREIGN KEY (league_id) REFERENCES leagues (id),
                FOREIGN KEY (id) REFERENCES teams (id));
            """)

conn.commit()

# Insert the data into the table season_teams
with open("database/csv_files/season_table.csv") as file:
    teams_stats = csv.reader(file)
    teams_stats = [(1, 1, *row) for row in teams_stats]
    cur.executemany("""
                    INSERT INTO season_teams(
                        country_id,
                        league_id,
                        name,
                        id,
                        home_shots_on_target,
                        away_shots_on_target,
                        home_wins_streak,
                        away_wins_streak,
                        home_losses_streak,
                        away_losses_streak,
                        home_goals,
                        away_goals,
                        last_10_home_wins,
                        last_10_away_wins)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, teams_stats)
    conn.commit()
