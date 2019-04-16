from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    CustomerID = models.AutoField(primary_key=True, unique=True)
    CustomerAddress = models.CharField(max_length=50)
    CustomerCity = models.CharField(max_length=50)
    CustomerState = models.CharField(max_length=2)
    CustomerZIP = models.IntegerField()

    def __str__(self):
        return str(User.first_name) + " " + str(User.last_name)