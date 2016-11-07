#!/usr/bin/env python

import checkMSD
import datetime
import getdata
import getSNCL
import unittest
import util

from obspy.core import read
from obspy.core import UTCDateTime
from obspy.io.xseed import Parser


class UnittestCheckMSD(unittest.TestCase):

    def test_checkMSD_get_current_day(self):
        today = UTCDateTime(UTCDateTime.now().year,
                            UTCDateTime.now().month, UTCDateTime.now().day)
        self.assertEqual(checkMSD.get_current_day(), today)

    def test_checkMSD_process_day_net(self):
        day = '2015001'
        net = 'CU'
        dataless_location = '/APPS/metadata/SEED/%s.dataless' % net
        clients = {'NEIC': True, 'ASL': True}
        test_case = [{'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BBGH.00.BH1',
                      'MSD': 99.99997106481482, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.MTDJ.00.BH2',
                      'MSD': 99.99997106481482, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GRTK.20.LN2',
                      'MSD': 99.9988425925926, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GRTK.20.LNZ',
                      'MSD': 99.9988425925926, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GRTK.20.LN1',
                      'MSD': 99.9988425925926, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.ANWB.20.HN1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.ANWB.20.HN2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.ANWB.20.HNZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BBGH.20.HN1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BBGH.20.HN2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BBGH.20.HNZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.00.BH1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.00.BH2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.00.BHZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.20.HN1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.20.HN2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.20.HNZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.00.LH1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.00.LH2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.00.LHZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.20.LN1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.20.LN2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.20.LNZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.00.VMU',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.00.VMV',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.BCIP.00.VMW',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GRGR.20.HN1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GRGR.20.HN2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GRGR.20.HNZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GRTK.20.HN1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GRTK.20.HN2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GRTK.20.HNZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GTBY.20.HN1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GTBY.20.HN2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.GTBY.20.HNZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.MTDJ.20.HN1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.MTDJ.20.HN2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.MTDJ.20.HNZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.SDDR.20.HN1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.SDDR.20.HN2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.SDDR.20.HNZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.TGUH.20.HN1',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.TGUH.20.HN2',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0},
                     {'NEIC': 0.0, 'Year': 2015, 'sncl': 'CU.TGUH.20.HNZ',
                      'MSD': 0.0, 'Day': 1, 'ASL': 0.0}]
        self.assertEqual(checkMSD.process_day_net(UTCDateTime(day), net,
                         Parser(dataless_location), clients), test_case)


class UnittestGetData(unittest.TestCase):

    def test_getData_get_availability(self):
        test_availability = 100.0
        test_file = '/msd/CU_ANWB/2015/001/00_BHZ.512.seed'
        self.assertEqual(getdata.get_availability(read(test_file)),
                         test_availability)

    def test_getData_check_missing_msd_data(self):
        test_day = UTCDateTime('2015001')
        test_network = 'CU'
        test_case = (['CU.BBGH.00.BH1', 'CU.MTDJ.00.BH2', 'CU.GRTK.20.LN2',
                      'CU.GRTK.20.LNZ', 'CU.GRTK.20.LN1'],
                     [99.99997106481482, 99.99997106481482, 99.9988425925926,
                      99.9988425925926, 99.9988425925926])
        self.assertEqual(getdata.check_missing_msd_data(test_day,
                                                        test_network),
                         test_case)

    def test_getData_check_channel(self):
        test_filename_false = '/msd/CU_BBGH/2015/001/_ACE.512.seed'
        test_filename_true = '/msd/CU_ANWB/2015/001/00_BHZ.512.seed'
        self.assertFalse(getdata.check_channel(test_filename_false))
        self.assertTrue(getdata.check_channel(test_filename_true))


class UnittestGetSNCL(unittest.TestCase):

    def test_getSNCL_get_sncls_parser(self):
        test_dataless = Parser('/APPS/metadata/SEED/CU.dataless')
        test_day = UTCDateTime('2015001')
        test_network = 'CU'
        test_case = [u'CU.ANWB.00.BH1', u'CU.ANWB.00.BH2', u'CU.ANWB.00.BHZ',
                     u'CU.ANWB.20.HN1', u'CU.ANWB.20.HN2', u'CU.ANWB.20.HNZ',
                     u'CU.ANWB.00.LH1', u'CU.ANWB.00.LH2', u'CU.ANWB.00.LHZ',
                     u'CU.ANWB.20.LN1', u'CU.ANWB.20.LN2', u'CU.ANWB.20.LNZ',
                     u'CU.ANWB.00.VMU', u'CU.ANWB.00.VMV', u'CU.ANWB.00.VMW',
                     u'CU.BBGH.00.BH1', u'CU.BBGH.00.BH2', u'CU.BBGH.00.BHZ',
                     u'CU.BBGH.20.HN1', u'CU.BBGH.20.HN2', u'CU.BBGH.20.HNZ',
                     u'CU.BBGH.00.LH1', u'CU.BBGH.00.LH2', u'CU.BBGH.00.LHZ',
                     u'CU.BBGH.20.LN1', u'CU.BBGH.20.LN2', u'CU.BBGH.20.LNZ',
                     u'CU.BBGH.00.VMU', u'CU.BBGH.00.VMV', u'CU.BBGH.00.VMW',
                     u'CU.BCIP.00.BH1', u'CU.BCIP.00.BH2', u'CU.BCIP.00.BHZ',
                     u'CU.BCIP.20.HN1', u'CU.BCIP.20.HN2', u'CU.BCIP.20.HNZ',
                     u'CU.BCIP.00.LH1', u'CU.BCIP.00.LH2', u'CU.BCIP.00.LHZ',
                     u'CU.BCIP.20.LN1', u'CU.BCIP.20.LN2', u'CU.BCIP.20.LNZ',
                     u'CU.BCIP.00.VMU', u'CU.BCIP.00.VMV', u'CU.BCIP.00.VMW',
                     u'CU.GRGR.00.BH1', u'CU.GRGR.00.BH2', u'CU.GRGR.00.BHZ',
                     u'CU.GRGR.20.HN1', u'CU.GRGR.20.HN2', u'CU.GRGR.20.HNZ',
                     u'CU.GRGR.00.LH1', u'CU.GRGR.00.LH2', u'CU.GRGR.00.LHZ',
                     u'CU.GRGR.20.LN1', u'CU.GRGR.20.LN2', u'CU.GRGR.20.LNZ',
                     u'CU.GRGR.00.VMU', u'CU.GRGR.00.VMV', u'CU.GRGR.00.VMW',
                     u'CU.GRTK.00.BH1', u'CU.GRTK.00.BH2', u'CU.GRTK.00.BHZ',
                     u'CU.GRTK.20.HN1', u'CU.GRTK.20.HN2', u'CU.GRTK.20.HNZ',
                     u'CU.GRTK.00.LH1', u'CU.GRTK.00.LH2', u'CU.GRTK.00.LHZ',
                     u'CU.GRTK.20.LN1', u'CU.GRTK.20.LN2', u'CU.GRTK.20.LNZ',
                     u'CU.GRTK.00.VMU', u'CU.GRTK.00.VMV', u'CU.GRTK.00.VMW',
                     u'CU.GTBY.00.BH1', u'CU.GTBY.00.BH2', u'CU.GTBY.00.BHZ',
                     u'CU.GTBY.20.HN1', u'CU.GTBY.20.HN2', u'CU.GTBY.20.HNZ',
                     u'CU.GTBY.00.LH1', u'CU.GTBY.00.LH2', u'CU.GTBY.00.LHZ',
                     u'CU.GTBY.20.LN1', u'CU.GTBY.20.LN2', u'CU.GTBY.20.LNZ',
                     u'CU.GTBY.00.VMU', u'CU.GTBY.00.VMV', u'CU.GTBY.00.VMW',
                     u'CU.MTDJ.00.BH1', u'CU.MTDJ.00.BH2', u'CU.MTDJ.00.BHZ',
                     u'CU.MTDJ.20.HN1', u'CU.MTDJ.20.HN2', u'CU.MTDJ.20.HNZ',
                     u'CU.MTDJ.00.LH1', u'CU.MTDJ.00.LH2', u'CU.MTDJ.00.LHZ',
                     u'CU.MTDJ.20.LN1', u'CU.MTDJ.20.LN2', u'CU.MTDJ.20.LNZ',
                     u'CU.MTDJ.00.VMU', u'CU.MTDJ.00.VMV', u'CU.MTDJ.00.VMW',
                     u'CU.SDDR.00.BH1', u'CU.SDDR.00.BH2', u'CU.SDDR.00.BHZ',
                     u'CU.SDDR.20.HN1', u'CU.SDDR.20.HN2', u'CU.SDDR.20.HNZ',
                     u'CU.SDDR.00.LH1', u'CU.SDDR.00.LH2', u'CU.SDDR.00.LHZ',
                     u'CU.SDDR.20.LN1', u'CU.SDDR.20.LN2', u'CU.SDDR.20.LNZ',
                     u'CU.SDDR.00.VMU', u'CU.SDDR.00.VMV', u'CU.SDDR.00.VMW',
                     u'CU.TGUH.00.BH1', u'CU.TGUH.00.BH2', u'CU.TGUH.00.BHZ',
                     u'CU.TGUH.20.HN1', u'CU.TGUH.20.HN2', u'CU.TGUH.20.HNZ',
                     u'CU.TGUH.00.LH1', u'CU.TGUH.00.LH2', u'CU.TGUH.00.LHZ',
                     u'CU.TGUH.20.LN1', u'CU.TGUH.20.LN2', u'CU.TGUH.20.LNZ',
                     u'CU.TGUH.00.VMU', u'CU.TGUH.00.VMV', u'CU.TGUH.00.VMW']
        self.assertEqual(getSNCL.get_sncls_parser(test_dataless, test_day,
                                                  test_network), test_case)

    def test_getSNCL_check_scls_msd(self):
        test_sncls = [u'CU.ANWB.00.BH1', u'CU.ANWB.00.BH2', u'CU.ANWB.00.BHZ',
                      u'CU.ANWB.20.HN1', u'CU.ANWB.20.HN2', u'CU.ANWB.20.HNZ',
                      u'CU.ANWB.00.LH1', u'CU.ANWB.00.LH2', u'CU.ANWB.00.LHZ',
                      u'CU.ANWB.20.LN1', u'CU.ANWB.20.LN2', u'CU.ANWB.20.LNZ',
                      u'CU.ANWB.00.VMU', u'CU.ANWB.00.VMV', u'CU.ANWB.00.VMW',
                      u'CU.BBGH.00.BH1', u'CU.BBGH.00.BH2', u'CU.BBGH.00.BHZ',
                      u'CU.BBGH.20.HN1', u'CU.BBGH.20.HN2', u'CU.BBGH.20.HNZ',
                      u'CU.BBGH.00.LH1', u'CU.BBGH.00.LH2', u'CU.BBGH.00.LHZ',
                      u'CU.BBGH.20.LN1', u'CU.BBGH.20.LN2', u'CU.BBGH.20.LNZ',
                      u'CU.BBGH.00.VMU', u'CU.BBGH.00.VMV', u'CU.BBGH.00.VMW',
                      u'CU.BCIP.00.BH1', u'CU.BCIP.00.BH2', u'CU.BCIP.00.BHZ',
                      u'CU.BCIP.20.HN1', u'CU.BCIP.20.HN2', u'CU.BCIP.20.HNZ',
                      u'CU.BCIP.00.LH1', u'CU.BCIP.00.LH2', u'CU.BCIP.00.LHZ',
                      u'CU.BCIP.20.LN1', u'CU.BCIP.20.LN2', u'CU.BCIP.20.LNZ',
                      u'CU.BCIP.00.VMU', u'CU.BCIP.00.VMV', u'CU.BCIP.00.VMW',
                      u'CU.GRGR.00.BH1', u'CU.GRGR.00.BH2', u'CU.GRGR.00.BHZ',
                      u'CU.GRGR.20.HN1', u'CU.GRGR.20.HN2', u'CU.GRGR.20.HNZ',
                      u'CU.GRGR.00.LH1', u'CU.GRGR.00.LH2', u'CU.GRGR.00.LHZ',
                      u'CU.GRGR.20.LN1', u'CU.GRGR.20.LN2', u'CU.GRGR.20.LNZ',
                      u'CU.GRGR.00.VMU', u'CU.GRGR.00.VMV', u'CU.GRGR.00.VMW',
                      u'CU.GRTK.00.BH1', u'CU.GRTK.00.BH2', u'CU.GRTK.00.BHZ',
                      u'CU.GRTK.20.HN1', u'CU.GRTK.20.HN2', u'CU.GRTK.20.HNZ',
                      u'CU.GRTK.00.LH1', u'CU.GRTK.00.LH2', u'CU.GRTK.00.LHZ',
                      u'CU.GRTK.20.LN1', u'CU.GRTK.20.LN2', u'CU.GRTK.20.LNZ',
                      u'CU.GRTK.00.VMU', u'CU.GRTK.00.VMV', u'CU.GRTK.00.VMW',
                      u'CU.GTBY.00.BH1', u'CU.GTBY.00.BH2', u'CU.GTBY.00.BHZ',
                      u'CU.GTBY.20.HN1', u'CU.GTBY.20.HN2', u'CU.GTBY.20.HNZ',
                      u'CU.GTBY.00.LH1', u'CU.GTBY.00.LH2', u'CU.GTBY.00.LHZ',
                      u'CU.GTBY.20.LN1', u'CU.GTBY.20.LN2', u'CU.GTBY.20.LNZ',
                      u'CU.GTBY.00.VMU', u'CU.GTBY.00.VMV', u'CU.GTBY.00.VMW',
                      u'CU.MTDJ.00.BH1', u'CU.MTDJ.00.BH2', u'CU.MTDJ.00.BHZ',
                      u'CU.MTDJ.20.HN1', u'CU.MTDJ.20.HN2', u'CU.MTDJ.20.HNZ',
                      u'CU.MTDJ.00.LH1', u'CU.MTDJ.00.LH2', u'CU.MTDJ.00.LHZ',
                      u'CU.MTDJ.20.LN1', u'CU.MTDJ.20.LN2', u'CU.MTDJ.20.LNZ',
                      u'CU.MTDJ.00.VMU', u'CU.MTDJ.00.VMV', u'CU.MTDJ.00.VMW',
                      u'CU.SDDR.00.BH1', u'CU.SDDR.00.BH2', u'CU.SDDR.00.BHZ',
                      u'CU.SDDR.20.HN1', u'CU.SDDR.20.HN2', u'CU.SDDR.20.HNZ',
                      u'CU.SDDR.00.LH1', u'CU.SDDR.00.LH2', u'CU.SDDR.00.LHZ',
                      u'CU.SDDR.20.LN1', u'CU.SDDR.20.LN2', u'CU.SDDR.20.LNZ',
                      u'CU.SDDR.00.VMU', u'CU.SDDR.00.VMV', u'CU.SDDR.00.VMW',
                      u'CU.TGUH.00.BH1', u'CU.TGUH.00.BH2', u'CU.TGUH.00.BHZ',
                      u'CU.TGUH.20.HN1', u'CU.TGUH.20.HN2', u'CU.TGUH.20.HNZ',
                      u'CU.TGUH.00.LH1', u'CU.TGUH.00.LH2', u'CU.TGUH.00.LHZ',
                      u'CU.TGUH.20.LN1', u'CU.TGUH.20.LN2', u'CU.TGUH.20.LNZ',
                      u'CU.TGUH.00.VMU', u'CU.TGUH.00.VMV', u'CU.TGUH.00.VMW']
        test_date = UTCDateTime('2015001')
        test_case = ([u'CU.ANWB.20.HN1', u'CU.ANWB.20.HN2', u'CU.ANWB.20.HNZ',
                      u'CU.BBGH.20.HN1', u'CU.BBGH.20.HN2', u'CU.BBGH.20.HNZ',
                      u'CU.BCIP.00.BH1', u'CU.BCIP.00.BH2', u'CU.BCIP.00.BHZ',
                      u'CU.BCIP.20.HN1', u'CU.BCIP.20.HN2', u'CU.BCIP.20.HNZ',
                      u'CU.BCIP.00.LH1', u'CU.BCIP.00.LH2', u'CU.BCIP.00.LHZ',
                      u'CU.BCIP.20.LN1', u'CU.BCIP.20.LN2', u'CU.BCIP.20.LNZ',
                      u'CU.BCIP.00.VMU', u'CU.BCIP.00.VMV', u'CU.BCIP.00.VMW',
                      u'CU.GRGR.20.HN1', u'CU.GRGR.20.HN2', u'CU.GRGR.20.HNZ',
                      u'CU.GRTK.20.HN1', u'CU.GRTK.20.HN2', u'CU.GRTK.20.HNZ',
                      u'CU.GTBY.20.HN1', u'CU.GTBY.20.HN2', u'CU.GTBY.20.HNZ',
                      u'CU.MTDJ.20.HN1', u'CU.MTDJ.20.HN2', u'CU.MTDJ.20.HNZ',
                      u'CU.SDDR.20.HN1', u'CU.SDDR.20.HN2', u'CU.SDDR.20.HNZ',
                      u'CU.TGUH.20.HN1', u'CU.TGUH.20.HN2', u'CU.TGUH.20.HNZ'],
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.assertEqual(getSNCL.check_sncls_msd(test_sncls, test_date),
                         test_case)


class UnittestUtil(unittest.TestCase):

    def test_util_asctime(self):
        test_time = datetime.datetime.utcnow()
        self.assertEqual(util.asctime(), '%s:%s:%s' %
                         (str(test_time.hour).zfill(2),
                          str(test_time.minute).zfill(2),
                          str(test_time.second).zfill(2)))

    def test_util_ascdate(self):
        test_time = datetime.datetime.utcnow()
        self.assertEqual(util.ascdate(), '%s-%s-%s' %
                         (str(test_time.year)[2:],
                          str(test_time.month).zfill(2),
                          str(test_time.day).zfill(2)))
    # def test_util_dsecs(self):
    #     'Unused in this project'
    #     test_elapse = 12.3456789
    #     test_time1 = datetime.datetime(2012,3,4,5,6,7,89)
    #     test_time2 = test_time1 + datetime.timedelta(test_elapse)
    #     self.assertEqual(util.dsecs(test_time2 - test_time1),
    #                      test_elapse * 86400)

if __name__ == '__main__':
    unittest.main()
