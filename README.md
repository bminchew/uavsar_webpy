uavsar-webpy
============

uavsar-webpy module contains a few simple tools to download UAVSAR data from ASF. 
Some examples are included below.  

Website
-------
http://www.gps.caltech.edu/~bminchew/mycodes/uavsar_webpy/uavsar_webpy-0.1.0/doc/build/html/index.html

Install
-------
python setup.py install [--prefix=/path/to/pybuild/uavsar-webpy] 

Requirements
------------
- Python 2.6 or greater 
- Numpy 1.6.0 or greater
- Python module Mechanize (http://wwwsearch.sourceforge.net/mechanize/) must be installed and
discoverable in PYTHONPATH

Options
-------
For convenience, create a text file $HOME/.dathack.d whose first line reads:
      uavsarhttp:username:password (replace fields username and password accordingly) 
   (if you're concerned about privacy run: chmod a-rxw .dathack.d; chmod u+r .dathack.d )
If $HOME/.dathack.d is not found or if line uavsarhttp:username:password is not
present, the routine will prompt the user for the username and password

Examples
--------
Copy the data link from the UAVSAR website (http://uavsar.jpl.nasa.gov)

1)  Download all PolSAR products in radar coordinates for SanAnd_08503_10084_002_101201_L090_CX_01

   run:  uavsar_polsar_download.py http://uavsar.asfdaac.alaska.edu/UA_SanAnd_08503_10071_003_100928_L090_CX_01/SanAnd_08503_10071_003_100928_L090HHHH_CX_01.mlc

2)  Download only HHHH data in both radar and ground range coordinates for the same data set

   run:  uavsar_polsar_download.py http://uavsar.asfdaac.alaska.edu/UA_SanAnd_08503_10071_003_100928_L090_CX_01/SanAnd_08503_10071_003_100928_L090HHHH_CX_01.mlc mlc,grd hhhh

3)  Download all RPI products in slant range coordinates for SanAnd_08503_09083-008_10027-003_0174d_s01_L090_01

   run:  uavsar_insar_download.py http://uavsar.asfdaac.alaska.edu/UA_SanAnd_08503_09083-008_10027-003_0174d_s01_L090_01/SanAnd_08503_09083-008_10027-003_0174d_s01_L090HH_01.int 

4)  Download unwrapped interferograms and correlation files in slant and ground range coordinates for SanAnd_08503_09083-008_10027-003_0174d_s01_L090_01

   run:  uavsar_insar_download.py http://uavsar.asfdaac.alaska.edu/UA_SanAnd_08503_09083-008_10027-003_0174d_s01_L090_01/SanAnd_08503_09083-008_10027-003_0174d_s01_L090HH_01.int int,cor rdr,grd 



