from celery import Celery

from webapp import create_app
from webapp.config import DevConfig
from webapp.models import db
from webapp.tasks import log

def make_celery(app):
    celery = Celery(
            app.import_name,
            broker=app.config['CELERY_BROKER_URL'],
            backend=app.config['CELERY_BACKEND_URL']
            )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

# make a dev app (with no REST)
flask_app = create_app(DevConfig)
db.init_app(flask_app)
celery = make_celery(flask_app)

