#!/usr/bin/env python

import getSNCL
import getdata
import os
import glob
from obspy.core import UTCDateTime
from obspy.io.xseed import Parser
from multiprocessing import Pool


def get_current_day(debug=False):
    # Grab the beginning of the day and return it at UTCDateTime
    current_day = UTCDateTime.now()
    current_day.hour = 0
    current_day.minute = 0
    current_day.second = 0
    current_day.microsecond = 0
    if debug:
        print('The current day is: ' + str(current_day))
    return current_day


def process_day_net(day, net, sp, clients, debug=False):
    # Find all non 100% data on msd and grab the sncl
    sncls_needed, avails_msd = getdata.check_missing_msd_data(day, net)

    if sp is False:
        sncls_metadata = []
    else:
        # Get all open epochs for the day using metadata
        sncls_metadata = getSNCL.get_sncls_parser(sp, day, net)

    # These are the sncls we need since they aren't on msd
    sncls_missing_msd, avails = getSNCL.check_sncls_msd(sncls_metadata, day)

    # Now we want to append the two lists
    sncls_needed += sncls_missing_msd
    avails_msd += avails

    if clients['ASL']:
        if debug:
            print('Working on ASL CWB')
        ip = '136.177.121.21'
        # Try and pick them from the local CWB
        availsCWBABQ = getdata.grab_CWB_data_jar(sncls_needed, day, ip)
    if clients['NEIC']:
        if debug:
            print('Working on NEIC CWB')
        ip = '137.227.224.97'
        sncls_needed_NEIC = []
        for pair in zip(sncls_needed, availsCWBABQ):
            if pair[1] < 100.:
                sncls_needed_NEIC.append(pair[0])
        # Try to grab from Golden anything we are still missing
        availsCWBNEIC = getdata.grab_CWB_data_jar(sncls_needed_NEIC,
                                                  day, ip)
    # Now we write out the new availability
    avails_out = []
    if clients['ASL']:
        for pair in zip(sncls_needed, availsCWBABQ, avails_msd):
            availsncl = {'sncl': str(pair[0]), 'Day': day.julday,
                         'Year': day.year, 'MSD': pair[2],
                         'ASL': pair[1]}
            if clients['NEIC']:
                try:
                    idx = sncls_needed_NEIC.index(pair[0])
                    availsncl['NEIC'] = availsCWBNEIC[idx]
                except:
                    pass
            avails_out.append(availsncl)
    else:
        for pair in zip(sncls_needed, avails_msd):
            availsncl = {'sncl': str(pair[0]), 'Day': day.julday,
                         'Year': day.year, 'MSD': pair[2]}
            avails_out.append(availsncl)
    print('Done processing ' + net + ' ' + str(day.julday))
    return avails_out


def writelog(avails, net, time, debug=False):
    logDir = 'logs'
    if not os.path.exists(logDir):
        os.mkdir(logDir)
    logName = logDir + '/INFO' + str(time.year) + '_' + \
        str(time.julday).zfill(3) + '_' + \
        net
    InfoFile = open(logName, 'w')
    InfoFile.write('Start time:' + str(time) + '\n')
    for avail in avails:
        if 'ASL' in avail.keys():
            if avail['ASL'] > avail['MSD']:
                InfoFile.write(avail['sncl'] + ', ' + str(avail['Year']) +
                               ', ' + str(avail['Day']))
                InfoFile.write(', MSD: ' + str(avail['MSD']))
                if 'ASL' in avail.keys():
                    InfoFile.write(', ASL: ' + str(avail['ASL']))
                if 'NEIC' in avail.keys():
                    InfoFile.write(', NEIC: ' + str(avail['NEIC']))
                InfoFile.write('\n')
    InfoFile.write('End Time: ' + str(UTCDateTime.now()))
    InfoFile.close()
    return


def emaillog(time):
    # People to email to
    emails = ['aringler@usgs.gov', 'tstorm@usgs.gov']

    # Log directory
    logDir = 'logs'

    # Grab all logs for the day
    logName = logDir + '/INFO' + str(time.year) + '_' + \
        str(time.julday).zfill(3) + '_*'
    logs = glob.glob(logName)
    emailStr = 'mutt -s  \"Back Fill for ' + str(time.year) + \
        ' ' + str(time.julday) + '\"'
    for log in logs:
        emailStr += ' -a ' + log
    emailStr += ' -- '
    for email in emails:
        emailStr += email + ', '
    emailStr += ' </dev/null'
    if debug:
        print(emailStr)
    os.system(emailStr)
    return


if __name__ == "__main__":

    # Here is a debug flag
    debug = False

    # Here is a timing flag
    time = True

    # Grab the current day
    current_day = get_current_day()

    # Start time
    stime = UTCDateTime.now()

    days_back = 30
    number_of_days = 30

    # Make a list of days
    days = [current_day - 24*60*60*(days_back + x) for x in range(number_of_days)]
    networks = ['IU', 'CU', 'US', 'IC', 'GT', 'IW', 'NE', 'XX', 'GS', 'NQ']
    for net in networks:

        try:
            sp = Parser('/APPS/metadata/SEED/' + net + '.dataless')
            clients = {'NEIC': True, 'ASL': True}
        except:
            sp = False
            clients = {'NEIC': False, 'ASL': True}

        # Need to make a function of one variable without a lambda
        def proc_part(x):
            return process_day_net(x, net, sp, clients)

        # pool = Pool(4)
        # avails = pool.map(proc_part, days)
        avails = []
        for day in days:
            avails.append(proc_part(day))
        avails = [item for sublist in avails for item in sublist]
        writelog(avails, net, stime)

    emaillog(stime)
