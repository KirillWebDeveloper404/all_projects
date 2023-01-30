from loguru import logger
from pathlib import Path

logger.add('debug/debug.log', format='{time} - {level}: {message}', level='DEBUG')
logger.info('test')
logger.info(f'{Path(__file__).resolve().parent.parent}')