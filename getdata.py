# -*- coding: utf-8 -*-
"""
Functions to get data
"""
import os
import glob
import random
import string
from obspy.core import read


def sncls_CWB(stime, ip, net, debug=True):
    # Get all the sncls that are on the CWB
    sncls = []
    javastr = 'java -jar CWBQuery.jar '
    javastr += '-h ' + ip
    javastr += ' -lsc'
    javastr += ' -b ' + stime.strftime('%Y/%m/%d 00:00:00')
    results = os.popen(javastr).read()
    results = results.split('\n')
    for result in results:
        if result[:2] == net:
            sncls.append(result[:2] + '.' + result[2:7].replace(' ', '') +
                         '.' + result[10:12].replace(' ', '') +
                         '.' + result[7:10])
    if debug:
        print(sncls)
    return sncls


def grab_CWB_data_jar(sncls, stime, ip, debug=True):
    new_avails = []
    letters = string.ascii_uppercase
    stringRan = ''.join(random.choice(letters) for _ in range(10))
    fileName = 'temp' + stringRan
    batchFile = open(fileName, 'w')
    if len(sncls) > 0:
        CWBsncls = sncls_CWB(stime, ip, sncls[0].split('.')[0])
    else:
        CWBsncls = []
    for sncl in sncls:
        if sncl not in CWBsncls:
            continue
        net, sta, loc, chan = sncl.split('.')
        # Grab the current network
        javastr = ' -s \"' + net + sta.ljust(5) + chan + loc + '\"'
        # Grab from the local CWB
        javastr += ' -h ' + ip
        # Use the following time
        javastr += ' -b ' + stime.strftime('%Y/%m/%d 00:00:00')
        # Get the full day
        javastr += ' -d 86400'
        # Grab dcc 512 data type
        javastr += ' -t dcc512'
        javastr += ' -o %N_%y_%j.msd'
        batchFile.write(javastr + '\n')
        if debug:
            print javastr
        # We now have the full query
    batchFile.close()
    javaRequest = 'java -jar CWBQuery.jar -f ' + fileName
    try:
        os.system(javaRequest)
    except:
        print('Problem with: ' + javaRequest)
    if debug:
        print('Finished with CWB request')
    for sncl in sncls:
        if debug:
            print('We are on: ' + sncl)
        net, sta, loc, chan = sncl.split('.')
        fname = net + (sta.ljust(5)).replace(' ', '_')
        if loc == '':
            fname += chan + '__'
        else:
            fname += chan + loc
        fname += '_' + str(stime.year)
        fname += '_' + str(stime.julday) + '.msd'
        if os.path.isfile(fname):
            st = read(fname)
            safe_write(st, stime)
            new_avails.append(get_availability(st))
            os.remove(fname)
        else:
            new_avails.append(0.)
    if os.path.isfile(fileName):
        os.remove(fileName)
    return new_avails


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
    path = '/msd/'
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
    if get_availability(st) == 100.:
        try:
            st.write(curpath, format="MSEED", reclen=512)
            os.system('./DQseed -Q -b 512' + ' ' + curpath)
        except:
            print('Unable to write: ' + curpath)
    elif os.path.exists(curpath):
        st2 = read(curpath)
        if get_availability(st) > get_availability(st2):
            try:
                st.write(curpath, format="MSEED", reclen=512)
                os.system('./DQseed -Q -b 512' + ' ' + curpath)
            except:
                print('Unable to write: ' + curpath)
    else:
        try:
            st.write(curpath, format="MSEED", reclen=512)
            os.system('./DQseed -Q -b 512' + ' ' + curpath)
        except:
            print('Unable to write: ' + curpath)
    return
