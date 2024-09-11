import pandas as pd
import numpy as np
import csv
import datetime

import sqlite3

con = sqlite3.connect("database/db/football.db")
cur = con.cursor()

cur.execute("""
            CREATE TABLE countries(
                id integer PRIMARY KEY,
                name varchar);
            """)

cur.execute("""
            CREATE TABLE leagues(
                id integer PRIMARY KEY,
                country_id integer NOT NULL,
                name varchar,
                FOREIGN KEY (country_id) REFERENCES countries (id));
            """)

countries_list = tuple(enumerate(
    sorted(("England", "Germany", "Italy", "Spain",
           "France", "Belgium", "Netherlands")),
    start=1))

cur.executemany("""
            INSERT INTO countries
            VALUES(?, ?)
            """, countries_list)
con.commit()

leagues_dictionnary = {"England": ["Premier League", "Championship"],
                       "Germany": ["Bundesliga 1", "Bundesliga 2"],
                       "Italy": ["Serie A", "Serie B"],
                       "Spain": ["La Liga Primera Division", "La Liga Segunda Division"],
                       "France": ["Le Championnat", "Division 2"],
                       "Belgium": ["Jupiler League"],
                       "Netherlands": ["Eredivisie"]}

country_league_list = []
for i, country in countries_list:
    for league in leagues_dictionnary[country]:
        country_league_list.append((i, league))

leagues_list = tuple((i, *item) for i, item in enumerate(country_league_list, start=1))

cur.executemany("""
            INSERT INTO leagues
            VALUES(?, ?, ?)
            """, leagues_list)
con.commit()


cur.execute("""
            CREATE TABLE teams(
                id integer PRIMARY KEY,
                country_id integer NOT NULL,
                name varchar,
                FOREIGN KEY (country_id) REFERENCES countries (id));
            """)
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


teams_set = set()

for url in urls:
    df = pd.read_csv(url)
    teams_set = teams_set.union(set(df["HomeTeam"].dropna().unique()))

teams_list = tuple((i, 1, value)
                   for i, value in enumerate(sorted(list(teams_set)), start=1))


cur.executemany("""
            INSERT INTO teams
            VALUES(?, ?, ?)
            """, teams_list)
con.commit()


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
                FOREIGN KEY (away_team_id) REFERENCES teams (id))
            """)

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

    df.to_csv("database/csv_files/matchs.csv", sep=',', header=False, index=False, mode='a',
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


with open("database/csv_files/matchs.csv") as file:
    matchs_info = csv.reader(file)
    cur.executemany("""
                    INSERT INTO matchs (country_id,
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
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, matchs_info)
    con.commit()


con.close()
