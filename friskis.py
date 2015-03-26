# -*- coding: utf-8 -*-
import re
import datetime
import locale

import requests
from pyquery import PyQuery

# Title of the heading before table containing shedule, used to find the correct table
SCHEDULE_TABLE_HEADING = 'Bokningsbara aktiviteter'


class URLs:
    base = 'http://linkoping.friskissvettis.se/'
    login = base + 'default.aspx?action=login_user'
    schedule = base + 'default.asp?page=183'


class Shift(object):
    def __init__(self, name, venue, leader_name, start_dt, end_dt, booking_url=None,
                 booked_places=None, bookable_places=None, total_places=None):
        self.name = name
        self.venue = venue
        self.leader_name = leader_name
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.booking_url = booking_url
        self.booked_places = booked_places
        self.bookable_places = bookable_places
        self.total_places = total_places

    def __unicode__(self):
        return u'%s, %s' % (self.name, self.leader_name)

    def __repr__(self):
        return '%s, %s' % (self.name, self.leader_name)

    def book(self, session):
        assert self.booking_url
        return session.get(self.booking_url)


def is_date(row):
    return len(row.children()) == 1


def is_beginning_of_crap(row):
    return len(row.children()) == 2 or not row.text()


def int_tuple(t):
    return (int(x) for x in t)


def parse_places(place_string):
    [places] = re.findall('\((\d+)\/(\d+)\) (\d+)', place_string)
    return int_tuple(places)


def parse_time(time_string):
    return datetime.time(*int_tuple(time_string.split(':')))


def parse_start_end_time(times):
    start, end = times.split('-')
    return parse_time(start), parse_time(end)


def parse_shift(row, date):
    cells = row.children()
    start_time, end_time = parse_start_end_time(cells.eq(1).text())

    href = cells.find('a').attr('href')
    url = URLs.base + href if href else None

    booked, bookable, total = parse_places(cells.eq(4).text())

    return Shift(name=cells.eq(2).text(),
                 venue=cells.eq(0).text(),
                 leader_name=cells.eq(3).text(),
                 start_dt=datetime.datetime.combine(date, start_time),
                 end_dt=datetime.datetime.combine(date, end_time),
                 booking_url=url,
                 booked_places=booked,
                 bookable_places=bookable,
                 total_places=total)


def parse_date(row):
    date = datetime.datetime.strptime(' '.join(row.text().split()[2:]), '%d %B')
    today = datetime.date.today()

    date = date.replace(year=today.year + (1 if date.month < today.month else 0))
    return date


class FriskisClient():

    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'sv_SE')
        self.session = requests.Session()

    def login(self, username, password):
        self.session.post(URLs.login, data={'user': username, 'pwd': password})

    def get_available_shifts(self):
        response = self.session.get(URLs.schedule)

        e = PyQuery(response.text)
        rows = e.find("h1:contains('%s')" % SCHEDULE_TABLE_HEADING).next().find('tr')

        for row in rows.items():
            # This check is needed since the HTML is slighly broken, which makes it impossible
            # to select exactly the table that we want...
            if is_beginning_of_crap(row):
                break

            if is_date(row):
                date = parse_date(row)
            else:
                yield parse_shift(row, date)
