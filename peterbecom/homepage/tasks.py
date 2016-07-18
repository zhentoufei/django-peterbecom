import datetime

from celery.task import task



@task()
def sample_task(filepath):
    print "Writing to filepath", filepath
    with open(filepath, 'w') as f:
        f.write(
            datetime.datetime.utcnow().strftime('%b %H:%M:%S\n')
        )