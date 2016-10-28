# -*- coding: utf-8 -*-
"""
Functions to get data
"""
import os
import glob
from obspy.core import read


def grab_CWB_data(sncls, time, client, debug=False):
    # Grab data from the CWB and report the availability
    new_avails = []
    for sncl in sncls:
        net, sta, loc, chan = sncl.split('.')
        st = client.get_waveforms(net, sta, loc,
                                  chan, time, time+24.*60.*60.)
        if len(st) > 0:
            if debug:
                print(st)
            safe_write(st, time)
            new_avails.append(get_availability(st))
            if debug:
                print('Wrote data for:' + str(st))
        else:
            new_avails.append(0.)
    return new_avails


def get_availability(st, debug=False):
    # Grab the availability by way of channel sampling rate and
    # the logic that it should be one day of data
    npts = 0
    if len(st) == 0:
        return 0.
    else:
        sr = st[0].stats.sampling_rate
        for tr in st:
            npts += tr.stats.npts
            if tr.stats.sampling_rate != sr:
                print('Problem with sampling rate' + str(tr.id))
        duration = float(npts)/float(st[0].stats.sampling_rate)
        duration /= (24.*60.*60.)
    return duration*100.


def check_missing_msd_data(day_to_check, network, debug=False):
    # Check data on msd that needs to be requested
    sncls = []
    avails = []
    path_to_files = '/msd/' + network + '_*' + '/' +\
                    str(day_to_check.year) + \
                    '/' + str(day_to_check.julday).zfill(3) + '/*.seed'
    files = glob.glob(path_to_files)
    if debug:
        print(files)
    for current_file in files:
        # Check if this is a data file
        if check_channel(current_file):
            pass
        else:
            continue
        try:
            # Now verify the availability
            st = read(current_file)
            if debug:
                print(st)
            avail = get_availability(st)
            if avail < 100.:
                if debug:
                    print('Need to request more data for:' + current_file)
                sncls.append(str(st[0].id))
                avails.append(avail)
        except:
            print('Problem with ' + current_file)
    return sncls, avails


def check_channel(file_name):
    # Check if the file is actually a data type miniSEED file
    bad_channels = ['_ACE', '_OCF', '_OFC', '_OFA']
    channel = file_name.split('/')[-1].replace('.512.seed', '')
    if any(x in channel for x in bad_channels):
        return False
    else:
        return True


def safe_add(st1, st2):
    # Add traces without producing merged masked arrays
    st = st1.copy()
    for tr in st2:
        if tr not in st1:
            st += tr
    return st


def safe_write(st, time):
    path = os.getcwd()
    if len(st) > 0:
        net, sta, loc, chan = str(st[0].id).split('.')
        curpath = path + '/' + net + '_' + sta
        if not os.path.exists(curpath):
            os.mkdir(curpath)
        curpath += '/' + str(time.year)
        if not os.path.exists(curpath):
            os.mkdir(curpath)
        curpath += '/' + str(time.julday).zfill(3)
        if not os.path.exists(curpath):
            os.mkdir(curpath)
        curpath += '/' + loc + '_' + chan + '.512.seed'
        if os.path.exists(curpath):
            st2 = read(curpath)
            st = safe_add(st, st2)
        st.write(curpath, format="MSEED", reclen=512)
    return
