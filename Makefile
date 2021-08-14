# Tutorial: https://makefiletutorial.com/#top
# command: gunicorn app.main:app -b $(HOST):$(PORT) -w $(WORKER_NUM) -k uvicorn.workers.UvicornWorker --access-logfile -


server:
	  gunicorn app.main:app -c gunicorn_config.py

dev_setup:
	 pip install -r requirements.dev.txt

test:
	pytest
