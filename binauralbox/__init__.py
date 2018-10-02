"""
Description: class and functions needed for binaural data management

Author: Adrien Llave - CentraleSupelec
Date: 31/08/2018

Version: 5.0

Date    | Auth. | Vers.  |  Comments
18/03/28  ALl     1.0       Initialization
18/05/30  ALl     2.0       Class HrtfData: add default sampling frequency
18/06/01  ALl     3.0       Class HrtfData: bug fix in method 'subset', add copy of the self.
18/07/19  ALl     4.0       Add Class RTBinauralizerFFT which is the as RTBinauralizer but working in Freq domain
18/07/26  ALl     4.1       In HrtfData: check if file exists before import it
18/08/29  ALl     4.2       - Add function is_hrtfdata
                            - Add method 'get_spherical_weighting_harder' to class 'Grid'
18/08/31  ALl     5.0       MAJOR MODIF: Module to package

"""

from .HrtfData import *
from .Grid import *
from .is_hrtfdata import *
from .export_hrir_to_matfile import *
from .import_hrir_from_matfile import *
