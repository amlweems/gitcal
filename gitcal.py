#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Usage:
    gitcal.py [<username>] [-b | --block]

Options:
    <username>    GitHub username (defaults to current user)
    -b --block    print colors as solid blocks instead of individual rects
    -h --help     display this help message
    -v --version  display the current version
"""

from docopt import docopt
import calendar, datetime
import requests
import math
import sys
import os

_color_table = [240, 228, 107, 28, 22]

def color(c, s, background):
    """Returns the string representing the ANSI code for a color
    """
    if (c == 0):
        return "\033[0m"+s
    else:
        return "\033["+["38","48"][background]+";05;" + str(c) + "m" + s + "\033[0m"

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
        return None
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
    max_commits = float(max([max(i) for i in cal]))
    if max_commits == 0.0: max_commits = 1.0
    print '  '+''.join(calendar.month_name[(i+9)%12+1][:3]+' '*(5+(i%2)*1) for i in range(12))
    for y in range(7):
        print [' ','M',' ','W',' ','F',' '][y]+" ",
        for x in range(53):
            if cal[y][x] == -1:
                sys.stdout.write("  ")
            else:
                index = int(math.ceil((4*cal[y][x])/max_commits))
                c = _color_table[index]
                if arguments['--block']:
                    if index == 0: c = 0
                    sys.stdout.write(color(c, "  ", True))
                else:
                    sys.stdout.write(color(c, "█", False))
                    sys.stdout.write(" ")
        sys.stdout.write('\n')

if __name__ == "__main__":
    arguments = docopt(__doc__, version='gitcal 0.1')
    name = arguments['<username>'] if arguments['<username>'] else os.getlogin()
    cal = get_calendar(name)
    if cal:
        print_calendar(cal)
    else:
        print "Error: username {0} was not found".format(name)
