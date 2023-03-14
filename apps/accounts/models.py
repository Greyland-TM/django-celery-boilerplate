from django.db import models
from django.contrib.auth.models import User
from django.db.models import DateTimeField, CharField
from phonenumber_field.modelfields import PhoneNumberField


# CHANGE THIS TO "Representative"
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = CharField(default="Joe", max_length=100)
    last_name = CharField(default="Dierte", max_length=100)

    def __str__(self):
        return self.first_name


class Customer(models.Model):
    STATUS_CHOICE_FIELDS = (('lead', 'Lead'), ('customer', 'Customer'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rep = models.ForeignKey(Employee, on_delete=models.CASCADE)
    first_name = CharField(default="", max_length=100, null=False, blank=False)
    last_name = CharField(default="", max_length=100, null=False, blank=False)
    email = CharField(default="", max_length=100, null=False, blank=False)
    phone = PhoneNumberField(null=True, blank=True)
    status = CharField(default="lead", max_length=100, choices=STATUS_CHOICE_FIELDS)
    onboarding_date = DateTimeField(null=True, blank=True)
    monday_id = CharField(default="", max_length=100, null=True, blank=True)

    # NOTE - IMPORTANT: Any webhooks should update models with .update() to avoid infinite loops
    def save(self, sync_monday=False, *args, **kwargs):
        from apps.monday_app.tasks import save_to_monday

        is_new = self._state.adding
        super(Customer, self).save(*args, **kwargs)

        # Handle monday sync
        if sync_monday:
            print('Creating new lead in monday... (Check celery terminal)')
            monday_was_created = save_to_monday.delay(self.pk, 'lead', is_new).get()
            print(f'Sync success: {monday_was_created}')

        print('\nSaved customer to database!\n**********\n')

    def __str__(self):
        return self.first_name
