#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrapVegas.py
~~~~~~~~~~~~~~~~~

Scraping of vegas.com for Barnes.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/fantasyNCAA
"""
import requests
from bs4 import BeautifulSoup


class Game(object):

    def __init__(self, date, time, team1, team2, favorite,
                 spread, total, money_line):
        self.date = date
        self.time = time
        self.team1 = team1
        self.team2 = team2
        self.favorite = favorite
        self.spread = spread
        self.total = total
        self.money_line = money_line

    def __repr__(self):
        return '<Game({} v {}>'.format(self.team1, self.team2)

    def info(self):
        return ('date={}, team1={}, team2={}, favorite={}, spread={}'.format(
                self.date, self.team1, self.team2, self.favorite, self.spread))


def get_page(url):
    request = requests.get(url)
    return request.text


def get_table(page):
    sports_data = page.find("table", {"class": "sportsline"})
    rows = sports_data.find_all("tr")
    rows.pop(0)  # removes header
    rows.pop(0)  # removes subheader
    clean_rows = [clean_row(row) for row in rows]

    return clean_rows


def rows_to_game(rows):
    game = []
    for row in rows:
        if row != 'new game':
            row = row.split(';')
            row = filter(None, row)
            game.extend(row)
        else:
            yield game
            game = []


def clean_row(row):
    new_row = ''

    tds = row.find_all("td")
    for td in tds:
        fonts = td.find_all('font')
        for font in fonts:
            if font.text:
                new_row += '{};'.format(font.text.replace('\xa0', ''))

    if new_row == '':
        return 'new game'
    return new_row


def make_games(rows):
    games = []
    raw_games = [game for game in rows_to_game(rows)]

    for game in raw_games:
        date = game[0]
        team1 = game[1]
        time = game[2]
        team2 = game[3]
        if game[4] == 'Point spreads have not been posted for this contest':
            spread = 'Not available yet.'
            favorite = 'Not available yet.'
        else:
            favorite = game[(game.index('Favorite') + 1)]  # game[5]
            spread = game[(game.index('Point spread') + 1)]  # game[9]
            total = game[(game.index('Total') + 1)]  # game[13]
            money_line = game[(game.index('Total money line') + 1)]  # game[17]
            new_game = Game(date, time, team1, team2, favorite, spread,
                            total, money_line)
            games.append(new_game)

    return games

if __name__ == "__main__":
    url = 'https://www.vegas.com/gaming/sportsline/college-football/'
    page = get_page(url)
    page = BeautifulSoup(page, 'html.parser')
    rows = get_table(page)
    games = make_games(rows)
    for game in games:
        print(game.info())
