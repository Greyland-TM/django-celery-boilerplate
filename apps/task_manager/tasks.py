from boilerplate_django_celery.celery import app
from apps.app_1.utils import process_app_1_packages
from apps.app_2.utils import process_app_2_packages
from .models import ServicePackage

@app.task
def daily_task_check():
    print(f"Checking customer packages on the cron task schedule...")
    try:
        # Get the all of the packages
        package_array = ServicePackage.objects.all()        

        # Seperate them by related_app 
        app_1_packages = package_array.filter(related_app='app_1')
        app_2_packages = package_array.filter(related_app='app_2')

        # Send the packages to the respective apps for handeling
        process_app_1_packages(app_1_packages)
        process_app_2_packages(app_2_packages)
    except Exception as e:
        print(f'Error: {e}')
    return True
