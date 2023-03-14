from apps.package_manager.models import ServicePackage
from apps.app_2.tasks import app_2_run_ads, app_2_post_webpage, app_2_post_blog

def process_app_2_packages(app_2_packages):
    try:
        # Sort them by type
        app_2_blogs = app_2_packages.filter(type="blog").values_list(flat=True)
        app_2_webpages = app_2_packages.filter(type="webpage").values_list(flat=True)
        app_2_ads = app_2_packages.filter(type="ads").values_list(flat=True)
        print(f'Sorting app_2 packages... {app_2_blogs.count()} blogs, {app_2_webpages.count()} webpages, {app_2_ads.count()} ads')

        # TODO - Add more fiters for error handeling

        # Send to the correct tasks
        app_2_post_webpage.delay(list(app_2_webpages))
        app_2_post_blog.delay(list(app_2_blogs))
        app_2_run_ads.delay(list(app_2_ads))
        return True
    except Exception as e:
        print(f'Error: {e}')
    return True

