#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Usage:
    gitcal.py [<username>]

Options:
    <username>  GitHub username (defaults to current user)
    -h          display this help message
"""

from docopt import docopt
import calendar, datetime
import requests
import os

_color_func = lambda x: [0,1][x>0]+[0,1][x>13]+[0,1][x>27]+[0,1][x>41]
_color_table = [240, 228, 107, 28, 22]

def color(c, s):
    """Returns the string representing the ANSI code for a color
    """
    return "\033[38;05;" + str(c) + "m" + s + "\033[0m"

def get_date(s):
    """Converts a date string of format YYYY/MM/DD to datetime
    """
    return datetime.datetime.strptime(s, "%Y/%m/%d")

def get_calendar(user):
    """Returns the calendar of a user in a 2 dimensional array (ready for printing)
    """
    cal = [[-1 for i in range(53)] for j in range(7)]
    url = "https://github.com/users/{0}/contributions_calendar_data".format(user)
    r = requests.get(url)
    if r.status_code != 200:
        return cal
    data = r.json()
    data = [[get_date(i[0]), i[1]] for i in data]
    offset = (data[0][0].weekday()+1)%7
    for i in range(len(data)):
        row = (i+offset)%7
        col = (i+offset)/7
        cal[row][col] = data[i][1]
    return cal

def print_calendar(cal):
    """Prints a calendar to the terminal (assumes xterm-256color)
    """
    print '  '+''.join(calendar.month_name[(i+9)%12+1][:3]+' '*(5+(i%2)*1) for i in range(12))
    for y in range(7):
        print [' ','M',' ','W',' ','F',' '][y],
        for x in range(53):
            if cal[y][x] == -1:
                print ' ',
            else:
                c = _color_table[_color_func(cal[y][x])]
                print color(c,'█'),
        print

if __name__ == "__main__":
    arguments = docopt(__doc__, version='HP Photosmart 6510 B211a WebScan')
    name = arguments['<username>'] if arguments['<username>'] else os.getlogin()
    cal = get_calendar(name)
    print_calendar(cal)
