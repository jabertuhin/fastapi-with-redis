# source: https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

bind = '0.0.0.0:8080'
backlog = 2048


workers = 2
worker_class = 'uvicorn.workers.UvicornWorker'


errorlog = '-'
loglevel = 'INFO'
accesslog = '-'