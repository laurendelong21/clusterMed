import os
import os.path as osp
import logging
from clustr.constants import CACHE, LOGS


for folder in [CACHE, LOGS]:
    os.makedirs(folder, exist_ok=True)

# logging
logging.basicConfig(filename=osp.join(LOGS, 'mrc_mulmorb_clustering.log'),
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
