#!/opt/local/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python

"""
uavsar_insar_download.py  :  Download UAVSAR InSAR data from ASF through the password protection

Usage:

.. code-block:: bash

   $ uavsar_insar_download.py url [options]

Parameter
---------
   url   :  Any single URL corresponding to the desired UAVSAR data 

Options
-------
   para  :  data paradigm [default is determined from file extension]
            :options:  
               |  all  --   get it all  
               |  ann  --   get only the annotation file 
               |  rdr  --   get slant-range data and annotation file
               |  grd  --   get ground-range data and annotation file
               |  kmz  --   get kmz files and annotation file

   type  :  data type [igm]
            :options:
               |  igm  --   get it all (default)  
               |  amp1 --   amplitude of scene 1
               |  amp2 --   amplitude of scene 2
               |  int  --   wrapped interferogram
               |  unw  --   unwrapped interferogram
               |  cor  --  correlation
               |  hgt  --   DEM (only valid with grd paradigm)

   chan  :  data channels [hh]
            :options:
               |  hh   --   co-polarized horizontal (default)
               |  hv   --   cross-polarized
               |  vv   --   co-polarized vertical 

Notes
-----
* Use a comma separted list (no spaces) for multiple options (e.g. rdr,grd)

* Do not combine para, type, and/or chan lists

* Python Mechanize (http://wwwsearch.sourceforge.net/mechanize/) must be installed and 
   discoverable in PYTHONPATH

* For convenience, create a text file $HOME/.dathack.d whose first line reads:
   uavsarhttp:<username>:<password> (replace fields <username> and <password>) 
   (if you're concerned about privacy run: chmod a-rxw .dathack.d; chmod u+r .dathack.d )

* If $HOME/.dathack.d is not found or if line uavsarhttp:<username>:<password> is not
   present, the routine will prompt the user for the username and password

See Also
--------
:ref:`uavsar_polsar_download`, :ref:`http_retrieve`

Examples
--------
First let's decide on some data.  A random choice (separated and given in bash format for instructional purposes only...one could just cut and paste the complete address):

.. code-block:: bash

   $ url=http://uavsar.asfdaac.alaska.edu
   $ line=UA_SanAnd_08503_09083-008_10027-003_0174d_s01_L090_01
   $ data=SanAnd_08503_09083-008_10027-003_0174d_s01_L090HH_01.int
   $ link=$url/$line/$data

Download all interferograms and supporting data (amp1, amp2, cor, int, unw) in radar coordinates for line `SanAnd_08503_09083-008_10027-003_0174d_s01_L090HH_01`_:

.. code-block:: bash

   $ uavsar_insar_download.py link

Download wrapped igrams and correlation maps in radar and groundrange coordinates as well as kmz format:

.. code-block:: bash

   $ uavsar_insar_download.py link rdr,grd,kmz int,cor

.. _SanAnd_08503_09083-008_10027-003_0174d_s01_L090HH_01: http://uavsar.jpl.nasa.gov/cgi-bin/product.pl?jobName=SanAnd_08503_09083-008_10027-003_0174d_s01_L090_01#data

"""
from __future__ import print_function, division
import sys,os
import numpy as np
from http_retrieve import http_retrieve, get_password

__title__      = 'uavsar_insar_download.py'
__author__     = 'Brent Minchew'
__email__      = 'bminchew@caltech.edu'
__created__    = 'June 2013'
__modified__   = ''
__version__    = '0.1'
__status__     = 'Development'
__conditions__ = 'Use at your own risk.'
__license__    = """
Copyright (C) 2013   Brent M. Minchew
--------------------------------------------------------------------
GNU Licensed

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

--------------------------------------------------------------------
"""

###==============================================================================###
def main(args):
   para,types,chan = _get_paradigm_channels(args) 
   urls = URLs(args[0],para,types,chan)
   _organize_fldr(urls)
   username, password = get_password()
   print('Files to download:')
   for fname in urls.filenames:
      print(urls.urllead+fname)
   print('\n')
   for fname in urls.filenames:
      print('downloading: '+urls.urllead+fname)
      http_retrieve(urls.urllead+fname, username=username, password=password)

###==============================================================================###
def _organize_fldr(urls):
   localfldr = urls.fldr.split('/')[-1]
   if 'UA_' == localfldr[:3]: localfldr = localfldr[3:]
   if not os.path.exists(localfldr) and os.getcwd().split('/')[-1] != localfldr:
      os.mkdir(localfldr)
   if os.getcwd().split('/')[-1] != localfldr: 
      os.chdir(localfldr)

###-------------------------------------------------------------------------------###
def _get_paradigm_channels(args):
   all_paras = ['all','ann','rdr','grd','kmz']
   all_types = ['igm','amp1','amp2','int','unw','cor','hgt','dem']
   all_chans = ['HH','HV','VV'] 
   chan_opts = ['ach','hh','hv','vv']

   # set defaults
   if args[0].split('.')[-1].strip() == 'ann': 
      para = ['ann']
   elif args[0].split('.')[-1].strip() == 'grd':
      para = ['grd']
   elif args[0].split('.')[-1].strip() == 'kmz':
      para = ['kmz']
   else:
      para = ['rdr']
   channels = ['hh']
   types = ['igm']

   for i in np.arange(1,len(args)):
      tpar, ttyp = False, False
      temp_para = args[i].split(',')
      for par in temp_para:
         if par in all_paras: 
            tpar = True
         elif par in all_types:
            ttyp = True
      if tpar: 
         para = temp_para
      elif ttyp:
         types = temp_para
      else:
         channels = temp_para

   if 'all' in para:
      para = all_paras[1:]
   if 'igm' in types:
      types = all_types[1:-1]
   if 'ach' in channels:
      channels = all_chans

   newpara, newchan, newtype = [], [], []
   for par in para:
      if par in all_paras: 
         if par == 'rdr':
            newpara.append('')
         else:
            newpara.append(par)
   for typ in types:
      if typ in all_types[1:-1]: newtype.append(typ)
   for chan in channels:
      if chan in chan_opts[-3:] or chan in all_chans: 
         newchan.append(chan.upper())

   if len(newpara) < 1:
      if len(para) == 1: 
         print('Invalid paradigm: ',para)
      else:
         print('Invalid paradigms: ',para)
      sys.exit()

   if len(newtype) < 1:
      if len(types) == 1:
         print('Invalid type: ',types)
      else:
         print('Invalid types: ',types)
      sys.exit()

   if len(newchan) < 1:
      if len(channels) == 1:
         print('Invalid channel: ',channels)
      else:
         print('Invalid channels: ',channels)
      sys.exit()

   newpara = uniquify_list(newpara)
   newtype = uniquify_list(newtype)
   newchan = uniquify_list(newchan)

   return newpara, newtype, newchan

###-------------------------------------------------------------------------------###
def uniquify_list(lis):
   new = []
   for i in lis:
      if i not in new: new.append(i)
   return new

###-------------------------------------------------------------------------------###
class URLs():
   """
   Class that builds a family of URLs from the sample
   """
   def __init__(self,sample,para,types,channels):
      if 'http://' in sample or 'https://' in sample:
         self.scheme = sample.split('://')[0] + '://'
      elif '://' in sample and len(sample.split('://')[0]) > 0:
         print('\n\n*** Only http has been tested...proceed with caution ***\n\n')
         self.scheme = sample.split('://')[0] + '://'
      self.sample = sample.split('://')[-1]
      self.host = self.sample.split('/')[0] + '/'
      self.fldr = '/'.join(self.sample.split('/')[1:-1])
      self.file = self.sample.split('/')[-1].split('.')[0]
      self.urllead = self.scheme + self.host + self.fldr + '/'

      getann, self.filenames = True, []
      lead, trail = self.file[:47], self.file[-3:]
      for par in para:
         parstr = par
         if len(par) > 1: parstr = '.' + par
         for chan in channels:
            for typ in types:
               if par != 'ann': 
                  self.filenames.append(lead+chan+trail+'.'+typ+parstr) 
         if getann: 
            self.filenames.append(lead+chan+trail+'.ann')
            getann = False
###-------------------------------------------------------------------------------###

###-------------------------------------------------------------------------------###
if __name__=='__main__':
   args = sys.argv[1:]
   if len(args) < 1 or len(args) > 4:
      print(__doc__)
      sys.exit()
   main(args)



