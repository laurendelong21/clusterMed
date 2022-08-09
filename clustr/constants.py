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
GP_DATA = osp.join(PROCESSED_DATA, 'gp_mmorbs.tsv')
GP_DATA_MEN = osp.join(PROCESSED_DATA, 'gp_mmorbs_men.tsv')
GP_DATA_WOMEN = osp.join(PROCESSED_DATA, 'gp_mmorbs_women.tsv')

RESULTS = osp.join(PROJECT_DIR, 'results')

HIER_AGG_RESULTS = osp.join(RESULTS, 'hier_agg')
AGG_MEN = osp.join(HIER_AGG_RESULTS, 'men')
AGG_WOMEN = osp.join(HIER_AGG_RESULTS, 'women')

KMEDOIDS_RESULTS = osp.join(RESULTS, 'kmedoids')
KMEDOIDS_MEN = osp.join(KMEDOIDS_RESULTS, 'men')
KMEDOIDS_WOMEN = osp.join(KMEDOIDS_RESULTS, 'women')

KMODES_RESULTS = osp.join(RESULTS, 'kmodes')
KMODES_MEN = osp.join(KMODES_RESULTS, 'men')
KMODES_WOMEN = osp.join(KMODES_RESULTS, 'women')

LCA_RESULTS = osp.join(RESULTS, 'lca')
LCA_MEN = osp.join(LCA_RESULTS, 'men')
LCA_WOMEN = osp.join(LCA_RESULTS, 'women')

BERNOULLI_RESULTS = osp.join(RESULTS, 'bernoulli')

