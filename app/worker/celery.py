import logging
import os
from datetime import timedelta
from celery import Celery

from app.models import TypeCurrency

logger = logging.getLogger(__name__)

app = Celery('my_app',
             broker=os.environ.get("BROKER_URL"),
             backend=os.environ.get("BROKER_URL"),
             include=['app.worker.tasks'])

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    worker_hijack_root_logger=False,
)
## Шедулер по валютам
app.conf.beat_schedule = {

    "btc_usd": {
        "task": 'app.worker.tasks.test_task',
        "schedule": timedelta(minutes=1),
        "args": (TypeCurrency.btc_usd.name,),
    },
    "eth_usd": {
        "task": 'app.worker.tasks.test_task',
        "schedule": timedelta(minutes=1),
        "args": (TypeCurrency.eth_usd.name,),
    },
}
