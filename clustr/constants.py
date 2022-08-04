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
PROJECT_DIR = '/exports/csce/eddie/inf/groups/AIML/MRC_UKB/'

DATA = osp.join(PROJECT_DIR, 'data')
PROCESSED_DATA = osp.join(DATA, 'processed_LD')

RESULTS = osp.join(PROJECT_DIR, 'results')
HIER_AGG_RESULTS = osp.join(RESULTS, 'hier_agg')
KMEDOIDS_RESULTS = osp.join(RESULTS, 'kmedoids')
KMODES_RESULTS = osp.join(RESULTS, 'kmodes')
LCA_RESULTS = osp.join(RESULTS, 'lca')
BERNOULLI_RESULTS = osp.join(RESULTS, 'bernoulli')

