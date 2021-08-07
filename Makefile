# Tutorial: https://makefiletutorial.com/#top

WORKER_NUM = 2
PORT = 8080
HOST = 0.0.0.0

server:
	  gunicorn app.main:app -b $(HOST):$(PORT) -w $(WORKER_NUM) -k uvicorn.workers.UvicornWorker

dev_setup:
	 pip install -r requirements.dev.txt

test:
	pytest
