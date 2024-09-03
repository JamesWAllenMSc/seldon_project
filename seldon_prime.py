""" Control scripts for the Seldon Project
"""

__author__ = "James Allen"
__date__ = "2024-08-09"
__license__ = "GPL-3.0 license"
__version__ = "1.0.1"
__maintainer__ = "James Allen"
__email__ = "jameswallenmsc@gmail.com"
__status__ = "Development"


import logging
import sys

sys.path.append('/home/jamesallen/projects/seldon_project/lib')

from lib.exchanges_update import exchanges_update
from lib.ticker_update import ticker_update

# Logging config
logging.basicConfig(filename='logs/global_event.log', level=logging.INFO,
                        format='Datetime:%(asctime)s - Level:%(levelname)s - Module:%(module)s - Function:%(funcName)s - Message:%(message)s')


exchanges_update()
ticker_update()

