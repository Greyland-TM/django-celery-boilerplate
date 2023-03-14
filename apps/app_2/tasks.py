from boilerplate_django_celery.celery import app
from apps.package_manager.models import ServicePackage


# TODO - These task will be called from the package manager after the celery beat task has determined that a package is due
@app.task
def app_2_task_1(list):
    print(f'Running app_2 tasks for {len(list)} items...')
    return True

@app.task
def app_2_task_2(list):
    print(f'Running app_2 tasks for {len(list)} items...')
    return True

@app.task
def app_2_task_3(list): 
    print(f'Running app_2 tasks for {len(list)} items...')
    return True

