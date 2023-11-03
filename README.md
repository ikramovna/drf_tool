# Setting Up Celery and Redis Your Project with Ngnix
## Step 1 — Installing Celery

First install redis 

```bash
sudo apt-get install redis-server
```

```bash
sudo service redis-server start
```

To install Celery, simply run the following command in your terminal:

```bash
pip install celery
```

## Step 2 — Configure Celery:
Create a Celery configuration file. You typically place this in your project directory or within your Django app. The file should define your Celery application and its settings. For example, you can create a file named 'celery.py':
```bash

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

app = Celery('your_project_name')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
```
## Step 3 — Configure Django Settings: 
In your Django project's settings (settings.py), configure Celery settings. Add the following lines to set up Celery with a message broker (e.g., Redis or RabbitMQ) and a result backend:

```bash
# Celery Configuration Options

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CELERY_TIMEZONE = "Asia/Tashkent"

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
```

## Step 4 — Start a Celery Worker: 
To start a Celery worker, you can run the following command from the directory where your Django project is located:
```bash
celery -A your_project_name worker --loglevel=info
```


