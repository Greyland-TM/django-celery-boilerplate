from django.db import models
from django.db.models import CharField, DateTimeField, BooleanField, DecimalField
from apps.accounts.models import Customer
from apps.monday_app.tasks import save_to_monday, save_to_monday


class ServicePackage(models.Model):
    """This model will be used to store the templates for posts."""

    TYPE_CHOICES = (
        ("type_1", "type_1"),
        ("type_2", "type_2"),
    )
    RELATED_APP_CHOICES = (
        ("app_1", "app_1"),
        ("app_2", "app_2"),
    )
    ACTION_CHOICES = (("create", "Create"),)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    related_app = CharField(max_length=100, default="", choices=RELATED_APP_CHOICES)
    type = CharField(max_length=100, default="", choices=TYPE_CHOICES)
    is_active = BooleanField(default=True)
    cost = DecimalField(max_digits=6, decimal_places=2)
    last_completed = DateTimeField(max_length=100, default=None, null=True, blank=True)
    date_started = DateTimeField(max_length=100, default=None, null=True, blank=True)
    next_scheduled = DateTimeField(max_length=100, default=None, null=True, blank=True)  # datetime
    requires_onboarding = BooleanField(default=False)
    action = CharField(max_length=100, default="create", choices=ACTION_CHOICES)
    error = CharField(max_length=100, default="")

    def save(self, customer_monday_id=None, *args, **kwargs):
        is_new = self._state.adding

        super(ServicePackage, self).save(*args, **kwargs)
        
        if is_new:
            save_to_monday.delay(self.customer.pk, 'package', is_new=True, package_pk=self.pk, customer_monday_id=customer_monday_id)