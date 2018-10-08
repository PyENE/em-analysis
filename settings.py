"""Given an xls file, build an OculometricDataset and provides data analysis tools
HMM_feat_outfile_v6_165_166.xls should be given as the xls file. It is the only one supported at the moment.
An OculometricDataset in a collection of TextReading which is a collection of Fixation.
These classes are described according to the useful information in the xls file.
"""

import os
# import sys

__author__ = 'Brice Olivier'
__copyright__ = ''
__credits__ = ['Brice Olivier', 'Jean-Baptiste Durand', 'Anne Guerin-Dugue']
__license__ = ''
__version__ = '1.0'
__maintainer__ = 'Brice Olivier'
__email__ = 'briceolivier1409@gmail.com'
__status__ = 'Prototype'

"""
os.environ['LD_LIBRARY_PATH'] += ':/home/bolivier/python-lib/'
os.environ['LD_LIBRARY_PATH'] += ':/home/bolivier/git/oculonimbus/ema/lib/vplants/sequence_analysis/build-scons/lib/'
os.environ['LD_LIBRARY_PATH'] += ':/home/bolivier/python-lib/lib'

os.environ['LD_LIBRARY_PATH'] += ':/home/bolivier/git/oculonimbus/'
os.environ['LD_LIBRARY_PATH'] += ':/home/bolivier/python-lib/'
os.environ['LD_LIBRARY_PATH'] += ':/usr/local/lib/'


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
SHARE_PATH = os.path.join(PROJECT_PATH, 'share')
DATA_PATH = os.path.join(SHARE_PATH, 'data')
MODELS_PATH = os.path.join(SHARE_PATH, 'models')
GRAPHICS_PATH = os.path.join(SHARE_PATH, 'graphics')
SRC_PATH = os.path.join(PROJECT_PATH, 'src')
ANALYSIS_PATH = os.path.join(PROJECT_PATH, 'notebooks')
TEST_PATH = os.path.join(PROJECT_PATH, 'test')


sys.path.append(PROJECT_PATH)
sys.path.append(SHARE_PATH)
sys.path.append(DATA_PATH)
sys.path.append(MODELS_PATH)
sys.path.append(GRAPHICS_PATH)
sys.path.append(SRC_PATH)
sys.path.append(ANALYSIS_PATH)
sys.path.append(TEST_PATH)
"""