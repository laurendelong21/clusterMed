import os.path as osp
import os
from pathlib import Path

# set up directories
HOME = str(Path.home())
# CACHE AND LOGGING
CACHE = osp.join(HOME, '.clustr')
LOGS = osp.join(CACHE, 'logs')

# MAIN DIRS
MAIN_DIR = osp.dirname(osp.realpath(__file__))
PROJECT_DIR = osp.abspath(osp.join(MAIN_DIR, os.pardir))
