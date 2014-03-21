#!/usr/bin/env python

"""
uavsar_polsar_download.py   :  Download UAVSAR PolSAR data from ASF through the password protection

Usage:

.. code-block:: bash 

   $ uavsar_polsar_download.py url [options]

Parameter
---------
   url   :  Any single URL corresponding to the desired UAVSAR data 

Options
-------
   para  :  data paradigm [default --> extension of url]
            :options:  
               |  all   --  get it all
               |  ann   --  get only the annotation file 
               |  mlc   --  get mlc data and annotation file
               |  stk   --  get compressed Stokes data and annotation file
               |  grd   --  get grd data and annotation file
               |  dem   --  get dem and annotation file
               |  kmz   --  get the kmz file
               
   chan  :  data channels (only works with all, mlc, or grd paradigms) [ach]
            :options:
               |  ach   --  get HHHH, HVHV, VVVV, HHHV, HHVV, HVVV data
               |  copl  --  get co-polarized data (HHHH, VVVV, and HHVV)
               |  crpl  --  get cross-pol data (HVHV, HHHV, and HVVV)
               |  powr  --  get power data (HHHH, VVVV, and HVHV)
               |  chan  --  any of {hhhh, hvhv, vvvv, hhhv, hhvv, hvvv} get data for the corresponding channel 

Notes
-----
* Use a comma separted list (no spaces) for multiple options (e.g. mlc,grd)

* Separate para and chan arguments with a space 

* Python Mechanize (http://wwwsearch.sourceforge.net/mechanize/) must be installed and 
   discoverable in PYTHONPATH

* For convenience, create a text file $HOME/.dathack.d whose first line reads:
   uavsarhttp:<username>:<password> (replace fields <username> and <password>) 
   (if you're concerned about privacy run: chmod a-rxw .dathack.d; chmod u+r .dathack.d )

* If $HOME/.dathack.d is not found or if line uavsarhttp:<username>:<password> is not
   present, the routine will prompt the user for the username and password

* See uavsar_insar_download.py documentation for examples.
 
"""
from __future__ import print_function, division
import sys,os
import numpy as np
from http_retrieve import http_retrieve, get_password

__title__      = 'uavsar_polsar_download.py'
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
   para,chan = _get_paradigm_channels(args) 
   urls = URLs(args[0],para,chan)
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
   all_paras = ['all','ann','dat','hgt','mlc','stk','grd','dem','kmz']
   all_chans = ['HHHH','HHHV','HHVV','HVVV','HVHV','VVVV'] 
   chan_opts = ['ach','cop','copl','crp','crpl','pow','powr','sig','sig0','nrcs',
                  'hhhh','hvhv','vvvv','hhhv','hhvv','hvvv']

   # set defaults
   para = [args[0].split('.')[-1].strip()]
   channels = ['ach']

   for i in np.arange(1,len(args)):
      tpar = False
      temp_para = args[i].split(',')
      for par in temp_para:
         if par in all_paras: tpar = True
      if tpar: 
         para = temp_para
      else:
         channels = temp_para

   if 'all' in para:
      para = all_paras[4:]
   if 'ach' in channels:
      channels = all_chans

   newpara, newchan = [], []
   for par in para:
      if par in all_paras: newpara.append(par)
   if len(newpara) < 1:
      if len(para) == 1: 
         print('Invalid paradigm: ',para)
      else:
         print('Invalid paradigms: ',para)
      sys.exit()

   for chan in channels:
      if chan in chan_opts: 
         if chan == 'copl' or chan == 'cop':
            newchan.append('HHHH'); newchan.append('HHVV'); newchan.append('VVVV')
         elif chan == 'crpl' or chan == 'crp':
            newchan.append('HVHV'); newchan.append('HHHV'); newchan.append('HVVV')
         elif chan == 'powr' or chan == 'pow' or chan == 'sig' or chan == 'nrcs' or chan == 'sig0':
            newchan.append('HHHH'); newchan.append('HVHV'); newchan.append('VVVV')
         elif chan in chan_opts[-6:]:
            newchan.append(chan.upper())
      elif chan in all_chans:
         newchan.append(chan)

   if len(newchan) < 1:
      if len(channels) == 1:
         print('Invalid channel: ',channels)
      else:
         print('Invalid channels: ',channels)
      sys.exit()
   
   newpara = uniquify_list(newpara)
   newchan = uniquify_list(newchan)
   return newpara, newchan

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
   def __init__(self,sample,para,channels):
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
      lead, trail = self.file[:34], self.file[-6:]
      for par in para:
         if par == 'mlc' or par == 'grd':
            for chan in channels:
               self.filenames.append(lead+chan+trail+'.'+par) 
         elif par == 'dat' or par == 'hgt' or par == 'kmz':
            self.filenames.append(lead+trail+'.'+par)
         elif par == 'stk': 
            self.filenames.append(lead+trail+'.dat')
         elif par == 'dem':
            self.filenames.append(lead+trail+'.hgt')
         if par != 'kmz' and getann: 
            self.filenames.append(lead+trail+'.ann')
            getann = False
###-------------------------------------------------------------------------------###

###-------------------------------------------------------------------------------###
if __name__=='__main__':
   args = sys.argv[1:]
   if len(args) < 1 or len(args) > 3:
      print(__doc__)
      sys.exit()
   main(args)



