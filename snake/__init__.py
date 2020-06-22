import sys

__author__ = 'James La Guma'
__version__ = '0.1'

if sys.version_info.major < 3 or (sys.version_info.minor < 6
                                  and sys.version_info.major == 3):
    raise ImportError('Python < 3.6 is unsupported.')
