from pathlib import Path
import logging

BASE_DIR = Path(__file__).parent.parent
logger = logging.getLogger('system')
logging.basicConfig(filename=BASE_DIR / 'logs.log', level=logging.INFO)
