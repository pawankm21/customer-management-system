from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User, Group
from .models import  Customer


def customer_signal(sender, instance, created, **kwargs):
    if created:
        group =Group.objects.get(name='admin')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name=instance.username,
        )

post_save.connect(customer_signal,sender=User)