from apps.package_manager.models import ServicePackage
from apps.app_1.tasks import app_1_run_ads, app_1_post_webpage, app_1_post_blog

def process_app_1_packages(app_1_packages):
    try:
        # Sort them by type
        app_1_blogs = app_1_packages.filter(type="blog").values_list(flat=True)
        app_1_webpages = app_1_packages.filter(type="webpage").values_list(flat=True)
        app_1_ads = app_1_packages.filter(type="ads").values_list(flat=True)
        print(f'Sorting app_1 packages... {app_1_blogs.count()} blogs, {app_1_webpages.count()} webpages, {app_1_ads.count()} ads')

        # TODO - Add more fiters for error handeling

        # Send to the correct tasks
        app_1_post_webpage.delay(list(app_1_webpages))
        app_1_post_blog.delay(list(app_1_blogs))
        app_1_run_ads.delay(list(app_1_ads))
        return True
    except Exception as e:
        print(f'Error: {e}')
    return True

