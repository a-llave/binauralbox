

"""
Description:

Author: Adrien Llave - CentraleSupelec
Date: 29/08/2018

Version: 1.0

Date    | Auth. | Vers.  |  Comments
18/08/29  ALl     1.0       Initialization

"""

import src.pkg.binauralbox as bb

hrtfdata = bb.HrtfData()
grid = bb.Grid()

print('TEST POSITIVE CASE')
assert bb.is_hrtfdata(hrtfdata), 'THE DATA HAVE TO BE A HRTF DATA OBJECT'

print('TEST NEGATIVE CASE')
assert not bb.is_hrtfdata(grid), 'THE DATA HAVE TO NOT BE A HRTF DATA OBJECT'

print('TEST SUCCESSFUL')





