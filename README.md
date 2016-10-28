# dailypull
This code does a daily pull from the ASL CWB and the NEIC CWB and adds the data into the msd archive

checkMSD.py does the actual pull and verification.

client.py is the fixed version of the NEIC client from obspy.  This should be removed in future versions after the obspy release.

getdata.py are helper functions for checkMSD.py

getSNCL.py are various helper functions for identifying the SNCLs needed.

# Logic

1) The code first looks for any SNCL on msd that does not contain 100 availability

2) The code then opens metadata for the network and identifies all stations that have open epochs and the SNCL was not obtained from the previous step

3) For every SNCL we request data from the ASL CWB if the data is still not at 100% we request it from the NEIC CWB.

