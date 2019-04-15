from django.db import models


# Create your models here.
class Customer(models.Model):
    CustomerID = models.AutoField(primary_key=True, unique=True)
    CustomerName = models.TextField()
    CustomerEmail = models.EmailField()
    CustomerAddress = models.TextField()
