import unittest
import getdata
from obspy.core import read, Stream


class TestMSD(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_availability_100(self):
        # Check if we get 100% availability from the test data
        st = read('data/00_LHZ.512.seed')
        self.assertEqual(getdata.get_availability(st), 100.)

    def test_get_availability(self):
        # Check availability of empty data
        st = Stream()
        self.assertEqual(getdata.get_availability(st), 0.)

    def test_check_channel_False(self):
        # Check if the following removes the channel
        filename = 'blah/91_ACE.512.seed'
        self.assertEqual(getdata.check_channel(filename), False)

    def test_check_channel_True(self):
        # Check if the following keeps the channel
        filename = 'balh/00_LHZ.512.seed'
        self.assertEqual(getdata.check_channel(filename), True)


if __name__ == '__main__':
    unittest.main()
