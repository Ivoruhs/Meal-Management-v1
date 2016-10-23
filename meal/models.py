from calendar import month
from datetime import datetime

from django.contrib.admin.utils import model_format_dict
from django.db import models

# Create your models here.
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.datetime_safe import date
from django.contrib.auth.models import User
# from twisted.names.client import lookupSenderPolicy


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=30)

    @property
    def name(self):
        return self.user

    def __str__(self):
        return "%s %s"%(self.id,self.name)

    def dates(self):
        return [d['date'] for d in self.log_set.values('date')]

    def entry(self):
        return self.log_set.filter(date__year=datetime.now().year).order_by('date')


class Log(models.Model):
    eid=models.ForeignKey(Employee,on_delete=CASCADE)
    date=models.DateField(default=datetime.now().date())

    def __str__(self):
        return "%s %s"%(self.eid,self.date)



#for signaler
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Employee.objects.get_or_create(user=kwargs.get('instance'))