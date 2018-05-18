#!/usr/bin/env python3

import os
import re
import datetime
import shutil

dirs = "/home/fos/Dokumente/Computer/python/pih_retention/testdir/"

daysaweek = 3
weekstokeep = 52
daystokeep = 60
monthlytokeep = 12
yearlytokeep = 10


def combinedirname(data):
    final = []

    for year, month, day in data:
        year = str(year)
        month = str(month)
        day = str(day)

        if len(month) <= 1:
            month = "0%s" % (month)
        if len(day) <= 1:
            day = "0%s" % (day)

        final.append("%s-%s-%s" % (year, month, day))
    # sort and uniq
    return sorted(set(final))


def splitdirnames(data):
    year, month, day = data.split('-')
    return [int(year), int(month), int(day)]


def getdirnames():
    final = []
    for dir in os.listdir(dirs):
        if re.search(r'^20..-..-..', dir):
            final.append(splitdirnames(dir))
    final.sort()
    final.reverse()
    return final


def getkeepeddirnames(data):
    a = []
    final = []

    for format in (daily, weekly, monthly, yearly):
        a.append(format(data))

    for formatdates in a:
        for dates in formatdates:
            final.append(dates)

    return combinedirname(final)


def getremoveddirnames(keep, data):
    final = []
    data = combinedirname(data)
    # convert from set to list
    a = set(data) - set(keep)
    for b in a:
        final.append(b)

    return sorted(final)


def removedirnames(data):
    os.chdir(dirs)
    for dir in data:
        # double check ...
        if os.path.isdir(dir):
            shutil.rmtree(dir)


def daily(data):
    final = []
    daystokeepi = daystokeep - 1
    for index, a in enumerate(data, start=0):
        if index <= daystokeepi:
            final.append(a)
    return final


def weekly(data):
    # sunday, wednesday, friday, tuesday, thursday, monday, saturday
    order = (7, 3, 5, 2, 4, 1, 6)
    i = 1
    final = []
    clearorder = []
    daysaweeki = daysaweek - 1

    for index, a in enumerate(order, start=0):
        if index <= daysaweeki:
            clearorder.append(a)

    for year, month, day in data:
        dayofweek = datetime.date(year, month, day).isoweekday()
        for dayorder in clearorder:
            if dayofweek == dayorder:
                if i <= weekstokeep:
                    final.append([year, month, day])
                    i = i + 1
    return final


def monthly(data):
    final = []
    i = 0
    y = 0
    monthlytokeepi = monthlytokeep - 1

    for year, month, day in data:
        # full backuped month
        if day >= 28:
            if data[i - 1][1] != month:
                if y <= monthlytokeepi:
                    final.append([year, month, day])
                    y = y + 1
        i = i + 1
    return final


def yearly(data):
    final = []
    i = 0
    y = 0

    yearlytokeepi = yearlytokeep - 1
    for year, month, day in data:
        # latest backup in year
        if data[i - 1][1] <= month:
            # latest backup in month
            if data[i - 1][2] <= day:
                if y <= yearlytokeepi:
                    final.append([year, month, day])
                    y = y + 1
        i = i + 1
    return final


data = getdirnames()
keep = getkeepeddirnames(data)
remove = getremoveddirnames(keep, data)
#removedirnames(remove)

print(keep)
print(remove)

print("Backups to keep %i" % (len(keep)))
print("Backups to remove %i" % (len(remove)))
