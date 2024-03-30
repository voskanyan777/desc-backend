from pathlib import Path
import logging

BASE_DIR = Path(__file__).parent.parent
logging.basicConfig(filename=BASE_DIR / 'logs.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', encoding='UTF-8')

logger = logging.getLogger()