#!/usr/bin/env python

"""
http_retrieve.py :  Simple routine to download password-protected data

Usage: 

.. code-block:: bash 

   $ http_retrieve.py url

Parameter
---------
url   :  file URL 

Notes
-----
* Python Mechanize (http://wwwsearch.sourceforge.net/mechanize/) must be installed and 
   discoverable in PYTHONPATH

* For convenience, create a text file $HOME/.dathack.d whose first line reads:
   uavsarhttp:<username>:<password>
   (if you're concerned about privacy run: chmod a-rxw .dathack.d; chmod u+r .dathack.d )

* If $HOME/.dathack.d is not found or if line uavsarhttp:<username>:<password> is not
   present, the routine will prompt the user for the username and password

"""
from __future__ import print_function, division
import sys,os

__title__      = 'http_retrieve.py'
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
def http_retrieve(url,username=None,password=None):
   try:
      import re, mechanize
   except:
      print(__doc__.split('*')[1])
      sys.exit()
   from urllib2 import HTTPError

   br = mechanize.Browser()
   try:
      res = br.open(url)
   except HTTPError, e:  # is a file is password protected, enter info and move on
      br.select_form(nr=0)
      if username==None or password==None:
         username, password = get_password()
         br['userid']   = username
         br['password'] = password
      else:
         br['userid']   = username
         br['password'] = password
      try:
         br.submit()
      except HTTPError, e: 
         sys.exit("submit failed: %d: %s" % (e.code, e.msg))
      br.open(url)
   try:
      br.retrieve(url, url.split('/')[-1])
   except:
      print('Nothing to download at URL: '+url)

###-------------------------------------------------------------------------------###

def get_password(pfile='.dathack.d',lineid='uavsarhttp'):
   """
   Attempt to retrieve username and password from $HOME/pfile which has the format::

      <lineid>:<username>:<password>

   If unsuccessful, prompt the user for information 
   """
   from getpass import getpass 
   home = os.getenv('HOME')
   username, password = None, None
   try:
      fid = open(home+'/'+pfile)
      reads = fid.readlines()
      fid.close()
      for row in reads:
         if lineid in row:
            username = row.split(':')[1].strip()
            password = row.split(':')[2].strip()
      if not username:  username = raw_input('Enter username: ')
      if not password:  password = getpass('Enter password: ')
   except:
      username = raw_input('Enter username: ')
      password = getpass('Enter password: ')
   return username, password

###-------------------------------------------------------------------------------###
if __name__ == '__main__':
   args = sys.argv[1:]
   if len(args) != 1:
      print(__doc__)
      sys.exit()
   http_retrieve(args[0])
