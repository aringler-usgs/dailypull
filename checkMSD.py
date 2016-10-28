#!/usr/bin/env python

import client
import getSNCL
import getdata
from obspy.core import UTCDateTime
from functools import partial
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
        clientABQ = client.Client(host='136.177.121.21')
        # Try and pick them from the local CWB
        availsCWBABQ = getdata.grab_CWB_data(sncls_needed, day, clientABQ)

    if clients['NEIC']:
        if debug:
            print('Working on NEIC CWB')
        clientNEIC = client.Client()
        sncls_needed_NEIC = []
        for pair in zip(sncls_needed, availsCWBABQ):
            if pair[1] < 100.:
                sncls_needed_NEIC.append(pair[0])
        # Try to grab from Golden anything we are still missing
        availsCWBNEIC = getdata.grab_CWB_data(sncls_needed_NEIC,
                                              day, clientNEIC)
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


if __name__ == "__main__":


    # Here is a debug flag
    debug = False
    
    # Here is a timing flag
    time = True
    
    # Grab the current day
    current_day = get_current_day()
    
    net = 'IC'
    clients = {'NEIC': True, 'ASL': True}

    sp = Parser('/APPS/metadata/SEED/' + net + '.dataless')
    days_back = 4
    number_of_days = 10
    
    InfoFile = open('INFO' + str(current_day.year) + '_' +
                    str(current_day.julday).zfill(3) + '_' +
                    net, 'w')
    
    # Make a list of days
    days = [current_day - 24*60*60*(days_back + x) for x in range(number_of_days)]
    
    # Need to make a function of one variable without a lambda
    def proc_part(x):
        return process_day_net(x, net, sp, clients)

    pool = Pool(10)
    avails = pool.map(proc_part, days)
    print(avails)
    
