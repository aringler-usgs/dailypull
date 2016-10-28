# -*- coding: utf-8 -*-
"""
Functions to get sncls from various locations
"""
import os.path
import socket
from time import sleep


def get_sncls_parser(sp, time, net, debug=False):
    # A function to get all sncls from a parser
    sncls = []
    for cursta in sp.stations:
        # As we scan through blockettes we need to find blockettes 50
        for blkt in cursta:
            if blkt.id == 50:
                # Pull the station info for blockette 50
                stacall = blkt.station_call_letters.strip()
                sncl_temp = net + '.' + stacall + '.'
            if blkt.id == 52:
                sncl = sncl_temp + blkt.location_identifier + '.'
                sncl += blkt.channel_identifier
                if blkt.start_date <= time and blkt.end_date >= time:
                    sncls.append(sncl)
                del sncl
    return sncls


def get_sncls_mdget(time, net, debug=False):
    # Variables that will not change often
    host = "137.227.230.1"
    port = 2052
    maxslept = 60./0.05
    maxblock = 10240
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Set blocking we will want a different timeout approach
    s.setblocking(maxslept)

    timemdget = str(time.year) + '/'
    timemdget += str(time.month).zfill(2) + '/'
    timemdget += str(time.day).zfill(2) + '-00:00:00'

    stringmdget = '-s ' + net + '.*.*.*'
    stringmdget += ' -b ' + timemdget
    stringmdget += " -c r\n"
    if debug:
        print('Request String: ' + stringmdget)
    s.sendall(stringmdget)
    # Now lets get the data
    getmoredata = True

    returnString = ""
    data = ''
    while getmoredata:
        # Pulling the request data and adding it into one big string
        data += s.recv(maxblock)
        if "* <EOR>" in data:
            if debug:
                print 'Found the end of the output'
            getmoredata = False
        else:
            if debug:
                print 'Okay getting more data'
        if 'no channels found' in data:
            returnString += 'No channels found\n'
        sleep(0.05)
    s.close()

    # Splitting the data by EOE into a list
    data = data.split('* <EOE>')
    data.pop()
    sncls = []
    for curepoch in data:
        curepoch = curepoch.split('\n')
        sncl = get_value("* NETWORK", curepoch) + '.'
        sncl += get_value("* STATION", curepoch) + '.'
        sncl += get_value("* LOCATION", curepoch) + '.'
        sncl += get_value("* COMPONENT", curepoch)
        sncls.append(sncl)
    return sncls


def check_sncls_msd(sncls, time, debug=False):
    # Check if there are missing sncls on msd
    neededsncl = []
    avails = []
    for sncl in sncls:
        net, sta, loc, chan = sncl.split('.')
        pathString = '/msd/' + net + '_' + sta + '/' + str(time.year) +\
                     '/' + str(time.julday).zfill(3) + '/' + \
                     loc + '_' + chan + '.512.seed'
        if debug:
            print(pathString)
        if not os.path.isfile(pathString):
            neededsncl.append(sncl)
            avails.append(0.)
    return neededsncl, avails


def get_value(strSearch, data):
    # This is a helper function to not call the search function a bunch
    # Currently this function only deals with 1 parameter so it needs to be
    # modified to deal with poles and zeros
    value = []
    value = [s for s in data if strSearch in s]
    value = (value[0].replace(strSearch, '')).strip()
    return value
