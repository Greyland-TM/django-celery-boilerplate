from .models import ServicePackage
from apps.accounts.models import Customer
from datetime import datetime
import dateutil.parser


# TODO - Create a new package for a customer.
# Accepts a dictionary of customer selected options.
# Returns a ServicePackage object or False.
def create_service_package(package, customer_pk):
    try:
        print("Creating service package...", package)
        customer = Customer.objects.get(pk=customer_pk)
        service_package = ServicePackage(
            customer=customer,
            related_app=package["related_app"],
            type=package["type"],
            cost=100,
            is_active= not package["requires_onboarding"],
            last_completed=None,
            date_started=None,
            next_scheduled=None,
            action=package["action"],
            # error=package.error,
            requires_onboarding=package["requires_onboarding"],
        )
        service_package.save()
        print('service package saved...')
    except Exception as e:
        print("\nError with create_service_package: ", e)
    return True


# TODO - Update a package for a customer.
# Accepts a dictionary of customer selected options.
# Returns a ServicePackage object or False.
def update_service_package(package):
    print("Updating an Existing ServicePackage...")
    return True

