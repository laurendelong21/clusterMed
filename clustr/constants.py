import os.path as osp
import os
from pathlib import Path
import importlib.resources

# set up directories
HOME = str(Path.home())
# CACHE AND LOGGING
CACHE = osp.join(HOME, '.clustr')
LOGS = osp.join(CACHE, 'logs')

# MAIN DIRS
#PROJECT_DIR = osp.dirname(osp.dirname(osp.realpath(__file__)))

def find_repo_directory():
    cwd = os.getcwd()
    if cwd.endswith('neurosymodal'):
        return cwd
    
    if osp.exists(osp.join(HOME, 'clusterMed')):
        return osp.join(HOME, 'clusterMed')

    # Get the directory of the currently executing script
    script_directory = osp.dirname(osp.realpath(__file__))
    
    # Navigate up the directory structure until we find the repo directory
    current_directory = script_directory
    while osp.basename(current_directory) != "clusterMed":
        parent_directory = osp.dirname(current_directory)
        # Break if we've reached the root directory
        if parent_directory == current_directory:
            print("NOTICE: Unable to find 'clusterMed' directory- is it nested?; creating data and results folders within HOME directory.")
            return HOME
        current_directory = parent_directory
    return current_directory

PROJECT_DIR = find_repo_directory()

DATA_DIR = osp.join(PROJECT_DIR, 'data')

# CREATE FOLDERS FOR RESULTS
RESULTS = osp.join(PROJECT_DIR, 'results')
HIER_AGG_RESULTS = osp.join(RESULTS, 'hier_agg')
KMEDOIDS_RESULTS = osp.join(RESULTS, 'kmedoids')
KMODES_RESULTS = osp.join(RESULTS, 'kmodes')
LCA_RESULTS = osp.join(RESULTS, 'lca')
