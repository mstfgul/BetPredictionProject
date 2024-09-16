# Impport the necessary libraries
import pandas as pd
import numpy as np
import csv
import datetime
import os

# This library allows us to connect to a PostgreSQL database
import psycopg2

# The external url of the database
db_url = "postgresql://admin:JVDdki5JwDKlAtHsFAdxL58tO9qQZh5j@dpg-crhvmi5umphs73cag3i0-a.frankfurt-postgres.render.com/football_p8l0"

# Connect to the database
conn = psycopg2.connect(db_url)

cur = conn.cursor()

# Create the table countries
cur.execute("""
            CREATE TABLE countries(
                id integer PRIMARY KEY,
                name varchar);
            """)

# Create the table leagues
cur.execute("""
            CREATE TABLE leagues(
                id integer PRIMARY KEY,
                country_id integer NOT NULL,
                name varchar,
                FOREIGN KEY (country_id) REFERENCES countries (id));
            """)

conn.commit()

# The list of countries
countries_list = tuple(enumerate(
    sorted(("England", "Germany", "Italy", "Spain", "France", "Belgium", "Netherlands")),
    start=1))

# Insert the countries into the table
cur.executemany("""
            INSERT INTO countries
            VALUES(%s, %s)
            """, countries_list)
conn.commit()

# Create a dictionnary with the leagues of each country
leagues_dictionnary = {"England": ["Premier League", "Championship"],
                       "Germany": ["Bundesliga 1", "Bundesliga 2"],
                       "Italy": ["Serie A", "Serie B"],
                       "Spain": ["La Liga Primera Division", "La Liga Segunda Division"],
                       "France": ["Le Championnat", "Division 2"],
                       "Belgium": ["Jupiler League"],
                       "Netherlands": ["Eredivisie"]}

# Create the list of leagues
country_league_list = []
for i, country in countries_list:
    for league in leagues_dictionnary[country]:
        country_league_list.append((i, league))

leagues_list = tuple((i, *item) for i, item in enumerate(country_league_list, start=1))

# Insert the leagues into the table
cur.executemany("""
            INSERT INTO leagues
            VALUES(%s, %s, %s)
            """, leagues_list)

conn.commit()

# Create the table teams
cur.execute("""
            CREATE TABLE teams(
                id integer PRIMARY KEY,
                country_id integer NOT NULL,
                name varchar,
                FOREIGN KEY (country_id) REFERENCES countries (id));
            """)

conn.commit()

# A list of urls to download the data
urls = [
    "https://www.football-data.co.uk/mmz4281/1011/B1.csv",
    "https://www.football-data.co.uk/mmz4281/1112/B1.csv",
    "https://www.football-data.co.uk/mmz4281/1213/B1.csv",
    "https://www.football-data.co.uk/mmz4281/1314/B1.csv",
    "https://www.football-data.co.uk/mmz4281/1415/B1.csv",
    "https://www.football-data.co.uk/mmz4281/1516/B1.csv",
    "https://www.football-data.co.uk/mmz4281/1617/B1.csv",
    "https://www.football-data.co.uk/mmz4281/1718/B1.csv",
    "https://www.football-data.co.uk/mmz4281/1819/B1.csv",
    "https://www.football-data.co.uk/mmz4281/1920/B1.csv",
    "https://www.football-data.co.uk/mmz4281/2021/B1.csv",
    "https://www.football-data.co.uk/mmz4281/2122/B1.csv",
    "https://www.football-data.co.uk/mmz4281/2223/B1.csv",
    "https://www.football-data.co.uk/mmz4281/2324/B1.csv",
    "https://www.football-data.co.uk/mmz4281/2425/B1.csv"
]

# Create the list of all the teams
teams_set = set()

for url in urls:
    df = pd.read_csv(url)
    teams_set = teams_set.union(set(df["HomeTeam"].dropna().unique()))

teams_list = tuple((i, 1, value) for i, value in enumerate(sorted(list(teams_set)), start=1))

# Insert the teams into the table
cur.executemany("""
            INSERT INTO teams
            VALUES(%s, %s, %s)
            """, teams_list)
conn.commit()

# Create the table matches
cur.execute("""
            CREATE TABLE matchs(
                id integer PRIMARY KEY,
                country_id integer NOT NULL,
                league_id integer NOT NULL,
                division varchar,
                season varchar,
                date date,
                time timestamp,
                home_team_id integer NOT NULL,
                away_team_id integer NOT NULL,
                home_team_goals integer,
                away_team_goals integer,
                result char(1),
                ht_home_team_goals integer,
                ht_away_team_goals integer,
                ht_result char(1),
                FOREIGN KEY (country_id) REFERENCES countries (id),
                FOREIGN KEY (league_id) REFERENCES leagues (id),
                FOREIGN KEY (home_team_id) REFERENCES teams (id),
                FOREIGN KEY (away_team_id) REFERENCES teams (id));
            """)

conn.commit()

# Create a csv file with the all the matches data
try:
    os.remove("database/csv_files/matchs.csv")
except:
    pass

teams_dict = {team: i for i, j, team in teams_list}

for url in urls:
    df = pd.read_csv(url)

    df = df.dropna(axis=0, how='all')

    df["country_id"] = 1
    df["league_id"] = 1
    df["season"] = url[-11:-9] + "/" + url[-9:-7]
    df["HomeTeam"] = df["HomeTeam"].map(teams_dict)
    df["AwayTeam"] = df["AwayTeam"].map(teams_dict)

    try:
        df['Time'] = pd.to_datetime(
            df["Date"] + '-' + df['Time'], dayfirst=True, utc=False)
    except:
        df['Time'] = np.nan

    df['Date'] = pd.to_datetime(df["Date"], format='mixed').dt.date

    df.to_csv("csv_files/matchs.csv", sep=',', header=False, index=False, mode='a',
              columns=["country_id",
                       "league_id",
                       "Div",
                       "season",
                       "Date",
                       "Time",
                       "HomeTeam",
                       "AwayTeam",
                       "FTHG",
                       "FTAG",
                       "FTR",
                       "HTHG",
                       "HTAG",
                       "HTR"])

# Insert the matches into the table
with open("database/csv_files/matchs.csv") as file:
    matchs_info = csv.reader(file)
    matchs_info = [
        tuple(None if field == ''
              else int(float(field)) if field.replace('.', '', 1).isdigit()
              else field for field in row) for row in matchs_info]
    matchs_info = [(i+1, *row) for i, row in enumerate(matchs_info)]
    cur.executemany("""
                    INSERT INTO matchs (id,
                                        country_id,
                                        league_id,
                                        division,
                                        season,
                                        date,
                                        time,
                                        home_team_id,
                                        away_team_id,
                                        home_team_goals,
                                        away_team_goals,
                                        result,
                                        ht_home_team_goals,
                                        ht_away_team_goals,
                                        ht_result)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, matchs_info)
    conn.commit()

# Close the connection to the database
cur.close()
conn.close()