# gunicorn.conf.py
import logging

loglevel = 'info'
accesslog = '-'
errorlog = '-'
capture_output = True

logging.basicConfig(level=logging.INFO)