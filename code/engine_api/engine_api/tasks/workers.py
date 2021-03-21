from engine_api import celery as celery_app


@celery_app.task()
def make_file(fname, content):
    with open(fname, 'w') as f:
        f.write(content)
