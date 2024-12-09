import logging
import sys


logger = logging.getLogger('ssh')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler('ssh.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


